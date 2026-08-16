# Agent system

## Today (2026-08)

- **Claude Code** runs on each machine. Sessions scope to a project root and
  carry per-root persistent memory on that machine. personal-os is the
  shared, versioned brain any session can read — local memory is cache, this
  repo is truth.
- Binding instruction files, in order: `~/.claude/CLAUDE.md` (global rules +
  project boundaries), per-project `CLAUDE.md` in-tree, project handoff notes
  (`HELMCNC_NOTES.md`).
- **helm-reports** skill triages customer bug/feature reports from the
  HelmCNC SUPPORT screen.
- **Codex CLI** — configured on cnc-pc (`~/.codex`) but not on PATH; intended
  role: second engineering/review worker, to be re-wired on main-pc.

## Direction — build incrementally, in this order

1. Keep personal-os current; every machine and agent reads the same world.
2. main-pc becomes the primary agent host (cnc-pc is too weak and belongs to
   the machine; it runs HelmCNC sessions only).
3. Re-wire Codex on main-pc as reviewer; Claude Code as builder.
4. The first "master agent" is simply a Claude session rooted in personal-os
   that reads the registry + project notes and dispatches work — prove the
   loop before writing any custom orchestration.
5. Business/media agents (marketing, sales, content, social) join only once
   the engineering loop is boring and reliable.

Anti-goal: turning any single tool into the whole operating system.
personal-os is the coordination point; GitHub carries the state.
