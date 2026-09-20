# Migration plan — the 2026-08 cleanup

Full read-only discovery ran 2026-08-16 on cnc-pc. This file tracks
execution. Legend: ✅ done · ⏳ in progress · 🔒 needs Tenis.

## Executed 2026-08-16 (from the cnc-pc session)

- ✅ Full ScanPen safety copy → `D:\ScanPen-backup-2026-08-16` (USB stick) —
  verified: 843 files, 6.50 GB incl. `.git` and the uncommitted capture
  takes, 0 failures
- ✅ personal-os relocated: fresh clone at `C:\Projects\_system\personal-os`,
  seeded, pushed to origin/main
- ✅ scanpen pushed: `PreissWorkshop/scanpen` (private), `master` @ 506dd95 —
  135 files, ~10 MB, largest blob 1.5 MB; `PROVENANCE.md` maps to the full
  local history (`C:\ScanPen` @ 3e90a27 + the D: copy)
- ✅ helmcnc-app: 20 already-made local commits pushed (origin/master
  22fc611 → 0a0b493); local-only branch `resume-rapid-approach` pushed as
  backup. No working-tree changes made.
- ✅ Old `C:\HelmCNC\GitHub\personal-os` clone deleted (guard first refused —
  it held one auto-fetched ref, verified to be the new repo's own first
  commit — then re-verified every ref as contained in the new history);
  empty `GitHub\` parent removed. The production install dir hosts no repos
  anymore.

## Executed 2026-08-20 (from the main-pc session)

- ✅ main-pc bootstrapped per `Post/MAIN-PC-SETUP.md`: Python 3.11.9, VS Code,
  gh installed (all user-scope); personal-os / scanpen / helmcnc-app cloned to
  their registry roots; GCM credential (PreissWorkshop) verified push-capable —
  the sign-in step was already done.
- ✅ **ScanPen verified on main-pc**: fresh clone @ 506dd95 — suite 47 passed /
  0 failed, `selftest --full` 38 checks / 0 failed. Report:
  `docs/reports/2026-08-20-main-pc-setup.md`.

## Executed 2026-08-21 (from the main-pc session)

- ✅ **Website registered for multi-machine work**: `preiss-website` added to
  the registry and a website step added to `docs/bootstrap-new-machine.md`.
  Verified nothing is stranded locally: every branch's commits are on origin
  (`feature/fable-design-refinement` @ 7af1a24 == origin, working trees clean
  except pycache). Noted: main-pc's repo-local SSH deploy key
  (`.ssh-local/`, untracked) fails with a file-ACL error — pushes from
  main-pc currently work via HTTPS/GCM instead.

## Executed 2026-08-22 (from the main-pc session)

- ✅ **Claude system registered**: `claude-system` (workshop ops brain, repo
  `PREISS_WORKSHOP_CLAUDE_SYSTEM-`) added to registry, prose, and bootstrap.
  Verified fully pushed (main @ 27b3808 == origin); the only local diff was
  a Windows file-mode artifact, silenced via `core.fileMode false`.
- ✅ Full laptop-readiness check across projects: website, ScanPen, HelmCNC
  app, personal-os, claude-system all on origin with nothing stranded
  locally (HelmCNC's 12 dirty shop-PC files remain the known exception,
  tracked below). *Same day, from the shop: that exception is cleared — the
  files had landed 08-20; see the cnc-pc section.* KilnController confirmed
  still ideas-only — no code
  exists anywhere. Noted: main-pc also carries 0-byte husks `C:\Voiceover`,
  `C:\lbr` (same cleanup family as the cnc-pc ones).

## Executed 2026-08-22 (from the cnc-pc session)

- ✅ **The "12 dirty shop-PC files" exception is CLEARED** — they had already
  landed 2026-08-20 as the "five nights" commit (9c333e7) and were pushed.
  Today's shop-side sweep re-verified helmcnc-app end to end: master =
  origin, main tree and all four worktrees clean, every side-branch tip
  contained in origin. Site repo (`C:\HelmCNC.bak\GitHub\HelmCNC`) clean at
  "Dev release 1.0.90", main = origin.
- ✅ scanpen re-verified from the shop side: GitHub `master` @ 506dd95 still
  carries the current code (local head 3e90a27 unchanged since the
  fresh-start; the GitHub tree is exactly it minus `capture/`). The
  `C:\ScanPen` clone had no `origin` remote configured — now added.
  Untracked capture takes stay local by design (they are in the D: archive).
- ✅ Laptop paste-prompt written — top of docs/bootstrap-new-machine.md,
  covering all five projects; also handed to Tenis in chat.

## Executed 2026-08-26 (from the laptop session)

- ✅ **Laptop bootstrap is done and verified** — done 2026-08-22, re-checked
  today: all five projects sit at their registry roots and every local head
  equals origin. personal-os ff23c05, scanpen 506dd95, helmcnc-app 3674778,
  claude-system 27b3808, website `feature/fable-design-refinement` 7af1a24
  (49 commits ahead of an otherwise-empty `main`, unmerged by design).
  Tailscale up on the laptop; the shop PC reachable both by Claude-to-Claude
  Remote Control and by RDP.
- ✅ **Laptop global agent file created** — `~/.claude/CLAUDE.md` did not
  exist on this machine, although `docs/agent-system.md` names it as binding
  instruction file #1. It now carries the machine map, this laptop's project
  roots, the hard rules, the shop-PC contact procedure, and the not-on-PATH
  tool paths, so a session rooted anywhere on the laptop starts with the same
  world instead of only sessions rooted where its memory happens to live.

- ✅ **The helmcnc-app SelfTest fixture blocker is CLEARED.**
  `SelfTest/Fixtures/script_S.dxf` was never in git — the root `.gitignore`
  rule `Fixtures/` matched it at any depth — so fresh clones failed the suite
  build with MSB3030 even though HELMCNC_NOTES.md claimed it was committed.
  Force-added and pushed from the shop session (0d3b730, that file only, 15210
  bytes, sha256 b878e662…); `.gitignore` was left alone, since the rule still
  guards `Data/` and a tracked path overrides it. Verified on the laptop:
  fast-forward pull, byte-identical fixture, HelmCNC.exe + HelmSelfTest.exe
  both build, and `HelmSelfTest.exe offline` reports **2166 passed / 0
  failed** — the suite is green off-shop for the first time. The shop session
  also confirmed no other ignored-but-required file exists: HelmSelfTest.csproj
  has exactly one Content item. The build recipe it took to get there is now
  written into docs/bootstrap-new-machine.md instead of living in one
  session's memory.
- ✅ Shop PC notification settings checked while we were there —
  `agentPushNotifEnabled` and `inputNeededNotifEnabled` are **already true**;
  nothing needed changing. Phone delivery was unverified that day; it was
  proved the next morning — see the 08-27 section.

## Executed 2026-08-27 (from the laptop session)

- ✅ **The stall-notification path is VERIFIED end to end** — the fix for the
  08-26 incident, proved rather than assumed. Tenis left the shop PC, the shop
  session was put into an input-needed stall at 07:50 with nobody there, and
  his phone buzzed **while locked**; tapping through gave approval buttons on
  the phone and answering from it unblocked the session. He never walked to
  the shop. Two traps that make re-tests lie: the mobile push is **suppressed
  while the user is active at the terminal** (leave a session unattended ~3
  min before concluding anything — the first two attempts were false
  negatives), and `PushNotification` returns "Mobile push requested"
  regardless of what happens downstream, so its result string is not a
  delivery receipt. Nothing local records which channel an answer arrived on.
- ⚠ Still untested, narrowly: a real **tool-permission** prompt as opposed to
  a question. What was proved is the input-needed category, which carries the
  same actionable phone UI, so the permission path is likely fine — not
  proven. It could not be forced from the shop session; see the new open item
  below for why that is its own problem.
- ✅ **The 1.0.91 suite-red mystery is narrowed** (helmcnc-app a17df66). First
  off-shop run of the offline gate: **2166 passed / 0 failed** on the laptop,
  with the nine touch-router SAFETY checks that are red on cnc-pc firing for
  real. The machines differ in hardware, not source — laptop SM_DIGITIZER=197
  with 10 touch points, cnc-pc 0 — and without a digitizer the synthetic
  WM_POINTERDOWN transport never reaches the handlers, which is exactly the
  shop symptom (fires=0). This establishes the E-STOP routing is correct in
  the current code; it does NOT explain cnc-pc's console-green 2117/0 on
  08-16 on the same digitizer-less machine, so that stays unexplained. The
  cheap decisive test is recorded in HELMCNC_NOTES.md. Nothing promotes on
  this alone.


## Executed 2026-08-28 (from the laptop session)

- ❌ **RETRACTED, 2026-08-28 later: the "runtime artifact" conclusion below is
  WRONG and the item under it must not be acted on.** The 9 touch SAFETY
  failures are a REAL E-STOP defect, not an RDP artifact.
  `EmergencyTouchRouter.HitAndFire` (Controls/TouchInput.cs:591-593) compares a
  SIGNED `Environment.TickCount` against a 350 ms debounce with a -100000
  sentinel; past ~24.9 days uptime TickCount goes negative, the difference is
  about -1.14 billion, the press is swallowed permanently, and `en.Fire()`
  never runs. MainForm registers the real E-STOP/STOP buttons through that
  router, so after ~25 days uptime the on-screen E-STOP BREAK-THROUGH (firing
  while a jog holds the touch capture) silently dies. cnc-pc is in that state
  now (37 d uptime, TickCount measured -1137538843); the 08-16 green / 08-20
  red transition is exactly the wrap. Four failing checks call PreFilterMessage
  DIRECTLY in-process, which no message-delivery theory can explain.
  **DANGER THIS CREATED: a reboot resets TickCount, the 9 go green,
  release.ps1 stops refusing, and 1.0.91 would ship with a dead E-STOP
  break-through. A post-reboot green proves NOTHING.** The laptop's 2166/0 is
  not evidence either - at 4.7 days uptime it cannot reach the failing branch.
  Full detail and the fix idiom in helmcnc-app NOTES top entry (00c2548).
  Gate stays SHUT.

- ✅ **The 1.0.91 suite-red is proven a runtime artifact, not a code defect -
  the promote gate stays shut pending one console run.** The three files that
  generate the 9 touch SAFETY checks and implement the router they drive are
  byte-identical between the shop's failing-binary source and the laptop build
  that passes all 9; the 9 deliver via PostMessage through the app message pump
  into an IMessageFilter, so the failure is a pumped message not reaching the
  filter under the shop's RDP session, not an E-STOP logic bug. Shop-side
  read-only sweep ruled out hotfixes, Windows updates and device changes and
  falsified the digitizer idea. Full detail in helmcnc-app NOTES (f60b5c8). The
  one uncontrolled variable is RDP session 2 vs console session 1; on this
  Win10-client box a headless RDP connection can only land in its own session
  2, so the decisive console run needs a real console logon.
- ✅ **Console test STAGED, safely: no reboot / no tscon / no auto-logon.**
  Per Tenis's constraint (must not lose Tailscale+RDP access to the shop), both
  access-risky routes were declined. Instead an opt-in double-click script sits
  on the shop console desktop (Lenovo\Desktop\RUN-SUITE-CONSOLE-TEST.cmd +
  README): runs HelmSelfTest.exe offline, detects console-vs-RDP via
  `query session` (not the unreliable %SESSIONNAME%, which reads "Console" for
  RDP on this box), and writes a timestamped result file. The answer arrives the
  next time anyone logs into the shop console, or when Tenis is next there
  physically. Offline self-test confirmed to do no machine motion and need no
  KFLOP/KMotion.
- ✅ **Reboot-resilience of shop remote access, established read-only:**
  Tailscale service and RDP TermService are both StartType=Automatic and come up
  at boot before any login, so remote access survives a reboot with nobody
  logged in. Reachability is over the Tailscale interface, not the LAN 3389
  firewall rule (which showed 0 enabled rules - flagged, not a problem while
  Tailscale is the path).

## Executed 2026-09-07 (from the laptop session)

- ✅ **The employee exists, and it does not need a computer to be awake.**
  `docs/employee.md` is now the single agent identity - first moves, what it
  may do alone, what needs Tenis, hard rules, delegation, reporting - read by
  every surface, so behaviour changes by editing that file rather than a
  prompt. Three cloud routines are live on claude.ai/code/routines and run on
  subscription usage with every machine off: **weekday standup** 06:30 Mon-Fri,
  **website audit** 07:00 Wed, **week-in-review** 15:00 Fri (UTC = Iceland).
  This closes step 4 of `docs/agent-system.md`. Before today the account had
  zero routines, zero scheduled tasks and zero API triggers - every action
  needed Tenis's prompt.
- ⚠ **Routines silently inherit every claude.ai connector.** All three came
  back from the API carrying Gmail, Google Calendar and Claude Code Remote,
  unrequested; a routine may use every tool of an attached connector, writes
  included, without asking, in an unattended run. That is mail-send authority
  on a job needing only git. All three were stripped
  (`clear_mcp_connections`), verified back as `mcp_connections: []`. **Check
  this on every routine created from any surface.**
- ✅ **Phase 1 prepared for main-pc, nothing left to design.**
  `docs/employee-setup-main-pc.md` plus `scripts/employee-preflight.ps1`,
  `scripts/employee-session.ps1`, `scripts/install-employee-autostart.ps1` -
  Telegram channel into an always-on session rooted here, autostarted at
  logon like the shop PC's remote-control task. Scripts parse-checked;
  preflight executed on the laptop - but the session launch line itself was
  never run, and could not have started (found and fixed 2026-09-17, below).
  Note for anyone writing more of them:
  PowerShell 5.1 reads `.ps1` as ANSI, so a UTF-8 em-dash becomes a string
  terminator error - keep scripts ASCII.
- ❌ **HelmCNC support-report triage was deliberately NOT made a routine.**
  The reports sit behind an admin endpoint whose token lives in the Signing
  folder; a cloud sandbox has neither the token nor the network permission,
  and this repo will never carry it. That job stays on main-pc or cnc-pc.
- Assessment, findings and the WhatsApp/voice picture:
  `docs/reports/2026-09-07-employee-agent.md`.

## Executed 2026-09-17 (from the laptop session)

- ✅ **main-pc is the always-on host; the laptop runs nothing unattended.**
  Tenis put main-pc on the tailnet (100.66.146.24, reached via DERP relay, no
  direct path). Tailnet names are now `cnc`, `main-pc`, `laptop`, `phone`;
  `desktop-a60v7p2` no longer resolves, so RDP to the shop is `mstsc /v:cnc`.
- ✅ **Inventory of what ran continuously on the laptop** - less than it
  looked. The three cloud routines need no machine and stay in the cloud
  (standup fired 06:39 today, succeeded). No desktop scheduled tasks, no
  session crons. Two machine-bound pieces, both dead: the `Claude Relay`
  logon task (`claude --remote-control laptop-relay`) had failed at every
  logon since the app updated past the hard-coded `claude-code\2.1.237` path
  ("The system cannot find the path specified"); and the Telegram plugin
  was enabled with no bot token, so it failed to connect in every session.
  Both retired on the laptop (task disabled, plugin disabled - reversible).
- ❌→✅ **`employee-session.ps1` could never have started the employee.**
  `--channels` is variadic, so the brief was swallowed as a second channel
  and the CLI exits: `--channels entries must be tagged`. Reproduced in print
  mode, fixed with `--` before the prompt, fix verified (`PONG`, exit 0). The
  line also lacked `--remote-control`, so the documented "approve prompts
  from the phone" was impossible - it now starts as RC session `employee`.
  It refuses to start without a bot token, and its `git pull` no longer
  reads as failed under PowerShell 5.1's stderr handling.
- ✅ **main-pc bootstrap scripted: `scripts/main-pc-always-on.ps1`.** One run
  at main-pc registers `PreissRelay` (logon task, `relay-session.ps1` keeps
  `claude --remote-control main-pc` alive and restarts it), installs Bun and
  the Telegram plugin if missing, and reports sleep settings. claude.exe is
  resolved at every launch by `scripts/resolve-claude.ps1` (PATH,
  `~\.local\bin`, newest CLI inside the Claude app) - the laptop relay died of
  a baked-in path. All six scripts parse clean and are pure ASCII; relay
  dry-run, resolver fallback and preflight verified on the laptop. The
  bootstrap itself is untested until main-pc runs it.
- **Why it cannot be done from the laptop alone:** main-pc exposes no remote
  shell over Tailscale - 22, 3389, 5985 and 5986 closed; only 135/139/445
  (RPC/SMB) open, which would need Tenis's password and weakened remote UAC.
  Not used.

## Executed 2026-09-18 (from the laptop session; Tenis was at the shop PC, believed to be main-pc)

- ✅ **The Telegram plugin must not be enabled user-wide.** Its server polls
  the bot in every session that loads it, channel flag or not, and Telegram
  allows one poller per bot - the relay or any desktop session would have
  fought the employee for messages (409, lost DMs). Verified on the laptop:
  `--channels` alone does NOT load a disabled plugin; `--settings
  scripts/employee-settings.json` does. The bootstrap now disables it
  user-wide, the employee enables it for itself, the preflight flags it.
- ✅ **CRLF would corrupt the token.** The plugin splits `.env` on LF only,
  so a Windows line ending leaves `\r` in the token. New
  `scripts/employee-set-token.ps1` writes it without a newline - and keeps
  the token out of every transcript, which `/telegram:configure <token>`
  does not.
- ✅ **First bootstrap run on main-pc, from Tenis's screenshot:** Bun
  installed, Telegram plugin installed and disabled user-wide, sleep and
  hibernate on AC both "never". The token prompt failed: Ctrl+V in the
  console types one control character (0x16, a single `*`), which the
  script rejected - the employee was skipped. Fixed: the token now goes into
  a small dialog (masked box, Ctrl+V and a clipboard button). Unknown from
  the screenshot whether the relay task registered; `main-pc` is not in
  ListAgents, so the relay is not connected - most likely its minimized
  window sits on a login or trust question. The bootstrap now logs relay
  starts/exits to `~\.claude\relay-main-pc.log`, prints the tail, and brings
  the relay window to the front at the end.

- ❌ **The bootstrap was run on the shop PC, not on main-pc.** Tenis said
  "I'm at the main pc"; the relay's own inspection reported
  `DESKTOP-A60V7P2`, user `Lenovo` - the CNC appliance. So Bun (~180 MB),
  the Telegram plugin, the bot token and the employee (auto mode) landed on
  the machine whose rule is "HelmCNC only, no installs", and its relay
  registered under the name `main-pc`. The scripts had no hostname guard -
  that is the root cause, and it is fixed: `scripts/machine-role.ps1` maps
  hostnames to the tailnet names, every installer and the employee refuse
  on `DESKTOP-A60V7P2`, and a relay is named from the hostname so a mis-run
  can never impersonate another machine again. Verified with simulated
  hostnames on the laptop.
- ⚠ **Containment from the laptop was blocked.** The shop relay runs in
  auto mode; its classifier denied the stop/disable block, and the session
  rightly refused to split it (permission laundering). Nothing on the shop
  PC changed until Tenis ran the undo himself (below). A later attempt to
  give the undo script a `-Yes` switch so a relay could run it unattended
  was denied by the laptop session's own classifier - correctly: skipping
  a typed confirmation for deletions is the gate itself.
- ✅ **Design change: a relay MAY run on the shop PC, the employee may not.**
  The shop PC's old `claude --remote-control` autostart was not running any
  more (no `desktop-a60v7p2-*` row online while Tenis was logged in), so a
  relay there is the laptop's only Claude path to the CNC PC - the
  documented preferred route. `relay-session.ps1` keeps permission prompts
  on the shop PC (approve at claude.ai/code) and uses auto mode only on the
  dev machines. Undo script `scripts/cnc-pc-undo-always-on.ps1`: guarded to
  that hostname, prints its plan, waits for a typed YES, then stops the
  employee, removes token/plugin/marketplace clone/Bun + PATH entry, and
  re-registers the relay as `cnc` with prompts (`-RemoveRelay` to drop it).
  Dry-run verified on the laptop.
- ✅ **Undone by Tenis at the shop PC** (his screenshot, ~11:10 shop clock,
  which runs two hours ahead of Iceland): PreissEmployee unregistered,
  Telegram state removed token included, plugin and marketplace
  uninstalled, Bun and its user PATH entry removed, PreissRelay
  re-registered as `cnc` with permission prompts and running. Not touched:
  C:\HelmCNC, C:\HelmCNC.bak, KMotion, backups, Signing. Oddity, noted not
  chased: C: free went 18.16 -> 18.19 GB although ~200 MB was removed.
  `cnc` had not yet appeared in ListAgents two minutes later; watch it.
- ✅ **Phase 1 is LIVE on PREISSWORKSHOP (2026-09-18, late morning).** The
  bootstrap ran there once the paste mix-up was sorted (the undo line was
  pasted twice on main-pc; its guard refused both times, as designed). What
  it took after that, all at the keyboard: the CLI had no claude.ai login
  for Remote Control ("Not logged in" in the status bar although API calls
  worked), so `/login` in the relay window, then `/exit` - the relay loop
  brought a fresh session that registered as `main-pc`. The employee,
  started before that login, sat on the auto-mode setup question nobody
  saw; once approved it began a duplicate recon and had no Telegram server
  process; `Esc`, `/exit` and the bootstrap paste restarted it (the launcher
  now loops like the relay, b988cd1). It registered as `employee`, the bot
  answered with a pairing code, and Tenis typed `/telegram:access pair` and
  `policy allowlist` himself - the employee refused the code relayed from
  the laptop session, correctly: pairing decides who may drive an auto-mode
  session. Reported by the employee: one sender allowed, policy allowlist,
  pending empty, first brief delivered to his phone.
- ✅ **Auto-mode setup saved on main-pc, with provenance rules** (Tenis's
  answers): pricing and supplier data -> him plus the quoted client, supplier
  prices and margins never; client files -> that client and him only;
  trading material (bots, API-keys file) -> no one, ever, no agent touches
  the broker API; raw EXIF/GPS photos -> public only after stripping. The
  recon found a trading-bots API-keys file on main-pc: same "never" bucket
  as the Signing folder.
- ⚠ **Open from today:** the shop PC's `cnc` relay never appeared in
  ListAgents (its window may hold a first-run question; check at the shop),
  and a peer probe of the idle row `Dispatch background conversation` went
  unanswered. Sleep on AC is "never" on both PCs.

## Found 2026-09-18 (from the employee session - which is on cnc-pc)

The employee's first act, unprompted, was to report which machine it was
on - and it pushed that straight to `main` from the CNC PC in auto mode,
which says something about that mode's gating. Its findings:

- ❌ **Confirms the item above from the inside:** `hostname` =
  DESKTOP-A60V7P2, `cnc` in `tailscale status`; Bun installed 10:24,
  `PreissRelay` (named `main-pc`) and `PreissEmployee` registered and
  running, bot token file present. The bot allows one poller, so main-pc's
  employee cannot go live until this one stops - the undo script does that
  first.
- ⚠ **RESOLVED for week-in-review, still open for website audit.** The
  15:00 week-in-review fired today and produced this report and its own
  section below — the routine works, so today's earlier read (a fire
  skipped before a session exists, leaving no trace) was the right theory
  for a first-run gap, not evidence of a broken routine. Website audit
  (Wed 07:00) is unverified from this session (no access to
  claude.ai/code/routines' run list from here) — next due 09-23, worth one
  check then.
- ⚠ **1.0.91 and 1.0.92 are shipped; this tracker still said otherwise.**
  Verified in `C:\HelmCNC.bak`: tags `stable/v1.0.91` and `stable/v1.0.92`
  exist; master 27d0286 (09-04) gave `promote.ps1` a `-Go "<who, where,
  when>"` switch that skips the typed gate. Standup PR #2 carries the
  correction and is unmerged. Open for Tenis: was each promote his go, and
  did the customer receive it (standup found no `installer/news.items`
  entry for either).

