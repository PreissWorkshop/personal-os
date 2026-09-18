"""The digest: a small, cached picture of the operation.

The employee reads docs/employee.md, registry/projects.yaml and
docs/migration-plan.md in full on every start. That is right for a worker and
fatal for a front desk - it is most of why a trivial question takes a minute
today. So the front desk reads a condensed digest instead, rebuilt only when
one of those files actually changes, and sent as a cached prompt prefix.

Cap is deliberate: a digest that grows without limit becomes the latency it
was written to remove.
"""

from __future__ import annotations

import logging
import re
import subprocess

from . import config

log = logging.getLogger("frontdesk.digest")

MAX_CHARS = 7000

SOURCES = (
    "registry/projects.yaml",
    "docs/migration-plan.md",
    "docs/employee.md",
    "docs/agent-system.md",
)

_cache: tuple[float, str] | None = None


def _mtime_signature() -> float:
    total = 0.0
    for rel in SOURCES:
        path = config.REPO_ROOT / rel
        if path.exists():
            total += path.stat().st_mtime
    return total


def get(force: bool = False) -> str:
    global _cache
    signature = _mtime_signature()
    if not force and _cache and _cache[0] == signature:
        return _cache[1]
    text = _build()
    _cache = (signature, text)
    log.info("digest rebuilt (%d chars)", len(text))
    return text


def _read(rel: str) -> str:
    path = config.REPO_ROOT / rel
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _build() -> str:
    parts: list[str] = []

    head = _git_head()
    if head:
        parts.append(f"personal-os HEAD: {head}")

    machines = _section(_read("registry/projects.yaml"), "machines:", "projects:")
    if machines:
        tidy = "\n".join(line.strip() for line in machines.splitlines() if line.strip())
        parts.append("MACHINES\n" + tidy)

    projects = _projects()
    if projects:
        parts.append("PROJECTS\n" + projects)

    open_items = _open_items()
    if open_items:
        parts.append("OPEN ITEMS from docs/migration-plan.md "
                     "(the living tracker; LOCKED = needs Tenis)\n" + open_items)

    gates = _section(_read("docs/employee.md"),
                     "## What needs Tenis's explicit OK", "## Hard rules")
    if gates:
        body = gates.split("\n", 1)[1] if "\n" in gates else gates
        parts.append("NEEDS TENIS'S EXPLICIT OK\n"
                     + _NOISE.sub("", body).strip())

    routines = _routines()
    if routines:
        parts.append("SCHEDULED CLOUD ROUTINES (they run with every machine off)\n"
                     + routines)

    reports = _recent_reports()
    if reports:
        parts.append("RECENT SESSION REPORTS (docs/reports/)\n" + reports)

    text = "\n\n".join(parts)
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n[digest truncated]"
    return text


def _git_head() -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(config.REPO_ROOT), "log", "-1", "--format=%h %cs %s"],
            capture_output=True, text=True, timeout=15, encoding="utf-8",
            errors="replace")
        return (proc.stdout or "").strip()[:200] if proc.returncode == 0 else ""
    except Exception:  # noqa: BLE001
        return ""


def _section(text: str, start: str, end: str) -> str:
    if not text or start not in text:
        return ""
    body = text.split(start, 1)[1]
    if end and end in body:
        body = body.split(end, 1)[0]
    return start + body if start.startswith("#") else body


def _projects() -> str:
    """id, status and this machine's root - not the prose."""
    text = _read("registry/projects.yaml")
    if not text:
        return ""
    lines: list[str] = []
    current: dict[str, str] = {}
    in_roots = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("- id:"):
            if current.get("id"):
                lines.append(_project_line(current))
            current = {"id": stripped.split("id:", 1)[1].strip()}
            in_roots = False
        elif stripped.startswith("status:") and current:
            value = stripped.split("status:", 1)[1].strip()
            # A YAML folded scalar (`status: >`) has its text on the following
            # lines; taking the marker literally printed "[>]" as the status.
            if value not in (">", "|", ">-", "|-", ""):
                current["status"] = value[:90]
        elif stripped.startswith("roots:"):
            in_roots = True
        elif in_roots and stripped.startswith("main-pc:"):
            root = stripped.split("main-pc:", 1)[1].strip()
            current["root"] = root.split("#", 1)[0].strip()
    if current.get("id"):
        lines.append(_project_line(current))
    return "\n".join(lines)


def _project_line(project: dict[str, str]) -> str:
    bits = [f"- {project['id']}"]
    if project.get("status"):
        bits.append(f"[{project['status']}]")
    if project.get("root"):
        bits.append(f"main-pc: {project['root']}")
    return " ".join(bits)


# The tracker's legend: done / in progress / needs Tenis.
_LOCK, _WIP, _DONE = "\U0001f512", "\u23f3", "\u2705"
_BULLET = re.compile(r"^(\s*)[-*]\s+(.*)$")
_NOISE = re.compile(r"[*`]+")


def _bullets(text: str) -> list[str]:
    """Reassemble whole bullets from a Markdown list.

    The tracker wraps a single item over three or four lines, so matching the
    one line that happens to carry the marker produced mid-sentence fragments
    - and worse, quoted the legend line itself as an open item. An item is
    only meaningful whole.
    """
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            current = None
            continue
        match = _BULLET.match(raw)
        if match:
            current = [match.group(2).strip()]
            blocks.append(current)
        elif current is not None and raw.startswith((" ", "\t")):
            current.append(raw.strip())
        else:
            current = None
    return [" ".join(block) for block in blocks]


def _open_items(limit: int = 14) -> str:
    text = _read("docs/migration-plan.md")
    if not text:
        return ""
    found: list[str] = []
    for item in _bullets(text):
        if _LOCK not in item and _WIP not in item:
            continue
        # A bullet that opens with the done marker is history, even when its
        # body still mentions a lock. Listing it as "needs Tenis" would be a
        # false open item, which is worse than omitting it.
        if item.lstrip().startswith(_DONE) or "RESOLVED" in item[:60].upper():
            continue
        marker = "LOCKED" if _LOCK in item else "WIP"
        line = item.replace(_LOCK, " ").replace(_WIP, " ")
        line = _NOISE.sub("", line)
        line = re.sub(r"\s+", " ", line).strip(" -\u2014")
        if len(line) < 12:
            continue
        if len(line) > 200:
            line = line[:199].rstrip() + "\u2026"
        found.append(f"- [{marker}] {line}")
    # The tracker is append-ordered: the newest open items are at the end.
    return "\n".join(found[-limit:])


def _routines() -> str:
    """Only the routine table from docs/agent-system.md.

    Taking everything between "Live now" and the next heading dragged in
    1800 characters of prose about connector scoping and the mailbox - which
    is history the front desk does not need and latency it should not pay.
    """
    text = _read("docs/agent-system.md")
    if not text:
        return ""
    rows: list[str] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != 2 or set(cells[0]) <= set("-: "):
            continue
        if cells[0].lower() == "routine":
            continue
        if "Employee" in cells[0] or "standup" in cells[0].lower():
            rows.append(f"- {cells[0]}: {cells[1]}")
    return "\n".join(rows)


def _recent_reports(limit: int = 6) -> str:
    folder = config.REPO_ROOT / "docs" / "reports"
    if not folder.is_dir():
        return ""
    names = sorted((p.name for p in folder.glob("*.md")), reverse=True)[:limit]
    return "\n".join(f"- {name}" for name in names)
