# The employee — assessment, and phase 0 built (2026-09-07, laptop session)

Goal Tenis set: one always-on "employee" he can message from his phone that
knows every project, takes tasks, gives reports, and delegates so work
continues while he is elsewhere. Before today, nothing was automated: every
action needed his prompt. Verified from this laptop: **zero routines, zero
scheduled tasks, zero API triggers existed on the account.**

## What is true about the tooling

Checked against the official docs today, not from memory.

- **WhatsApp: no official support anywhere in Anthropic's stack** - and, as of
  this afternoon, **dropped** - see Cost below. Claude Code
  channels ship Telegram, Discord and iMessage; during the research preview
  `--channels` only accepts plugins from an Anthropic-maintained allowlist, so
  the community WhatsApp plugin needs the `--dangerously-load-development-channels`
  escape hatch. Real WhatsApp means Meta's Business Cloud API plus a bridge we
  write. **Voice calls** are further: the WhatsApp Business Calling API exists
  (VoIP, call webhooks) but needs a media server plus speech-to-text and
  text-to-speech. Not offered in US/CA/TR/EG/VN/NG;
  Iceland `[UNVERIFIED — needs check]` against Meta's country list.
- **Everything else he asked for already exists**, split over two products:
  - *Subscription:* Remote Control (drive a local session from the phone),
    channels (chat bridge into a running session), **routines** (cloud runs on
    cron / API call / GitHub event, with every machine off), Desktop scheduled
    tasks, session-to-session `SendMessage`.
  - *API (Managed Agents, beta):* persistent sessions, memory stores that
    survive a session, a coordinator with a roster of specialists, scheduled
    deployments, webhooks, hard dollar budgets. The only surface that gives a
    persistent identity reachable by webhook — i.e. WhatsApp-native.

## Built today — phase 0 is live

- **`docs/employee.md`** — the employee itself: identity, first moves, what it
  may do alone, what needs Tenis, hard rules, delegation, reporting. Every
  surface (routine, local session, future Managed Agent) reads this one file,
  so behaviour is changed by editing this repo, not by editing a prompt.
- **Three cloud routines**, created and connector-scoped:

  | Routine | Cadence (UTC = Iceland) | Does |
  |---|---|---|
  | Employee - weekday standup | 06:30 Mon-Fri | Reads the four repos and the tracker; 12-line standup: MOVED / BLOCKED / WATCH / TODAY. No commit on a normal day. |
  | Employee - weekly website audit | 07:00 Wed | Builds the site, audits output, fixes only unambiguous breakage, PR + report. Never merges to `main`. |
  | Employee - weekly project report | 15:00 Fri | Week in review across all repos, dated report + tracker update, PR against this repo. |

  All three run `claude-sonnet-5`, clone from GitHub, and end with a short
  summary Tenis reads in the app or on claude.ai.
- **Phase 1 prepared for main-pc** — `docs/employee-setup-main-pc.md` plus
  `scripts/employee-preflight.ps1`, `scripts/employee-session.ps1`,
  `scripts/install-employee-autostart.ps1`. Tenis is next at main-pc
  **Thursday 2026-09-10**; the sitting is run-and-verify, not build.

## Cost — the question Tenis asked, and the decision

He asked what the cheapest way is, and whether Telegram is cheaper and
easier. It is, by a wide margin, and he added that he does not care which
chat app it is because it works the same way. So **WhatsApp is dropped and
Telegram is the channel.**

| | Telegram | WhatsApp Cloud API |
|---|---|---|
| Per message | free, no per-message fee, no volume cap | charged per delivered template message, by category and country; Europe sits at the high end. Service replies inside the 24-hour window are free |
| Account | a bot from BotFather, minutes | Meta Business account, a spare number, business verification that can take days |
| Code to write and host | none, the plugin is official | a bridge we write, host and maintain |
| Brain it needs | routines + a local session, both inside the existing subscription | a Managed Agent to be webhook-reachable: roughly $3-15/day of API usage |

Dropping WhatsApp removes the only paid tier in the whole plan. What is left
runs on the Claude subscription he already has, plus Cloudflare and Resend
free tiers.

**Total additional cost of the employee, chat and e-mail included: nothing.**
Not a reduced bill - no new bill. Voice went the same way: WhatsApp voice
would need a media server plus speech-to-text and text-to-speech, and voice
notes into Telegram cover the case for free.

## E-mail — the employee gets its own address

Tenis asked for the employee to have its own address so it can deal with
suppliers and clients on his behalf. It is `assistant@preissworkshop.is`,
and it is close to free and close to instant, because most of it is already
running:

- **Inbound is most of the way there.** Cloudflare Email Routing is live on
  `preissworkshop.is` - verified today by DNS lookup, MX at
  `route1-3.mx.cloudflare.net`, SPF `include:_spf.mx.cloudflare.net`. The
  2026-09-06 notes record a catch-all to `preissworkshop@gmail.com`, which
  would mean the new address already receives; the catch-all rule itself is
  `[UNVERIFIED - needs check]` from outside, so it wants one test mail. The
  named route is two minutes either way.