## Executed 2026-09-18 (from the employee session on main-pc — first live run)

- ✅ **The employee is LIVE on main-pc.** Tenis ran the one-paste bootstrap
  at PREISSWORKSHOP ~09:24; verified from inside: hostname PREISSWORKSHOP,
  user tenis, scheduled tasks `PreissRelay` and `PreissEmployee` both
  Running, relay log healthy (clean exit 10:11, auto-restarted 30 s later as
  RC session `main-pc`, permission mode auto), Telegram channel reachable
  from the phone, tailnet resolving all four names (main-pc / cnc / laptop /
  phone). The 🔒 "one paste left at main-pc" item is CLOSED; only the
  account signups below remain of it. Phase 1 of `docs/employee.md` is no
  longer "scripted, not live" — it is running.
- ✅ **Both standup PRs are closed, neither merged.** Content-diff
  `main...pr1` was empty (the button-sweep correction landed 09-07) — closed
  same day. PR #2's ship correction was condensed into the Found 2026-09-18
  section above, with its one missing detail folded in here:
  **1.0.92 carries a toolpath fix — view re-anchors to the new WCS mid-run,
  Tom's G54→G55 shift (helmcnc-app 030c80c), tagged at d33107f "Dev release
  1.0.92", 2026-09-02.** Closed by the 09-18 week-in-review routine
  (content-diff against `main` was a no-op by then).
