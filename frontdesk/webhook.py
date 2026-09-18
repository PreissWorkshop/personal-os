"""Inbound events - anything in the operation that wants to reach the phone.

The Surveillance NVR already posts a JSON event per motion clip
(surveillance/notify.py -> webhook_url), so pointing it here puts a fire or a
person alert in the same chat as everything else, with no second bot and no
second app. Anything that can POST JSON works the same way: CI, a build, a
Cloudflare Worker, a script on the CNC PC.

Bound to the tailnet, never the open internet, and a shared token is required.
It is a doorbell, not an API: it can push a message and nothing else.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import config

log = logging.getLogger("frontdesk.webhook")

MAX_BODY = 64 * 1024


def _format(payload: dict) -> str:
    """Recognise the NVR's shape; fall back to compact JSON for anything else."""
    if payload.get("camera_name") or payload.get("camera"):
        name = payload.get("camera_name") or payload.get("camera")
        kind = str(payload.get("kind") or "movement")
        headline = {
            "fire": "POSSIBLE FIRE",
            "fall": "Something fell",
            "person": "Person",
            "large": "Large movement",
        }.get(kind, "Motion")
        when = payload.get("started_at")
        stamp = ""
        if isinstance(when, (int, float)):
            stamp = dt.datetime.fromtimestamp(when, dt.timezone.utc).strftime(" at %H:%M")
        zones = payload.get("zones")
        where = f" in {zones}" if zones else ""
        line = f"{headline} - {name}{stamp}{where}"
        if kind == "fire":
            line += ("\nCamera guess from flame-coloured flicker, not a smoke alarm. "
                     "Check in person.")
        return line

    if payload.get("text"):
        source = payload.get("source")
        return f"[{source}] {payload['text']}" if source else str(payload["text"])

    return "Event: " + json.dumps(payload, ensure_ascii=False)[:800]


class _Handler(BaseHTTPRequestHandler):
    server_version = "frontdesk"
    push = None
    token = ""

    def log_message(self, fmt, *args):  # noqa: A003 - quieten the default stderr spam
        log.debug(fmt, *args)

    def _reply(self, code: int, body: str) -> None:
        raw = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802 - health check only
        if self.path.split("?")[0] == "/health":
            self._reply(200, "ok")
        else:
            self._reply(404, "not found")

    def do_POST(self) -> None:  # noqa: N802
        path, _, query = self.path.partition("?")
        if path not in ("/event", "/"):
            self._reply(404, "not found")
            return

        supplied = ""
        for pair in query.split("&"):
            key, _, value = pair.partition("=")
            if key == "token":
                supplied = value
        supplied = supplied or (self.headers.get("X-Frontdesk-Token") or "")
        if not _Handler.token or supplied != _Handler.token:
            log.warning("rejected an event from %s: bad token", self.client_address[0])
            self._reply(403, "forbidden")
            return

        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            self._reply(400, "bad length")
            return

        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict):
                payload = {"text": str(payload)}
        except (UnicodeDecodeError, json.JSONDecodeError):
            payload = {"text": raw.decode("utf-8", "replace")[:800]}

        if _Handler.push:
            _Handler.push(_format(payload))
        self._reply(200, "queued")


def start(push, token: str) -> ThreadingHTTPServer | None:
    """Start the listener. No token configured means the door stays shut."""
    if not token:
        log.info("no FRONTDESK_WEBHOOK_TOKEN set - inbound events are off")
        return None
    _Handler.push = staticmethod(push)
    _Handler.token = token
    server = ThreadingHTTPServer((config.WEBHOOK_HOST, config.WEBHOOK_PORT), _Handler)
    thread = threading.Thread(target=server.serve_forever, name="webhook", daemon=True)
    thread.start()
    log.info("inbound events on http://%s:%d/event", config.WEBHOOK_HOST, config.WEBHOOK_PORT)
    return server