- **Outbound needs one key.** `src/api/mail.js` in the website repo is
  already written against Resend's free tier (3,000/month) and is
  **outbox-first**: every message becomes a `crm_outbox` row in D1 before any
  provider sees it. That was built so a visitor's message is never lost while
  mail is unconfigured, and it happens to be exactly the approval gate an
  agent mailbox needs. A draft is a row; a row is not a sent mail. This is
  TODO-OWNER item "Connect outgoing e-mail (Resend, free)", already on his
  list for the CRM.
- **Not built yet:** the Email Worker that files inbound mail onto the client
  timeline instead of a shared Gmail. That is phase 4 of the website repo's
  `WORKSHOP-OS.md`, and it is what makes the employee read only its own
  correspondence rather than a mailbox it shares with him. Worth doing, after
  the two steps above, on main-pc where it can be tested live.

**The address is deliberately not his.** It signs as Preiss Workshop, never
as Tenis personally. A supplier reading it is being told the truth, a mistake
stays contained, and replies land where the employee can see them.

**What it may send alone is narrow on purpose** - acknowledgements with a
reference, a supplier asked for a price list or lead time, a chase with
nothing new added. Anything carrying a commitment - prices, dates, accepting
or declining an order, an unhappy client, a first approach to a stranger,
money in either direction - is drafted to the outbox and waits. The full
list is in `docs/employee.md` -> E-mail. Widen it once it has a track record
he has actually read; that is how a new hire earns the client list, and the
same logic applies here.

## A trap worth recording

**Cloud routines silently inherit every claude.ai connector.** All three came
back from the API carrying Gmail, Google Calendar and Claude Code Remote, none
of which was requested — and a routine can use every tool of an attached
connector, writes included, without asking, during an unattended run. That is
mail-send authority on a job that only needs git. All three were updated to
`clear_mcp_connections`, verified back as `mcp_connections: []`. **Check this
on every routine created from any surface.**

Second, smaller: PowerShell 5.1 reads `.ps1` files as ANSI, so a UTF-8 em-dash
in a script turns into a string-terminator error. The three scripts are
ASCII-only and parse clean. Keep them that way.

## What could be wrong

- ~~The routines have never fired yet.~~ **The standup was test-fired today
  and succeeded** (run 12:41-12:44, status SUCCEEDED). It cloned all four
  repos, read `employee.md`, the registry and the tracker, and found on its
  own that the "uncommitted button-sweep work" item had been open for eight
  days after helmcnc-app `67a0596` landed it on 2026-08-30. It corrected the
  tracker, pushed `claude/migration-plan-button-sweep-correction-0907`, and
  opened PR #1 — which was verified against the real commit and merged.
  It also flagged the website branch drift that this session then fixed.
  So cloning, GitHub access, PR creation and the honesty rules all work.
  Still true in general: a green run status means the session started and
  exited, **not** that the task succeeded — read the transcript.
- HelmCNC **support-report triage was dropped from phase 0 on purpose.** The
  reports live behind an admin endpoint whose token is in the Signing folder;
  a cloud sandbox has neither the token nor the network permission, and this
  repo will not carry it. That job stays on main-pc or cnc-pc.
- The website audit assumes `python src/site/build.py` works in the sandbox
  with stdlib only. True on the dev machines; unverified in the cloud
  environment until Wednesday.

## What was verified, and how

Docs read today: channels, routines, Managed Agents (core, memory, multiagent,
deployments, webhooks, repo resources, tool policies). Account state read via
the routines API. Scripts parse-checked with the PowerShell parser;
`employee-preflight.ps1` executed on the laptop and reported correctly.
Routine creation and the connector strip confirmed from the API responses.

## What needs Tenis

1. **Thursday at main-pc**: `docs/employee-setup-main-pc.md`, steps 1-6. Two
   items are his alone — creating the Telegram bot, and choosing the
   permission posture (the shipped default is safe).
2. ~~Phase 2 go/no-go~~ **Decided 2026-09-07: no WhatsApp, no Managed Agent,
   no API bill.** Telegram is the channel. The Thursday sitting now also
   turns on the employee's e-mail - three signups that are his alone
   (Telegram bot, Resend account, the Cloudflare route).
3. Open items from `migration-plan.md` are unchanged and still his.

## Safest next step

Phase 0 is proven, so Thursday is a 20-minute sitting, not a build. Read the
06:30 standup on 2026-09-08 to see the employee working unprompted, then run
`docs/employee-setup-main-pc.md` at main-pc.

The employee's own pick for what matters most, from its first run: **the
shop-PC permission-gating question**, open since 2026-08-27 on the machine
wired to the live CNC. Five minutes checking
`shell:startup\claude-remote-control.cmd` for a skip-permissions flag,
before anything else runs there.