- ⚠ **gh is not authenticated on main-pc** — `gh` exits asking for login,
  while git push works via GCM. Until fixed the employee cannot file the
  machine-queue GitHub issues its standing duties require, nor close PRs.
  No credential store was touched (hard rule). Needs one interactive
  `gh auth login` by Tenis at this machine — or typed into the employee
  session as `! gh auth login --hostname github.com --git-protocol https --web`.
- ✅ **Week-in-review routine fired for the first time, 09-18 15:00 UTC**
  (this session, cloud sandbox, no machine). Produced
  `docs/reports/2026-09-18-week-in-review.md` and the entries in this file
  dated from that session. `mcp_connections: []` still true (checked by this
  session's own tool list — no Gmail/Calendar/Remote Control attached).
  Website audit remains unverified (next due 09-23).

## Second sitting 2026-09-18 ~10:45 (employee on main-pc, hostname verified)

- ✅ **Outgoing mail is ON, and not through Resend.** Website `main` today
  (e8b2547 → 6de2e2a): Tenis bought Workers Paid, `preissworkshop.is` is
  onboarded for Cloudflare Email Sending, the `preiss-mail` Worker is
  deployed and bound to Pages as `MAIL`; Gmail send-as
  `tenis@preissworkshop.is` verified SPF/DKIM/DMARC PASS, DMARC `p=reject`.
  The Resend signup this tracker was waiting on is obsolete;
  `docs/employee.md` and setup step 7 rewritten to match. One owner step
  left there: Admin → Outbox → *Send what is waiting* (seven test mails
  since 09-07).
- ⚠ **Standup 06:39 (succeeded) — two website findings not reported
  before.** (1) 8 of the 9 commits that reached website `main` on 09-17
  are authored "Claude" straight onto `main`, 06:47–07:31, no branch or PR;
  `AGENT_WORKFLOW.md` says never work directly on main unless instructed.
  Verified in a scratch clone. If Tenis was driving that session, this is
  fine and the rule in that file should say so; if not, it is a gate that
  did not hold. (2) Website `PROGRESS.md` has no entry after 09-06 — it
  misses the CRM merge and everything since. The registry's stale
  "feat/projects-board 1 ahead" line is corrected.
- ✅ **main-pc's website checkout is current** (was 2.5 months stale: SSH
  origin with a repo-local key that fails its ACL, `origin/main` at
  519c1b5 from 07-03). On Tenis's word ("get the main PC up to date",
  12:12): origin switched to the HTTPS URL (old:
  `git@github.com:PreissWorkshop/preiss-workshop-website.git`;
  `core.sshCommand` left in place, now unused), fetched, main worktree
  switched from `feature/site-redesign-admin-2026-07` to `main` and
  fast-forwarded to fb7594f. Tree was clean before and after. Build
  verified: 114 pages, 56 sitemap pairs. The three sibling worktrees were
  not touched.
