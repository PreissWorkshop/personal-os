# Employee phase 1 — main-pc setup

Everything here was prepared 2026-09-07 from the laptop and is meant to be
**run on main-pc**, first sitting 2026-09-10 (Thursday). Nothing in it needs
a decision while you are at the keyboard except the two marked 🔒.

Goal: an always-on Claude Code session on main-pc, rooted in this repo,
reachable from the phone by Telegram, that reads `docs/employee.md` and
runs the operation between sittings. Cloud routines (phase 0) are already
live and need none of this.

## Before you start

Everything is on GitHub. On main-pc:

```powershell
cd C:\Projects\_system\personal-os; git pull
```

## Step 1 — prerequisites (~5 min)

The channel plugins are Bun scripts, so Bun is required. Claude Code must be
on PATH for a scheduled task to launch it.

```powershell
powershell -ExecutionPolicy Bypass -File C:\Projects\_system\personal-os\scripts\employee-preflight.ps1
```

It checks Claude Code, Bun, git, the repo clones, and the claude.ai login,
and prints exactly what is missing. Install Bun if it says so:

```powershell
irm bun.sh/install.ps1 | iex
```

## Step 2 — 🔒 create the Telegram bot (~3 min, yours)

Account creation is yours, not the agent's.

1. Open Telegram, message **@BotFather**, send `/newbot`.
2. Give it a display name (e.g. `Preiss Workshop`) and a username ending in
   `bot` (e.g. `preiss_workshop_bot`).
3. Copy the token BotFather returns. It is a secret: it goes in the
   configure command below and nowhere else. Never into this repo.

## Step 3 — install and configure the channel (~5 min)

In a normal Claude Code session on main-pc:

```
/plugin install telegram@claude-plugins-official
```

If it reports the marketplace is missing, add it and retry:

```
/plugin marketplace add anthropics/claude-plugins-official
```

Choose the **user** scope so it works from every project. If the summary
says to, run `/reload-plugins`. Then, with the token from step 2:

```
/telegram:configure <token>
```

That writes `~/.claude/channels/telegram/.env` — machine-local, never
committed.

## Step 4 — first run and pairing (~5 min)

Exit Claude Code and start the employee session:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Projects\_system\personal-os\scripts\employee-session.ps1
```

Then, from your phone:

1. Message the bot anything. It replies with a pairing code.
2. Back in the session on main-pc: `/telegram:access pair <code>`
3. Lock it down so only you can reach it:
   `/telegram:access policy allowlist`

Test it: from the phone, send *"read docs/employee.md and tell me today's
open 🔒 items"*. The answer comes back in Telegram.

## Step 5 — autostart at logon (~2 min)

So it comes back by itself after a reboot:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Projects\_system\personal-os\scripts\install-employee-autostart.ps1
```

This registers a per-user scheduled task, `PreissEmployee`, that runs
`employee-session.ps1` at logon in a minimized window. Same pattern as the
shop PC's `claude --remote-control` autostart. Remove it any time with:

```powershell
Unregister-ScheduledTask -TaskName PreissEmployee -Confirm:$false
```

## Step 6 — 🔒 decide the permission posture

The session runs unattended, so it will hit permission prompts while you are
away. Three options, least to most permissive:

1. **As-is (recommended).** Prompts pause the session; you approve from the
   phone via Remote Control, or from claude.ai/code in any browser. Safe,
   occasionally slow.
2. **Allowlist the boring reads** in `~/.claude/settings.json` on main-pc
   (`git status`, `git log`, `python -m pytest`, and similar) so routine work
   never stalls. Middle ground, and the one to grow into.
3. **`--dangerously-skip-permissions`.** Do not. This machine can push to
   every repo in the operation, and `docs/migration-plan.md` already carries
   an open 🔒 item about the shop session appearing to run ungated — that is
   a problem to fix, not a pattern to copy.

The script ships option 1. Nothing to do unless you want to change it.

## What the session does once running

It reads `docs/employee.md` on start, so its behaviour lives in this repo,
not in a prompt. It answers from the phone, keeps the tracker current, fires
and reviews the cloud routines, files machine-bound work as GitHub issues,
and pushes what it produces.

## If something misbehaves

- **The bot does not reply**: the session is not running with `--channels`.
  The bot can only answer while the channel is active.
- **The task did not start at logon**: `Get-ScheduledTask PreissEmployee`,
  then check `Get-ScheduledTaskInfo PreissEmployee` for the last result.
- **Channels do not appear in `claude --help`**: expected. The flag works
  while the feature is in research preview but is not listed.
- **A cloud routine did nothing**: ask any session `/schedule why did my
  <name> routine do nothing this morning?` — it reads the run log.
