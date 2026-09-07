# Agent system

## The employee (2026-09)

`docs/employee.md` is the agent identity: one set of rules every surface
reads — cloud routines today, an always-on session on main-pc from
2026-09-10, a Managed Agent later. Behaviour changes by editing that file
and pushing, never by editing one prompt in one place.

**Live now — three cloud routines** (claude.ai/code/routines; they run with
every machine off, on subscription usage):

| Routine | Cadence (UTC = Iceland) |
|---|---|
| Employee - weekday standup | 06:30 Mon-Fri |
| Employee - weekly website audit | 07:00 Wed |
| Employee - weekly project report | 15:00 Fri |

**Scoping rule, learned the hard way:** a routine created from any surface
silently inherits *every* claude.ai connector — Gmail and Calendar included,
with write access, usable without asking during an unattended run. Strip
them (`clear_mcp_connections`) unless the routine genuinely needs one, and
check `mcp_connections` on the response. See
`docs/reports/2026-09-07-employee-agent.md`.

Phase 1 (Telegram + always-on session on main-pc + the employee's own
mailbox) is scripted and waiting: `docs/employee-setup-main-pc.md`,
`scripts/employee-*.ps1`.

**The employee has an address**, `assistant@preissworkshop.is` — never
Tenis's own, and it signs as the workshop rather than as him. Outgoing mail
is outbox-first through `src/api/mail.js`, so a draft is a `crm_outbox` row
and a row is not a sent mail. What it may send unattended is deliberately
narrow; anything carrying a commitment waits for Tenis. The rules are in
`docs/employee.md` → E-mail, and they are the binding version.

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
4. ✅ **Done 2026-09-07, in the cloud rather than on a machine.** The first
   master agent is `docs/employee.md`, read by three routines that need no
   computer to be awake. Step 4's point stands: prove the dispatch loop
   before writing custom orchestration — the first standup fires 2026-09-08.
5. ⏳ Reach it from the phone, and give it a mailbox: Telegram into an
   always-on main-pc session plus `assistant@preissworkshop.is`, both free,
   both Thursday 2026-09-10. **WhatsApp was assessed and dropped the same
   day** — no official support in the Claude stack, per-message fees, Meta
   verification, and a bridge and Managed Agent to pay for, all to deliver
   the same chat box Telegram gives free.
6. Business/media agents (marketing, sales, content, social) join only once
   the engineering loop is boring and reliable.

Anti-goal: turning any single tool into the whole operating system.
personal-os is the coordination point; GitHub carries the state.