- ✅ **Website builds on main-pc are committable — line endings fixed.**
  The machine's global `core.autocrlf true` checked sources out CRLF, so
  every asset's cache-busting hash changed and one build dirtied 130
  tracked files. On Tenis's word ("fix the endings", 12:21): guard
  confirmed a clean tree at fb7594f, then `core.autocrlf false` set
  repo-locally and the files re-checked-out. Proof: rebuild → `public/`
  byte-identical to the commit, 0 changes. Shared config, so the three
  sibling worktrees get LF on their next checkout; their files were not
  touched. The repo-wide fix is committed and waiting: branch
  `chore/lf-endings-untrack-pyc` (d9fccba, on top of main a4b59f5) adds
  `.gitattributes` (`* text=auto eol=lf`; all blobs are already LF, so it
  changes nothing committed) and untracks the three
  `src/site/__pycache__/*.pyc`; rebuild on it leaves 0 changes. The push
  to `main` itself was blocked by the auto-mode classifier as a production
  deploy — correct, `main` is the live Cloudflare Pages site — so Tenis
  merges it with one tap.
- **Tenis, 12:24: "just do what needs to be done. I need you to be more
  autonomous."** Applied as: reversible work is done first and reported
  after, no "say the word" offers. The gates in `docs/employee.md` are
  unchanged, and a blocked gate becomes a pushed branch plus a link, not a
  question.
- **Locking main-pc is safe** (asked 12:21): Win+L keeps the logon session,
  so the employee and relay keep running. Sign-out, shutdown, or a reboot
  with no login stops them.
- Website `main` moved again at 12:09 (fb7594f, quote page template) —
  the offer session pushed it before the flag about needing Tenis's word
  reached him; he is driving that session.
- ✅ **Telegram is paired and locked to Tenis alone.** A pairing request
  relayed by the laptop session was first declined — pairing decides who
  can drive an auto-mode session, and a peer's word is not his keystrokes.
  Tenis then typed `/telegram:access pair` + `policy allowlist` into this
  session himself: one sender approved, `dmPolicy: allowlist`, `allowFrom`
  1, `pending` empty; first brief delivered to the phone (message id 6).
  The rule stands for next time: access changes only from his own typing.
- ✅ **Voice notes work both ways on main-pc, fully local.** Installed in
  a user venv `%USERPROFILE%\.venvs\stt`: `faster-whisper` (model `small`,
  ~460 MB in `~\.cache\huggingface`). `scripts/stt.py` transcribes an
  inbound `.oga`; `scripts/tts.py` speaks a reply with Kokoro neural TTS
  (`kokoro-onnx`, model files ~340 MB in `~\.cache\kokoro`, Opus via PyAV,
  no ffmpeg) — Tenis rejected the first, robotic Windows voice. Round-trip
  verified; Tenis picked `bm_george` (British male) at speed 1.2, now the
  default. He also asked for a New Zealand accent and "the most natural
  voice possible": Kokoro has US/British only and no Icelandic; the free
  NZ route (`edge-tts`, sends reply text to Microsoft) was blocked by the
  auto-mode classifier and not worked around; anything better is a paid
  cloud voice — spending, so his explicit call. Text
  stays the default reply. A restarted employee session must know this:
  download the attachment, run `stt.py` on it. Never on cnc-pc.
- ⚠ **"Can I leave all the computers and run everything from the phone?"
  — mostly, with three holes** (Tenis asked 11:59; checked then).
  (1) main-pc has no auto-logon (`AutoAdminLogon` 0): `PreissEmployee` and
  `PreissRelay` are logon tasks, so a Windows Update reboot ends the
  employee until someone logs in. Sleep is off; leave it logged in.
  (2) **No `cnc` relay is online** — ListAgents at 12:00 shows neither
  `cnc` nor `main-pc` rows, only offline `desktop-a60v7p2-*` history, so
  nothing at the shop PC can be reached from here until the relay is
  started at its keyboard. `[UNVERIFIED — needs check]`: whether the
  main-pc relay is really connected, since its task reads Running but no
  `main-pc` row is listed. (3) Classifier blocks and the missing `gh`
  login still need him at claude.ai/code or a keyboard.
- **Client offer system (website), as reported 12:10 by its own session —
  not verified here:** mail live end to end (main @ 377defe); quotes
  Q-2026-0007/0008 for Völundur built in the admin and test-sent to Tenis,
  SPF/DKIM/DMARC pass; quote-page polish on `feat/quote-page-polish`,
  local and unpushed, tests 61/61 pending a rerun. 🔒 Tenis: put
  Völundur's real e-mail on the client record and press send on
  Q-2026-0008 himself; OK the deletion of test project V-2026-0003; and
  that session intends to push the template to `main` — his word needed,
  flagged to him on Telegram.
- ✅ main-pc's HelmCNC clone fast-forwarded 0a0b493 (08-10) → 27d0286
  (09-04), clean, = origin. **HelmCNC builds and tests on main-pc**
  (subagent run, ~12:40): `build.cmd ReleaseNew` + the framework-MSBuild
  suite call, then `HelmSelfTest.exe offline` → `RESULT: 2179 passed, 0
  failed`, 47 s, all 12 `tickwrap` checks present, tree clean afterwards,
  ~94 MB in ignored paths, nothing system-wide. Uptime 4.5 d, so this is
  not high-uptime evidence. Count is 2 below cnc-pc's 2181 (08-31) —
  unexplained, not chased. The recipe block in
  `docs/bootstrap-new-machine.md` had its backslashes eaten into control
  characters; rewritten with the commands that worked. ScanPen and
  claude-system clones equal origin; the website clone is fixed (above).
