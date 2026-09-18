# Agent system

## Two tiers (2026-09-18)

**The front desk answers; the employee works.** A fast agent
(`frontdesk/`, Haiku-class, ~5 KB cached digest of this repo) owns the
Telegram bot and replies in about a second; anything needing files, a repo, a
build or a push is dispatched to a Claude Code session that reads
`docs/employee.md` as always. The employee gave up the channel the same day -
Telegram allows one poller per bot token, so `employee-session.ps1` detects
the `PreissFrontDesk` task and starts without `--channels`.

Why the split: phase 1 put the channel inside the worker, so the phone queued
behind the work, nothing ever spoke first, and voice was manual. That is the
whole of why Tenis said the Telegram employee gave him nothing the Claude app
did not. The front desk also brings the piece no other surface has - it pushes
without being asked: reminders, finished-job reports, a nudge on a silent job,
a 06:45 brief, and a webhook the Surveillance NVR can already talk to.

Design, limits and setup: `docs/frontdesk.md`. It has six tools, no shell and
no file write, so a fast model on an open chat channel can talk and can ask a
gated worker to act - it cannot act itself.

## The employee (2026-09)

`docs/employee.md` is the agent identity: one set of rules every surface
reads — cloud routines today, an always-on session on main-pc next, a
Managed Agent later. Behaviour changes by editing that file
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

**main-pc is the always-on host (2026-09-17)** — the laptop runs nothing
unattended. `scripts/main-pc-always-on.ps1`, run once at main-pc, registers
`PreissRelay`: a logon task keeping `claude --remote-control main-pc` alive,
so the laptop reaches main-pc by `SendMessage` the way it reaches the shop
PC. Phase 1 (Telegram + the employee session + its own mailbox) follows on
top: `docs/employee-setup-main-pc.md`, `scripts/employee-*.ps1`.

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
5. ✅ **Phone: done 2026-09-18.** Telegram into the always-on `employee`
   session on main-pc (PREISSWORKSHOP), paired to Tenis alone, relay
   `main-pc` beside it. ⏳ The mailbox `assistant@preissworkshop.is` is
   still open (setup doc step 7). **WhatsApp was assessed and dropped the same
   day** — no official support in the Claude stack, per-message fees, Meta
   verification, and a bridge and Managed Agent to pay for, all to deliver
   the same chat box Telegram gives free.
6. ✅ **Front desk: built 2026-09-18.** The phone belongs to the fast tier,
   the employee is a worker reached through it, and something in the
   operation finally speaks first. Four steps are Tenis's
   (`docs/frontdesk.md` → Setup). Phone calls were assessed and phased, not
   built - telephony reverses the 09-07 voice decision on the same
   arithmetic, and voice notes cover the case.
7. Business/media agents (marketing, sales, content, social) join only once
   the engineering loop is boring and reliable.

Anti-goal: turning any single tool into the whole operating system.
personal-os is the coordination point; GitHub carries the state.
