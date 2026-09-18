# The front desk

Written 2026-09-18. The fast agent that holds the phone.

## Why it exists

Phase 1 put Telegram **inside** the employee: `employee-session.ps1` started
one session with `--channels plugin:telegram`, so the same session that reads
repos, runs suites and pushes was also the one answering the phone. Three
consequences, all of them structural rather than bad luck:

1. **One session, one queue.** A message sent while the employee was working
   waited for the work. And its start brief orders a full read of
   `docs/employee.md`, `registry/projects.yaml` and `docs/migration-plan.md`,
   so even "what's open today?" rode a heavyweight session.
2. **It never spoke first.** The three cloud routines report into a session,
   not into a pocket. Speaking first is the one thing the Claude app cannot
   do — and it was the one thing missing. Tenis's verdict on 2026-09-18 was
   exact: *"I might as well just log on to my Claude app."* He was right.
3. **Voice existed but was manual.** `scripts/stt.py` and `scripts/tts.py`
   have been on main-pc since 2026-09-18, but `docs/employee.md` says text is
   the default and the session had to be told to use them each time.

The fix is an inversion, not an addition: **the fast agent holds the phone and
the employee gives it up.**

## The shape

| | Front desk | Employee |
|---|---|---|
| Code | `frontdesk/` in this repo, plain Python | Claude Code, as before |
| Owns | the Telegram bot | nothing on the phone |
| Model | `claude-haiku-4-5` (escalates to `claude-sonnet-5`) | whatever the CLI runs |
| Context | a **cached digest** of this repo | full reads, as before |
| Job | answer in about a second, or delegate and say so | do the work |
| Host | `PreissFrontDesk` logon task on main-pc | `PreissEmployee`, unchanged |
| Auth | an `ANTHROPIC_API_KEY` — calls the API directly | the claude.ai login, as before |

Telegram allows exactly **one poller per bot token** — the 409 Conflict
already documented in `docs/employee-setup-main-pc.md` step 3. So this is not
a preference: with the front desk installed, `employee-session.ps1` detects
the `PreissFrontDesk` task and starts **without** `--channels`. That is
automatic; `-KeepChannel` forces the old behaviour if the front desk is ever
removed.

## What the front desk may do — and what it cannot

It has **six tools and no others**: `delegate`, `task_status`, `remind`,
`remember`, `recall`, `escalate`. It has no shell, no file write, no git and
no network beyond Telegram and the model API. Everything that can change the
world goes through `delegate`, which starts a Claude Code session under the
auto-mode safety classifier, rooted in the right project, reading
`docs/employee.md` — so every gate in that file still applies.

That is the security property, and it is the reason a fast model is allowed to
sit on an open chat channel at all: **it can talk, and it can ask a gated
worker to act. It cannot act.**

It is also paired to one chat, the same posture as the plugin's
`access policy allowlist`. Anyone who finds the bot can message it, so:
the pairing code is printed **in the main-pc window and nowhere else** - never
sent over the channel it protects - five wrong codes lock pairing until the
front desk is restarted (which mints a new code), and once paired, any other
chat is ignored and logged.

## Where the second goes

Three things buy the latency, and they are the whole trick:

- **A cached system prompt.** The identity block and the digest are sent with
  `cache_control: ephemeral`, so the world-view is a cache read rather than
  thousands of fresh input tokens on every message.
- **A digest instead of a repo read.** `frontdesk/digest.py` condenses the
  machine map, the project roots, the open `LOCKED`/`WIP` items, the approval
  gates and the routine schedule into roughly 5 KB, rebuilt only when one of
  those files changes. Full detail stays in the repo, where the worker reads
  it.
- **`delegate` acknowledges before it dispatches.** The tool carries a `reply`
  field, sent to Telegram the instant the tool call arrives — so the
  acknowledgement never waits on a second model round trip.

`[UNVERIFIED — needs check]` The end-to-end reply time on main-pc. The design
targets about a second, and the log line after every turn prints the real
figure (`answered in N.NNs`) plus the cache-read token count. Check it there
rather than believing this paragraph.

## Speaking first

`frontdesk/scheduler.py` ticks every 20 s and pushes:

| Trigger | What lands on the phone |
|---|---|
| A reminder falls due | the reminder |
| A delegated job finishes | its report, cut to five lines, with the job number |
| A job has run 20 minutes in silence | one nudge, once, naming the job |
| 06:45 daily | the morning brief, composed from the digest; one line if the day is quiet |
| Anything POSTs to the webhook | the event |

The webhook (`frontdesk/webhook.py`, port 8787, shared-token) is how the rest
of the operation reaches the phone. It already understands the Surveillance
NVR's event shape — `surveillance/notify.py` posts `camera_name`, `kind`,
`zones`, `started_at` — so a fire or person alert lands in the same chat as
everything else, with no second bot and no second app. Anything that can POST
JSON works: CI, a build script, a Cloudflare Worker.

Bind it to the tailnet, never to the open internet. It is a doorbell: it can
push a message and nothing else.

## Voice

Voice note in → `scripts/stt.py` (faster-whisper, local, audio never leaves
the machine) → the transcript is **always quoted back** so a mishearing is
visible before it becomes a wrong answer → the answer, spoken back through
`scripts/tts.py` (Kokoro, `bm_george` at 1.2x) when the question was spoken.
`/voice on|off|auto` changes that; `auto` is the default and means
voice-in-voice-out.

Two honest limits:

- **English only.** `tts.py` passes `lang="en-us"` and `bm_george` is an
  English voice, so an Icelandic answer is sent as text rather than
  mispronounced confidently. `[UNVERIFIED — needs check]` whether the Kokoro
  build in `~\.cache\kokoro` carries any Icelandic voice at all.