- ⏳ **New website feature asked by voice 12:59: measurement appointments
  on the client project page.** Accepted quote → Tenis offers free slots →
  client picks one on the page and gives the address if it is missing →
  entry in Tenis's calendar with address → reminders → an "on my way" view
  with live position, ETA and a late notice. Employee is doing it on
  main-pc, branch `feat/measurement-appointments`, never `main`; the
  offer-system session (laptop) confirmed it has nothing in flight and
  does not touch `src/api/portal.js`. Plan: `APPOINTMENTS-PLAN.md` in the
  website repo, three phases — (1) booking: owner offers times in the
  admin, client picks on the script-free page by plain form POST, both
  get a mail with an `.ics` (calendar with address, no Google link, no
  key); (2) reminders via a key-protected cron endpoint; (3) "on my way"
  map/ETA — amends WORKSHOP-OS's "no continuous tracking" decision
  (driver-initiated, one trip, self-ending), live traffic needs a paid
  map API, SMS does not exist: all three are 🔒 Tenis when phase 3
  starts. **Phase 1 is built and on a preview (14:05), not merged:**
  branch `feat/measurement-appointments` @ 4882e8d, 15 files, new module
  `src/api/appointments.js` + table `wo_appointments` (in the backup
  list), admin card "Measurement visit", client form POST
  `/api/p/<token>/book` (page still script-free, CSP gained only
  `form-action 'self'`), `.ics` PUBLISH/CANCEL. Tests 78 passed / 0
  failed under Node (61 before, same runner) plus an end-to-end run
  against in-memory SQLite — as reported by the implementing subagent;
  the employee read the route and `book()` and found them sound. Preview
  verified up and carrying the new card:
  `https://feat-measurement-appointment.preiss-workshop-website.pages.dev`
  (Cloudflare cuts the alias to 28 chars). NOT verified: the admin card
  in a real browser, how Gmail/phone mail present the `.ics`, whether the
  preview is bound to the live D1 and live mail sender (Tenis told to
  treat it as live). Known: a booking mail re-sent from the outbox loses
  its attachment (pre-existing outbox limit); `book()` does not itself
  refuse on an archived project. 🔒 Tenis: try it once per TODO-OWNER.md,
  review the Icelandic, then say merge.
- ⏳ **The laptop disconnected 13:30; the employee took over the offer
  system's code work.** Nothing lost: that session had confirmed
  everything pushed (website main @ 31b71a7), GitHub agrees, all laptop
  Remote Control sessions now read offline. In flight there, per Tenis's
  screenshot: (1) client branding — dark site-header band + logo on the
  quote page, job page and both client mails, print-safe: never pushed,
  restarted 13:40 on main-pc as branch `feat/client-branding` (subagent;
  works in the same clone, so `feat/measurement-appointments` must not be
  touched meanwhile). (2) Q-2026-0008 repricing (hours −25 %, material
  unchanged, VAT 24 %) plus a final test send — admin data, not code; the
  employee has no admin login and does not look for one; it offered to
  compute the lines from numbers Tenis sends, he types them in. His
  internal cost structure stays out of every repo. 13:45: Tenis sent the
  costing over Telegram and asked about a material/labour split and a
  visible 25 % discount; the employee advised yes to both (visible
  discount with a reason; two subtotals, not hours × rate; the VAT-refund
  point marked unverified) and returned the client-facing lines plus a
  margin warning. No figures are recorded here on purpose. 🔒 Tenis:
  choose the discount %, enter the lines in the admin, send the quote.
- ✅ **Client branding built, not merged** (14:20): website branch
  `feat/client-branding` @ 2242301 — `src/api/brand.js`, dark header band
  + logo on the quote page, job page and all client mails, print rules;
  tests 64 passed / 0 failed (61 baseline), as reported by the subagent;
  the employee looked at the phone-width renders and sent them to Tenis.
  The mail logo loads from production, so it 404s until merged.
- ❌ **The employee's "try the booking on the preview" advice was wrong.**
  Cloudflare previews of this project have no D1, login or mail bound —
  verified 14:25: preview `/api/admin/ping` reports `db:false,
  auth:false, mail:false`, `/api/p/<token>` answers 503. Corrected to
  Tenis on Telegram. The try-out has to happen live after a merge (the
  booking is invisible to clients until times are offered) or after he
  binds D1 to the Preview environment.
- ✅ **One branch carries all three, ready to merge:** website
  `release/2026-09-18-client-flow` @ febd933 on main 31b71a7 — line
  endings + branding + booking; one conflict (`src/api/portal.js`, both
  sides kept); appointment mails adopt the brand band; an open offer does
  not print, a booked visit does; TODO-OWNER try-out rewritten for the
  live admin. Observed by the subagent: `test_crm` 82 passed / 0 failed,
  `test_quote` 8 / 0, Build OK 114 pages with `public/` byte-identical.
  The employee checked the 390 px render. Static preview:
  `https://release-2026-09-18-client-fl.preiss-workshop-website.pages.dev`.
  Still unverified until the live try-out: the admin card in a browser,
  `.ics` handling in Gmail/phone mail. 🔒 Tenis, link sent 14:00:
  https://github.com/PreissWorkshop/preiss-workshop-website/compare/main...release/2026-09-18-client-flow
  → create PR → merge, then the TODO-OWNER try-out.
- ✅ **Merged by Tenis and live, 14:05:** website PR #2, `main` @ 04b5564
  contains febd933. Verified on preissworkshop.is: home 200, the live
  `admin/wo.js` carries `appointment-offer`, the mail logo PNG answers
  200, `/api/admin/ping` reports db/auth/mail/github/turnstile all true.
  Branches `chore/lf-endings-untrack-pyc`, `feat/client-branding`,
  `feat/measurement-appointments`, `release/2026-09-18-client-flow` (and
  the laptop's `feat/quote-page-polish`) are now dead — deletion is 🔒
  Tenis. main-pc's clone is back on `main` @ 04b5564, clean. 🔒 Tenis: the live try-out (TODO-OWNER.md) —
  `.ics` behaviour on the phone, logo in the mails, the Icelandic. Phase
  2 (reminders) starts after his feedback.
- PR #1 was already closed by the time of writing (not via this session);
  PR #2 was closed by the 09-18 week-in-review routine, below. Local
  `origin/pr1`/`pr2` refs a previous session made were pruned by fetch.

## Executed 2026-09-18 (from the week-in-review cloud routine, 15:00 UTC)

First successful run of the routine (see corrections folded into the
09-18 sections above) — full account in
`docs/reports/2026-09-18-week-in-review.md`. Summary:

- ✅ **The week's git history confirmed across all four repos**, all
  branches, both shallow clones unshallowed first. HelmCNC and ScanPen: zero
  commits in 7 days (last real work 09-04 and 08-16 respectively — both
  outside the window, not a regression, just a quiet week for both). No
  stray branches ahead of `master`/`main` carrying unmerged work in either.
  personal-os and the website: both dominated by 09-17/09-18 activity
  already narrated above.
- ✅ **ScanPen suite run for real** (fresh `pip install`, nothing cached):
  pytest 46/47, `selftest --full` 37/38 — same one failure both times
  (`sweep-artifacts-verified`, `spot_recompute_max_deviation` 1.53794e-07 mm
  vs the `< 1e-07 mm` gate), folded into the tolerance item below. Working
  tree left clean (`results/capability_report.json` reverted).
- ✅ **Website build run for real**: `python src/site/build.py` →
  114 pages, 56 sitemap pairs, matching the number already on record.
  Working tree left clean.
- ✅ **PR #2 closed** via the GitHub API (content-diff against `main` was a
  no-op) — see the corrected 09-18 entry above.
- ❌ **Could not run**: HelmCNC's suite (no Windows/.NET in this sandbox)
  and the website's Node test harness (`test_crm`/`test_quote` numbers
  stay as the implementing session reported them, not re-verified here).

## Third stretch 2026-09-18 14:05–15:35 (employee on main-pc)

- ❌ **The employee went silent for ~50 minutes, and that is its fault.**
  Tenis asked at 14:04 for a final test of the updated quote; that needs
  the live admin, the employee had no login, tried the Chrome skill, the
  tool call was declined at the main-pc terminal, and it stopped and
  waited without a word on Telegram until he asked "are you stuck?" at
  14:33. His words: "never again hang like that without a warning!" Rule
  now in the employee's memory: any block gets a Telegram line within a
  minute, then work continues on whatever does not depend on it.
- ✅ **Q-2026-0008 updated in the live admin and test-sent to Tenis only**
  (15:27), on his explicit instruction. Material/labour split per room and
  a visible discount equal to 25 % of labour; totals read back from the
  live database and match the employee's arithmetic exactly. Quote set
  back to `draft`, then sent with the recipient pinned to
  `tenis@preissworkshop.com`; the client record still holds that
  placeholder, so nothing can reach the client. Re-accepting reuses
  project V-2026-0005. Figures are deliberately not recorded here. Open:
  the page labels the discount only "Afsláttur", not "25 % af vinnu".
