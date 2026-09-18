"""The shared state both tiers read: conversation, tasks, memory, reminders.

SQLite, machine-local, one file. This is what makes the front desk "see
everything" without re-reading the repo on every message.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ts       REAL    NOT NULL,
    chat_id  TEXT,
    role     TEXT    NOT NULL,      -- user | assistant
    text     TEXT    NOT NULL,
    via      TEXT                   -- text | voice | webhook | schedule
);
CREATE INDEX IF NOT EXISTS messages_ts ON messages(ts);

CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  REAL    NOT NULL,
    started_at  REAL,
    finished_at REAL,
    status      TEXT    NOT NULL,   -- queued | running | done | failed
    request     TEXT    NOT NULL,
    result      TEXT,
    log_path    TEXT,
    reported    INTEGER NOT NULL DEFAULT 0,
    nudged_at   REAL
);
CREATE INDEX IF NOT EXISTS tasks_status ON tasks(status);

CREATE TABLE IF NOT EXISTS facts (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    ts    REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS reminders (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    due_at  REAL NOT NULL,
    text    TEXT NOT NULL,
    sent_at REAL
);
CREATE INDEX IF NOT EXISTS reminders_due ON reminders(due_at, sent_at);

CREATE TABLE IF NOT EXISTS outbox (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ts      REAL NOT NULL,
    text    TEXT NOT NULL,
    sent_at REAL
);

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

_lock = threading.Lock()
_init_lock = threading.Lock()
_conn: sqlite3.Connection | None = None


def connect() -> sqlite3.Connection:
    """One connection, shared. Four threads reach this - the poll loop, the
    sender, the scheduler and the webhook - so opening it is guarded."""
    global _conn
    if _conn is not None:
        return _conn
    with _init_lock:
        if _conn is None:
            config.ensure_dirs()
            conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.executescript(SCHEMA)
            conn.commit()
            _conn = conn
    return _conn


def _run(sql: str, args: tuple = ()) -> sqlite3.Cursor:
    conn = connect()
    with _lock:
        cur = conn.execute(sql, args)
        conn.commit()
        return cur


def _all(sql: str, args: tuple = ()) -> list[sqlite3.Row]:
    conn = connect()
    with _lock:
        return conn.execute(sql, args).fetchall()


# --- meta -----------------------------------------------------------------

def get_meta(key: str, default: str | None = None) -> str | None:
    rows = _all("SELECT value FROM meta WHERE key = ?", (key,))
    return rows[0]["value"] if rows else default


def set_meta(key: str, value: str) -> None:
    _run("INSERT INTO meta(key, value) VALUES(?, ?) "
         "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, value))


# --- conversation ---------------------------------------------------------

def add_message(role: str, text: str, chat_id: str | None = None,
                via: str = "text") -> None:
    _run("INSERT INTO messages(ts, chat_id, role, text, via) VALUES(?,?,?,?,?)",
         (time.time(), chat_id, role, text, via))


def recent_messages(limit: int) -> list[dict[str, str]]:
    """Conversation history in the shape the Messages API wants.

    Two constraints the raw log does not satisfy, because the front desk also
    stores what it pushed unprompted: the first message must be a user
    message, and roles may not repeat. A morning brief followed by a job
    report is two assistant rows in a row, and sending that gets the whole
    request rejected. So: drop leading assistant rows, and merge a run of the
    same role into one message.
    """
    rows = _all("SELECT role, text FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    history: list[dict[str, str]] = []
    for row in reversed(rows):
        role = row["role"] if row["role"] in ("user", "assistant") else "assistant"
        text = (row["text"] or "").strip()
        if not text:
            continue
        if not history and role != "user":
            continue
        if history and history[-1]["role"] == role:
            history[-1]["content"] += "\n" + text
            continue
        history.append({"role": role, "content": text})
    # A trailing assistant row is fine: the caller appends the new user turn.
    return history


# --- tasks ----------------------------------------------------------------

def create_task(request: str) -> int:
    cur = _run("INSERT INTO tasks(created_at, status, request) VALUES(?,?,?)",
               (time.time(), "queued", request))
    return int(cur.lastrowid)


def start_task(task_id: int, log_path: str) -> None:
    _run("UPDATE tasks SET status='running', started_at=?, log_path=? WHERE id=?",
         (time.time(), log_path, task_id))


def finish_task(task_id: int, status: str, result: str) -> None:
    _run("UPDATE tasks SET status=?, finished_at=?, result=? WHERE id=?",
         (status, time.time(), result, task_id))


def get_task(task_id: int) -> sqlite3.Row | None:
    rows = _all("SELECT * FROM tasks WHERE id = ?", (task_id,))
    return rows[0] if rows else None


def open_tasks() -> list[sqlite3.Row]:
    return _all("SELECT * FROM tasks WHERE status IN ('queued','running') ORDER BY id")


def recent_tasks(limit: int = 8) -> list[sqlite3.Row]:
    return _all("SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (limit,))


def unreported_finished() -> list[sqlite3.Row]:
    return _all("SELECT * FROM tasks WHERE status IN ('done','failed') "
                "AND reported = 0 ORDER BY id")


def mark_reported(task_id: int) -> None:
    _run("UPDATE tasks SET reported = 1 WHERE id = ?", (task_id,))


def mark_nudged(task_id: int) -> None:
    _run("UPDATE tasks SET nudged_at = ? WHERE id = ?", (time.time(), task_id))


# --- memory ---------------------------------------------------------------

def remember(key: str, value: str) -> None:
    _run("INSERT INTO facts(key, value, ts) VALUES(?,?,?) "
         "ON CONFLICT(key) DO UPDATE SET value = excluded.value, ts = excluded.ts",
         (key.strip().lower(), value, time.time()))


def forget(key: str) -> bool:
    cur = _run("DELETE FROM facts WHERE key = ?", (key.strip().lower(),))
    return cur.rowcount > 0


def all_facts() -> list[sqlite3.Row]:
    return _all("SELECT key, value FROM facts ORDER BY ts DESC")


def search_facts(query: str) -> list[sqlite3.Row]:
    like = f"%{query.strip().lower()}%"
    return _all("SELECT key, value FROM facts WHERE key LIKE ? OR lower(value) LIKE ? "
                "ORDER BY ts DESC LIMIT 20", (like, like))


# --- reminders ------------------------------------------------------------

def add_reminder(due_at: float, text: str) -> int:
    cur = _run("INSERT INTO reminders(due_at, text) VALUES(?,?)", (due_at, text))
    return int(cur.lastrowid)


def due_reminders(now: float) -> list[sqlite3.Row]:
    return _all("SELECT * FROM reminders WHERE sent_at IS NULL AND due_at <= ? "
                "ORDER BY due_at", (now,))


def pending_reminders() -> list[sqlite3.Row]:
    return _all("SELECT * FROM reminders WHERE sent_at IS NULL ORDER BY due_at")


def mark_reminder_sent(reminder_id: int) -> None:
    _run("UPDATE reminders SET sent_at = ? WHERE id = ?", (time.time(), reminder_id))


# --- outbox ---------------------------------------------------------------
# Anything the front desk wants to push to the phone goes here first, so a
# Telegram outage delays a message instead of losing it.

def enqueue_push(text: str) -> None:
    _run("INSERT INTO outbox(ts, text) VALUES(?, ?)", (time.time(), text))


def pending_pushes() -> list[sqlite3.Row]:
    return _all("SELECT * FROM outbox WHERE sent_at IS NULL ORDER BY id LIMIT 20")


def mark_push_sent(push_id: int) -> None:
    _run("UPDATE outbox SET sent_at = ? WHERE id = ?", (time.time(), push_id))


def dump(path: Path) -> None:
    """Human-readable state dump, for debugging from the console."""
    payload: dict[str, Any] = {
        "tasks": [dict(r) for r in recent_tasks(20)],
        "facts": [dict(r) for r in all_facts()],
        "reminders": [dict(r) for r in pending_reminders()],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
