"""Delegation - handing real work to the employee.

The front desk answers; it does not work. Anything that needs files, a repo,
a build or a suite is spawned as a headless Claude Code session
(`claude -p`) rooted in the right project, running under the same rules as
the always-on employee because it reads the same docs/employee.md.

Why `claude -p` rather than SendMessage into the long-lived `employee`
session: a subprocess is trackable. The front desk gets a pid, an exit code,
a transcript on disk and a definite finish, so it can report back and nudge
when a job goes quiet. A message into a live session gives none of that, and
docs/employee.md already records the failure mode - a peer in
`requires_action` never replies, and the sender cannot tell.

The long-lived `employee` session stays as it is, for continuity work Tenis
drives himself from claude.ai/code.
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path

from . import config, state

log = logging.getLogger("frontdesk.employee")

TASK_TIMEOUT = 45 * 60      # a job still running after this is reported, not killed silently

BRIEF = """You were dispatched by the front desk on main-pc. Tenis is on his
phone and cannot watch you work.

Read docs/employee.md in personal-os and work by its rules. Hard limits that
apply to this job: no secrets, ever; nothing destructive, no shipping
HelmCNC, no merge to the website's main, nothing touching production, no
spending and no publishing without Tenis's explicit OK. If the job needs any
of those, stop and say exactly what needs his word.

THE JOB:
{request}

Finish with a report of at most five lines: the answer or the blocker first,
then what you verified and how, then anything still needing Tenis. Put detail
in the repo, not in the report. If a suite failed, quote the failure. If you
could not verify something, say so - never present a green you did not see.
Push anything you commit before you finish."""


def claude_binary() -> str | None:
    """Find the CLI the same way scripts/resolve-claude.ps1 does."""
    found = shutil.which("claude") or shutil.which("claude.exe")
    if found:
        return found
    for candidate in (
        config.HOME / ".local" / "bin" / "claude.exe",
        config.HOME / ".local" / "bin" / "claude",
        config.HOME / "AppData" / "Local" / "Programs" / "claude" / "claude.exe",
    ):
        if candidate.exists():
            return str(candidate)
    return None


def project_root(project: str | None) -> Path:
    """Resolve a project id to its root on THIS machine, per the registry.

    One session, one project root - CLAUDE.md's rule. An unknown id falls
    back to personal-os rather than guessing a path.
    """
    if not project:
        return config.REPO_ROOT
    wanted = project.strip().lower()
    if wanted in ("personal-os", "personal_os", "os", ""):
        return config.REPO_ROOT
    registry = config.REPO_ROOT / "registry" / "projects.yaml"
    try:
        text = registry.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return config.REPO_ROOT
    current, in_roots = None, False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("- id:"):
            current = stripped.split("id:", 1)[1].strip().lower()
            in_roots = False
        elif stripped.startswith("roots:"):
            in_roots = True
        elif in_roots and stripped.startswith("main-pc:") and current == wanted:
            root = Path(stripped.split("main-pc:", 1)[1].strip().strip('"'))
            return root if root.exists() else config.REPO_ROOT
    return config.REPO_ROOT


def _child_env() -> dict[str, str]:
    """`claude -p` must ride the claude.ai login, not the front desk's key.

    An ANTHROPIC_API_KEY in the environment silently outranks the claude.ai
    login - the exact trap scripts/employee-session.ps1 and
    scripts/relay-session.ps1 already work around. The front desk needs that
    key for its own fast model, so it strips it from every child.
    """
    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    return env


def delegate(request: str, project: str | None = None) -> int:
    """Queue a job and start it. Returns the task id immediately."""
    task_id = state.create_task(request if not project else f"[{project}] {request}")
    thread = threading.Thread(target=_run, args=(task_id, request, project),
                              name=f"task-{task_id}", daemon=True)
    thread.start()
    return task_id


def _run(task_id: int, request: str, project: str | None) -> None:
    config.ensure_dirs()
    log_path = config.TASK_LOG_DIR / f"task-{task_id}.log"
    state.start_task(task_id, str(log_path))

    binary = claude_binary()
    if not binary:
        state.finish_task(task_id, "failed",
                          "Claude Code not found on PATH. Run scripts\\employee-preflight.ps1.")
        return

    root = project_root(project)
    prompt = BRIEF.format(request=request.strip())
    cmd = [binary, "-p", "--permission-mode", "auto", prompt]

    started = time.time()
    try:
        proc = subprocess.run(
            cmd, cwd=str(root), env=_child_env(), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=TASK_TIMEOUT)
        output = (proc.stdout or "").strip()
        errors = (proc.stderr or "").strip()
        transcript = f"$ {' '.join(cmd[:4])} ...\ncwd: {root}\n\n{output}\n\n--- stderr ---\n{errors}"
        try:
            log_path.write_text(transcript, encoding="utf-8")
        except OSError:
            pass
        took = time.time() - started
        if proc.returncode != 0 and not output:
            state.finish_task(task_id, "failed",
                              _trim(errors or f"exit {proc.returncode}, no output"))
        else:
            state.finish_task(task_id, "done", _trim(output or errors or "(no output)"))
        log.info("task %d finished in %.0fs (exit %s)", task_id, took, proc.returncode)
    except subprocess.TimeoutExpired:
        state.finish_task(task_id, "failed",
                          f"Still running after {TASK_TIMEOUT // 60} minutes; gave up waiting. "
                          f"Transcript: {log_path}")
    except Exception as exc:  # noqa: BLE001 - a failed job must not kill the front desk
        log.exception("task %d crashed", task_id)
        state.finish_task(task_id, "failed", f"{type(exc).__name__}: {exc}")


_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def _trim(text: str, limit: int = 2000) -> str:
    """Keep the tail: a Claude Code run ends with its report."""
    clean = _ANSI.sub("", text).strip()
    if len(clean) <= limit:
        return clean
    return "...\n" + clean[-limit:]


def summary() -> str:
    """What the front desk tells Tenis when he asks what is going on."""
    rows = state.recent_tasks(8)
    if not rows:
        return "No jobs dispatched yet."
    now = time.time()
    lines = []
    for row in rows:
        if row["status"] == "running":
            age = int((now - (row["started_at"] or now)) / 60)
            lines.append(f"#{row['id']} running {age}m - {_short(row['request'])}")
        elif row["status"] == "queued":
            lines.append(f"#{row['id']} queued - {_short(row['request'])}")
        else:
            lines.append(f"#{row['id']} {row['status']} - {_short(row['request'])}")
    return "\n".join(lines)


def _short(text: str, limit: int = 70) -> str:
    one_line = " ".join((text or "").split())
    return one_line if len(one_line) <= limit else one_line[:limit - 1] + "…"