- ⚠ **Tenis sent the live admin password over Telegram** so the employee
  could do the above. It was used once, from an environment variable, to
  obtain a session cookie kept in the session scratchpad; it is in no
  file, repo or report — but it is in the Telegram chat history and in
  this session's transcript. 🔒 Tenis: change `ADMIN_PASSWORD` in the
  Pages project when today's quote work is done. Better for next time: a
  separate long-lived admin credential for the employee, or Cloudflare
  Access, so his own password never travels.
- ✅ **Week-in-review routine fired for the first time** (15:06, run
  succeeded): PR #3 → fast-forwarded into `main` by the employee after
  reading the diff (b72a05b; tracker corrections, first
  `docs/reports/2026-09-18-week-in-review.md`, ScanPen suite run for real
  in the sandbox: pytest 46/47, selftest 37/38, the known FP-dust miss at a
  third value). It also closed PR #2. Note for the connector audit: the
  routine reads `mcp_connections: []` yet had working GitHub MCP tools
  with write access (commented on and closed a PR, opened PR #3, sent a
  push notification). That is within its prompt ("open a pull request")
  but wider than "git only" — the environment, not the connector list,
  grants it. Worth one look at the routine environment's GitHub scope.

- ✅ **Q-2026-0008 is with the client (15:56).** Tenis rehearsed the
  accept on the test copy, then instructed the send at the main-pc
  terminal with the client's own request mail as the source for name,
  e-mail and phone. Done through the admin API, in order: client record
  #2 given the real e-mail and phone, quote returned to `draft`, recipient
  and totals read back, then sent — the mail path answered `sent`.
  Project V-2026-0005 was checked first and carries no test residue; it
  is reused on acceptance. The admin session cookie was deleted
  afterwards. Watch for: the accept/decline mail, or the view counter
  rising above the ~27 test views. The new domain may land in the
  client's Spam — Tenis was told to text him.

## Fourth sitting 2026-09-19 ~09:40 (employee on main-pc, hostname verified)

- ❌ **main-pc rebooted itself 09-18 22:10 and the employee was down for
  11.5 hours.** Cause, from the System event log: Windows Update
  (`MoUsoCoreWorker.exe`, then `TrustedInstaller.exe` twice) installing
  security update KB5129195 - three planned restarts, 22:10-22:12. Not a
  crash, not power. Active hours were 04:00-17:00 and no update policy of
  any kind was set, so 22:10 was fair game. The PreissEmployee/PreissRelay
  tasks fire at logon and there is no auto-logon, so nothing came back
  until Tenis logged on at 09:37.
- ✅ **Fix applied 09:40** with `scripts/no-auto-reboot.ps1` (elevated, Tenis
  approved the UAC prompt; `-Undo` reverts): active hours 08:00-02:00 (18 h
  is Windows' maximum), smart active hours off, restart notifications on,
  plus policy keys AUOptions=2 (notify before download) and
  NoAutoRebootWithLoggedOnUsers=1. Registry read-back matches.
- ⚠ **`[UNVERIFIED - needs check]` whether Windows 11 Home honours the
  policy keys.** The update agent still reports NotificationLevel 4 (fully
  automatic) after the change; that API is unreliable on Windows 11, so
  this proves nothing either way. Check: Settings > Windows Update >
  Advanced options should show "some settings are managed by your
  organisation", and the next Patch Tuesday (2026-10-13) should ask before
  installing. What IS certain: a forced restart can now only land between
  02:00 and 08:00.
- Trade-off taken: if the policy holds, security updates wait for Tenis's
  click. The employee reminds him when one is pending.

- **Routines since the last sitting: none ran.** 09-19 is a Saturday (standup
  is Mon-Fri); the Friday week-in-review is already merged and seen.
- ⏳ **Two cloud-session branches sit unmerged, no pull request on either**
  (checked by `git ls-remote`; `gh` is still not logged in on main-pc):
  `claude/quick-response-delegating-agent-2ox6b1` (09-18 15:55 - `frontdesk/`,
  a fast Python process that would own the Telegram bot and hand work to
  the employee; 27 files, needs an API key, so it spends money) and
  `claude/icelandic-language-skill-77oinn` (09-19 08:16 - an Icelandic
  writing skill plus report; rules marked [K] are unverified by a native
  reader). Both edit `docs/employee.md` and this file, so whichever merges
  second needs a hand merge. Neither changes behaviour until merged.

- ⏳ **Surveillance app: Tenis wants the phone to see the camera with every
  PC off (09-19).** *Same day, from the shop: the app is located and
  registered - see the cnc-pc section below. The route question stands.*
  The app's code was NOT found: not in the registry, not
  on main-pc's disk, not running here, no PreissWorkshop repo under the
  obvious names; the only trace is `surveillance/notify.py`, named by the
  front-desk branch. Read-only look at the LAN from main-pc: the camera is
  192.168.8.13, Dahua family by MAC, RTSP 554 and Dahua port 37777 open;
  the router at 192.168.8.1 looks like a Huawei mobile-broadband box
  `[UNVERIFIED - login page only]`, which cannot run Tailscale and is
  probably behind carrier NAT, so port forwarding is out. Two routes that
  need no PC: (1) the camera's own P2P cloud with the DMSS or Imou Life
  phone app - free, works today, video relays through the vendor's
  servers; (2) a small always-on box (Raspberry Pi class, about 5 W) on
  the router running Tailscale plus go2rtc - private, costs hardware
  money, and is where the app's motion alerts would move to. Nothing was
  logged into and nothing was changed.

- ✅ **Surveillance is cloned and working on main-pc** (09-19 ~11:00), at
  `C:\Projects\Surveillance\repo`: `.venv` built, recorder code imports.
  Toolchain installed user-scope: Temurin 17 in `~\tools`, Android
  build-tools 34.
- ✅ **Phone app 1.1 built and pushed** (Surveillance- 459fe21): when the
  recorder does not answer, the app plays the camera's own RTSP stream -
  no PC involved. Password typed on the phone, kept there. **Compiles and
  packages; not yet run on a phone.** The APK went to Tenis by Telegram. It
  is signed with a new main-pc key, so the phone's 1.0 must be uninstalled
  once first.
- ✅ **1.1 is installed on Tenis's phone** (11:09, his screenshots): the
  new error screen with the three buttons shows, Tailscale connected, all
  tailnet nodes but the laptop online. The recorder answers nowhere, as
  expected. The direct view itself is still untried - he was on 5G, and
  it needs the shop wifi.
- ⚠ **What 1.1 does not cover**: phone away from the shop AND every PC
  off. The router looks like a Huawei mobile-broadband box `[UNVERIFIED -
  login page only]` - no Tailscale on it, no port forwarding - so a device
  inside the shop must stay on. Full account: Surveillance-
  `docs/no-pc.md`. Nothing on the camera or router was logged into or
  changed.

- ⏸ **Surveillance paused by Tenis 09-19 ~11:30**, as it stands: setup
  prepared, one double-click left (see Waiting on Tenis).
- ✅ **Website audit 09-19, 13:10-13:35 UTC, on Tenis's instruction** (public
  site, admin, crew app, server). Branch `audit/2026-09-19-site-admin-crew`
  off `main` @ a71a66c, pushed @ a7ff5ed (13:43), **not merged, not live**.
  Five read-only auditors in parallel, then fixes in 20 commits. Observed on
  the final state: build reproduces with no diff, `test_crm.html` 83/83,
  `test_quote.mjs` 8/8, admin Python tests OK, `audit_seo.py` 0 warnings,
  every script passes a syntax check, crew, admin and six public pages load
  in headless Edge without script errors. main-pc's checkout is back on
  `main`, clean. Not
  verified: anything against the live database, real mail or a real phone.
  The account - fixed, needs-Tenis, ranked backlog - is in the website repo,
  `AUDIT-2026-09-19.md`. Worst things found and fixed: a crew member could
  read any job and any colleague's check-in selfie by typing an id; every
  Workshop save that succeeded said "Save failed"; a quote's accept could
  land twice; "valid until the 18th" died at 00:00 on the 18th; the
  newsletter form could mail-bomb any address; two clients could book the
  same measurement hour. No pull request opened: `gh` is not logged in on
  main-pc - GitHub offers the button on the branch page.

## Executed 2026-09-19 (from the cnc-pc session, hostname verified)