- **Icelandic transcription is worse than English.** Whisper does handle
  Icelandic; accuracy is materially lower, which is exactly why the transcript
  is quoted back, and why a confidence below 0.75 is flagged in the reply.

## Phone calls — not built, deliberately

Tenis asked about a Jarvis that rings him and talks. That needs a telephony
provider, a number, per-minute fees and a realtime voice model, and it
reverses the 2026-09-07 decision in `docs/employee.md` that dropped WhatsApp
and voice on the same arithmetic. Decision 2026-09-18: **phase it.** The
voice-note loop above delivers most of the feel at no marginal cost; real
calls get their own assessment, with its own justification, the way WhatsApp
got one. `[UNVERIFIED — needs check]` Icelandic number availability and
per-minute pricing at any provider — nothing here was checked.

## Cost

The front desk runs on an API key, not the subscription, because a direct
call with prompt caching is what makes it fast. Haiku is the cheap model and
the cached prefix is most of each request. **Estimate, not a quote:** a few
hundred short messages a day is cents per day — an order of magnitude under
the $3–15/day that got WhatsApp rejected. Delegated work still rides the
claude.ai subscription, because `claude -p` uses the CLI login;
`frontdesk/employee.py` strips `ANTHROPIC_API_KEY` from every child process
so that stays true (an API key in the environment silently outranks the
claude.ai login — the same trap `employee-session.ps1` already works around).

Watch the real number in the console for a week before trusting either figure.

## Setup

Prerequisites: the phase-1 bootstrap is done (`PreissRelay` and
`PreissEmployee` exist), and Python 3.9+ is on PATH. Everything below runs at
main-pc; the shop PC refuses by `machine-role.ps1`.

**1. Get an API key** 🔒 — console.anthropic.com → API keys. Yours alone:
account creation and keys are never an agent's job. It is a `sk-ant-…` value
and it is not the claude.ai login.

**2. Store the secrets** (~2 min)

```powershell
cd C:\Projects\_system\personal-os; git pull
powershell -ExecutionPolicy Bypass -File scripts\frontdesk-set-key.ps1
```

A masked dialog, same as `employee-set-token.ps1` — Ctrl+V works there, and in
the black console window it does not. It reuses the bot token already stored
for the Telegram plugin, generates a webhook token, writes
`~\.claude\frontdesk\.env` and locks that file to your user. Nothing goes in
this repo and nothing goes through an agent.

**3. Check it before trusting it** (~1 min)

```powershell
powershell -ExecutionPolicy Bypass -File scripts\frontdesk-session.ps1 -SelfTest
```

66 offline checks: state, time parsing, the digest built from the real repo,
message splitting, event formatting, and the turn loop against a stubbed
model. It makes no Telegram or model call, so it proves the plumbing and not
the two live legs — those are proved by step 4.

**4. Run it and pair** (~3 min)

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-frontdesk-autostart.ps1
Start-ScheduledTask -TaskName PreissFrontDesk
```

The window prints a pairing code. From the phone, message the bot
`/pair <code>`. Then hand the phone over properly, so the employee stops
polling the same bot:

```powershell
Stop-ScheduledTask -TaskName PreissEmployee; Start-ScheduledTask -TaskName PreissEmployee
```

Its window should now say *"The front desk owns the Telegram bot; starting as
a worker with no channel."*

**5. Point the NVR at it** (optional) — read `FRONTDESK_WEBHOOK_TOKEN` out of
`~\.claude\frontdesk\.env` yourself and set the Surveillance webhook to
`http://main-pc:8787/event?token=<that value>`. Never paste that token into a
chat.

## If something misbehaves

- **The bot answers twice, or drops messages.** Both the front desk and the
  employee are polling. `Get-ScheduledTask PreissFrontDesk` should exist and
  be enabled, and the employee window should report that it has no channel.
  Restart `PreissEmployee`.
- **"No ANTHROPIC_API_KEY".** `~\.claude\frontdesk\.env` is missing or the key
  line is empty. Re-run `frontdesk-set-key.ps1`. A 401 in the log means the
  key is wrong, not absent.
- **Replies come back but nothing is ever dispatched.** The log's first lines
  print `worker CLI:`. If that says *not found*, `claude` is not on PATH for
  this process — run `scripts\employee-preflight.ps1`.
- **Voice notes come back as "voice is not set up".** The venv at
  `~\.venvs\stt` is missing. It is a main-pc/laptop thing and must never be
  installed on the shop PC.
- **Nothing pushes, but the chat works.** Pushes go through the outbox and
  need a paired chat. The log says `NOT PAIRED` if it is not.
- **Pairing says it is locked.** Five wrong codes. Restart the task; the new
  window prints a new code. If that happened without you typing a wrong code,
  someone else found the bot - the log names the chat id.
- **The morning brief did not arrive.** It fires once per day after 06:45 and
  claims the day in `meta.last_brief` before composing, so a crash mid-compose
  costs that day's brief rather than sending two. `/brief` asks for it now.
- **It answered something wrong about the operation.** The digest is a
  condensation, not the truth. `/digest` rebuilds it; if the content is wrong,
  fix `docs/migration-plan.md` or `registry/projects.yaml` — that is the
  source, and this is downstream of it.

## Changing how it behaves

The front desk's character, its brevity rule and its refusals live in
`IDENTITY` at the top of `frontdesk/brain.py`, and its world comes from this
repo through `frontdesk/digest.py`. Same principle as `docs/employee.md`:
behaviour changes by editing the file and pushing, never by editing one
prompt in one place. The restart loop pulls before each start, so a push is
live at the next restart.