- ✅ **The surveillance app is located - it was on GitHub all along.** Repo
  `PreissWorkshop/Surveillance-` (private; the trailing hyphen is why the
  obvious names missed), one branch,
  `claude/camera-motion-detection-app-vmzwgf`. Built 08-27 to 08-31 by
  sessions on the shop PC. Verified here: both checkouts
  (`C:\HelmCNC\GitHub\Surveillance-` and `C:\Surveillance`) clean, no stash,
  no local-only branch or commit - nothing stranded. Registered in
  `registry/projects.yaml` with main-pc root `C:\Projects\Surveillance\repo`;
  bootstrap step 8 added (untested on main-pc). The repo's `HANDOFF.md` now
  opens with a start-here section for main-pc (bd7c7b9): the gitignored
  state that stays behind, and how each piece crosses over, is listed there
  and deliberately not here.
- ⚠ **The recorder runs nowhere.** On cnc-pc: no process, no listener, no
  autostart task; its event index was last written 09-04.
- ⚠ **The project left about 1.1 GB on the shop PC**, against the
  no-installs rule: a checkout inside `C:\HelmCNC` (the 08-16 line
  "production hosts no repos" stopped being true on 08-28), a second clone
  with a 273 MB `.venv`, and a JDK plus an Android SDK (~700 MB). Listed in
  `docs/filesystem.md`. Nothing was deleted - see below.
- ⚠ **This repo is PUBLIC on GitHub** (anonymous API, 09-19:
  `visibility=public`), and no file here says that is intended. The tracker
  carries hostnames, LAN and tailnet addresses and open ports. Visibility is
  an account setting - Tenis's call alone.

## Executed 2026-09-19 (from the cloud session - money skill)

- ✅ **The money skill exists**: `.claude/skills/money` on branch
  `claude/profitable-business-debt-situation-6d7hq3` - the finance and
  business-building brain Tenis asked for: rules, a five-phase cash model,
  the four-rung ladder (sold hours → productized service → product →
  recurring), nine evidence-labelled reference files (FI and debt math,
  Iceland tax and legal, case studies and base rates, playbooks, maker
  leverage, software and AI money, remote work and relocation, what fails,
  sources), a stdlib calculator (`plan`, `debt`, `runway`, `fi`, `rate`,
  `unit`, `score`; selftest 33/33), templates and four evals. Tested:
  with-skill vs baseline subagents on the four prompts, graded
  independently - 31/32 assertions with the skill, 19/32 without; trigger
  accuracy on twenty queries is 100 % precise but loads on only 2-3 of 10
  casual money questions in a bare session, hence the CLAUDE.md rule.
  Report: `docs/reports/2026-09-19-money-skill.md`. Wired into `CLAUDE.md`,
  `docs/employee.md`, `docs/agent-system.md`, the bootstrap doc and
  `.gitignore`.
- ✅ **Second round the same day**, on his "how else could it improve":
  a claims list plus `verify_claims.py` that makes the upgrade pass
  mechanical (controls verify from the sandbox, everything else BLOCKED
  here); a prompt hook (`.claude/hooks/money_trigger.py`,
  `.claude/settings.json`) that injects a load-the-skill note on money
  words - pipe-tested, `[UNVERIFIED — needs check]` live; a private
  decision log the skill reads and scores; the employee's monthly money
  review; `job` and `forecast` in the calculator; nine outreach and offer
  templates; six eval prompts. Rating against two days ago, his question:
  about 5/10 then, 7.5/10 now, 9 reachable after verification, the
  snapshot and the CRM/Freemius feeds.
- ⏳ **2026-09-20, laptop handoff.** Tenis is at the laptop and continues
  the skill work there, pushing to this branch; main-pc pulls later.
  `scripts/money-setup.ps1` (new, untested on Windows) does the machine
  setup in one run and, with `-Verify`, runs the source-verification
  pass from the laptop's open internet - the single biggest quality
  step left. The private folder `~\.preiss\finance` is per machine and
  travels by USB or cloud, never through git. Both skill branches (this
  one and the Icelandic one) are docs-and-skills only; merging them to
  `main` is what lets every machine pull the same thing - his call.
- ⚠ **Evidence is snippet-level by construction.** The sandbox proxy refused
  nearly every website (all `.is` sites, regulators, vendors, founders'
  blogs), so only HelmCNC's own site, Anthropic's pricing page, Apple's
  small-business page and three vendor docs repos were read on the page.
  Every other claim is labelled [S]/[SR] with its URL;
  `references/sources.md` lists the ordered upgrade pass (~2 hours from
  main-pc or the laptop).
- ⚠ **Privacy design**: personal-os is public, so the skill carries no real
  figure. Real numbers live only in a private snapshot outside every repo
  (`~\.preiss\finance\finance-snapshot.json`, from the template in
  `assets/`); `.gitignore` backstops it; the employee may model and
  recommend but never spends, and reports quote the phase, never the
  balances.
- ⚠ **Merge collision**: like the Icelandic branch, this branch edits
  `CLAUDE.md`, `docs/employee.md`, `docs/agent-system.md`,
  `docs/bootstrap-new-machine.md` and this file. Whichever merges second
  needs a hand merge of those five files (the bootstrap junction paragraph
  becomes one block listing both skills).

## Waiting on Tenis

- 🔒 **Money skill - kick off on main-pc, then merge** (09-19, updated
  09-20): main-pc has no shell over Tailscale (`docs/employee-setup-main-pc.md`),
  so the hands there are the `employee` Remote Control session - claude.ai/code
  from the laptop, or Telegram. (1) Have it add a worktree for the branch at
  `C:\Projects\_system\personal-os-money` and run
  `scripts\money-setup.ps1 -Verify` from there (the exact dispatch went to it
  from the cloud session on 09-20 and is in Tenis's chat); the script is
  untested on Windows, so read its output line by line. (2) Fill
  `~\.preiss\finance\finance-snapshot.json` on main-pc by hand, nowhere else,
  and run `plan` - the phase it prints is the starting point for every money
  conversation. (3) When the run is clean, merge the branch to `main` (it
  carries main as of a55ca34, so it merges clean; if the Icelandic branch lands
  first, hand-merge the five shared files), then on main-pc `git pull`,
  `git worktree remove C:\Projects\_system\personal-os-money`, and re-run
  `scripts\money-setup.ps1` from the main clone - it re-points the junction
  and the hook. Then book the accountant meeting with the five questions in
  `references/iceland.md` §10.
- 🔒 **Website audit branch: read `AUDIT-2026-09-19.md`, then merge or not**
  (09-19). Merging deploys. Three things in it are his alone: set a random
  `CREW_SECRET` in the Pages project (the crew cookie is signed with the
  admin password today), the kennitala / VSK number for the footer, and the
  quote terms that say "prices include 24% VAT" over ex-VAT lines.

- 🔒 **Surveillance - one double-click at main-pc** (09-19). Tenis decided
  11:14 by voice: main-pc hosts the recorder for now. Everything is
  prepared and pushed (Surveillance- 38919e2); the recorder is proven on
  main-pc against the fake camera. Left for him: **Start Shop Camera
  recorder** on the main-pc desktop, approve the Windows prompt, type the
  camera password, choose a web password. Then on the phone: Try the
  recorder again. Not yet run for real. Still open behind it: the direct
  view tried on shop wifi; the always-on box (money); his wish for no
  Tailscale, met by a Cloudflare Tunnel once the recorder runs
  (Surveillance- `docs/no-pc.md`).

- 🔒 **Approve retiring the surveillance leftovers on cnc-pc** (09-19): the
  two checkouts, the `.venv`, the JDK and the Android SDK (~1.1 GB) - only
  after main-pc has its own working clone plus whatever gitignored state
  Tenis wants carried over (listed in the repo's `HANDOFF.md`).

- 🔒 **Is this repo meant to be public?** (09-19) It is - see the cnc-pc
  section above. Private costs nothing on GitHub and breaks no clone that is
  signed in; the three cloud routines use this repo, so check their access
  to a private one before flipping it.

- 🔒 **Two branches need a yes or no** (09-19): the front desk
  (`docs/frontdesk.md` on its branch - costs API money, changes who answers
  the phone) and the Icelandic skill (safe to merge; the employee can do
  it on his word).

- 🔒 **Make a main-pc reboot harmless - pick one** (09-19). "Never reboots"
  cannot be guaranteed on Windows 11 Home; "comes back by itself" can.
  (a) Auto-logon with Sysinternals Autologon (password stored as an
  encrypted LSA secret, typed by Tenis, never seen by the employee) - then
  the two logon tasks restart the relay and the employee within minutes of
  any reboot. Free; the cost is that someone at the keyboard after a
  reboot is in without a password. (b) Windows 11 Pro upgrade - makes the
  no-auto-restart policy officially enforceable; costs money. They
  combine. Recommended: (a) now.

- 🔒 **Change the admin password now** — it travelled over Telegram
  (third 09-18 stretch); the quote work it was for is finished.

- 🔒 **HelmCNC 1.0.91/1.0.92: is Tom actually running it?** Tenis, by
  voice note 09-18: he e-mailed Tom the update "a couple of weeks back" and
  has not heard from him. So the ship was his go; installation on the
  customer machine is unconfirmed, and `installer/news.items` still has no
  entry for either version. The employee cannot read Tom's version (support
  reports sit behind the Signing token). 09-18 12:35: a no-commitment chase
  text handed to Tenis on Telegram to send from his own mail — the
  employee's mailbox is not set up and Tom has only ever heard from Tenis.
  Open until Tom answers.
- 🔒 **Website: were the 09-17 direct-to-main Claude commits yours?** Still
  open — nothing since answers it. *The merge itself is done*
  (`release/2026-09-18-client-flow` → `main` @ 04b5564, 09-18 14:05); what
  remains is the live try-out (`.ics` in Gmail/phone mail, the admin card,
  the Icelandic) per `TODO-OWNER.md`.
- 🔒 **Employee mailbox — one click left**: the `assistant@` Email Routing
  route (`docs/employee-setup-main-pc.md` step 7). *Send what is waiting*
  is done — `TODO-OWNER.md` confirms 7 sent / 0 failed, 09-18 10:52. Sending
  itself is on (Cloudflare Email Sending, 09-18); no Resend account needed.
  Inbound catch-all already delivers (live since 09-06).
- 🔒 **`gh auth login` on main-pc** — one interactive run, see the 09-18
  main-pc section above; unblocks the employee's issue-queue duty.
- 🔒 **The shop PC's `cnc` relay** has not appeared in ListAgents since the
  undo re-registered it; next time at the shop, open "Claude relay (cnc)"
  from the taskbar and answer whatever it asks.
- ⚠ **The employee's e-mail is deliberately gated.** Inbound already works -
  Email Routing has been live on preissworkshop.is since 09-06 with a
  catch-all, verified by DNS lookup 09-07, so mail to the new address arrives
  today. Outbound rides `src/api/mail.js`, which is outbox-first: every
  message becomes a `crm_outbox` row before any provider sees it, so a draft
  is a row and a row is not a sent mail. What it may send alone is narrow on
  purpose (acknowledgements, a supplier asked for a price list, a chase with
  nothing new); anything carrying a commitment - prices, dates, accepting or
  declining an order, an unhappy client, a first approach, money either way -
  waits for Tenis. Full list in `docs/employee.md` -> E-mail. Widen it once
  there is a track record he has read.
- ✅ **DECIDED 2026-09-07, same day: no WhatsApp, no Managed Agent, no API
  bill.** Tenis asked what the cheapest way is and said he does not care
  which chat app it is, because it works the same way. Telegram is free with
  no per-message fee and takes minutes; WhatsApp charges per delivered
  template message, needs Meta business verification, and needs a bridge and
  a Managed Agent we would write, host and pay for (~$3-15/day) to deliver
  the same chat box. Dropping it removes the only paid tier in the plan -
  the employee now costs nothing beyond the existing subscription. Voice went
  with it; voice notes into Telegram cover the case.

- ✅ **RESOLVED 2026-08-31: the TickCount-wrap defect is fixed, and the suite is GREEN on the failing machine itself.** `Controllers/TickWindow.cs` (5c70d83) carries the wrap-safe predicates; every sentinel comparison converted (E-STOP router, both `_liftFenceTick` gates, `_lastMachMmTick` via saturating AgeMs, UI windows); a `tickwrap` suite section drives the incident's exact tick so ANY machine proves the wrap. Decisive run on cnc-pc at 38 d uptime, TickCount live-negative: **2181 passed / 0 failed**, all nine formerly-red SAFETY checks firing (fires=1/2/3 vs 0). En route the tickwrap section's first shop run exposed a reporter NRE that silently killed 2076 checks while printing an ordinary-looking red - fixed at the reporter (8ce66f1); lesson recorded in NOTES. `test_m0.ngc` recreated and committed at the repo root (e7993d7) - the share copy is unreachable - and ship-1091.cmd repointed. 1.0.91 and 1.0.92 have since been promoted to stable (see Found 2026-09-18).
- ✅ **BitLocker on the shop PC: OFF — a reboot is access-safe.** Tenis ran `manage-bde -status C:` elevated 2026-08-28: C: fully decrypted, Protection Off, no key protectors. So a headless reboot cannot hit a recovery prompt, and with Tailscale + RDP both starting at boot, remote access survives one. This clears the last *access* risk of the reboot route. It does NOT make the reboot route free: it still means planting an auto-logon credential on a production-adjacent PC and rebooting it. Recommended path stays the staged console script — the 1.0.91 promote/release runs at the shop console anyway, so the decisive test runs for free the next time Tenis is there to ship. Reboot route remains available if he wants the answer sooner, his explicit call.
- ✅ **RESOLVED (was open as of 2026-08-28, cleared by 2026-08-30): the
  button-sweep work is committed and pushed.** helmcnc-app 67a0596 lands
  SelfTest/ButtonSweepTests.cs, UiShots.cs, SizeCeiling.cs and the csproj
  edits together (105 controls seen, 99 pressed, 0 threw, 0 dead — matches
  the figures this item was tracking); HELMCNC_NOTES.md carries the same
  entry at 2026-08-27/30. This 🔒 item sat open in the tracker for over a
  week after the work it describes had already landed — corrected
  2026-09-07 standup.
- 🔒 **The shop-PC Claude session appears to run WITHOUT permission
  gating — check this before anything else on this list.** Reported by that
  session itself on 08-27, not independently verified from the laptop: every
  project has `allowedTools: []`, there is no `permissions` block and no
  `defaultMode` in any settings file there, yet `git push` and `WebFetch` both
  execute ungated, and it could not raise a tool-permission prompt on demand
  even when trying to. It declined to force one by running something
  destructive — correct call. This means yesterday's approvals were the
  session choosing to ask Tenis questions, not the harness stopping it: the
  safety came from its judgment, not from enforcement. On a machine wired to a
  live CNC that is worth a deliberate decision. It also reverses the
  git-allowlist idea floated on 08-26 — that session does not need loosening,
  it may need gating. Check how `shell:startup\claude-remote-control.cmd`
  launches it (a `--dangerously-skip-permissions`-style flag would explain
  everything).
- 🔒 **ScanPen tolerance call, still open, third machine now confirms it.**
  `sweep-artifacts-verified` misses by floating-point dust on every machine
  tried so far, at a different value each time: laptop
  `spot_recompute_max_deviation` 1.857e-07 mm, cloud sandbox (09-18
  week-in-review, fresh `pip install`, `pytest -q`) 1.53794e-07 mm — both
  against the `< 1e-07 mm` gate, both otherwise green (46/47 pytest; main-pc
  and cnc-pc previously reported 47/0, not re-verified this session). Three
  different values on three environments is stronger evidence for FP
  variance, not a regression — but the house rule holds: a missed threshold
  is reported, never loosened. Widen the gate or pin package versions:
  Tenis's call.
- 🔒 Approve later cleanups: empty husks (`Mach3`, `KilnController`, `lbr`,
  `Voiceover`, `New folder` — all verified 0 bytes); archive `HelmCNC.56` +
  `HelmCNC-preclean-2026-07-25-*` as dated zips; remove merged worktrees
  (`.wt-gaps`, `.wt-shepherd`) via `git worktree remove`; decide the fate of
  branch `resume-rapid-approach` (now safe on origin).
- 🔒 **After the laptop clone is verified working**: retire `C:\ScanPen`
  from cnc-pc (frees ~6.6 GB, roughly doubling free disk; the D: archive and
  GitHub remain). *2026-08-20: the **main-pc** clone is verified green, which
  `Post/MAIN-PC-SETUP.md` deems sufficient for the retire — Tenis's call.*

## Standing decisions

- Shop-PC roots are grandfathered (architecture.md) — no moves, ever, of
  `C:\HelmCNC.bak`, `C:\HelmCNC`, KMotion, FlexiCAM-AmpBackups,
  StateBackups, Signing.
- ScanPen's full history stays local + on the stick. If GitHub-hosted history
  is ever wanted, run `git filter-repo` (dropping `capture/`) on **main-pc**,
  never on the shop PC.
- Big media never lands on the cnc-pc disk again.
