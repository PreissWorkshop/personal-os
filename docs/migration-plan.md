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
  preflight executed on the laptop. Note for anyone writing more of them:
  PowerShell 5.1 reads `.ps1` as ANSI, so a UTF-8 em-dash becomes a string
  terminator error - keep scripts ASCII.
- ❌ **HelmCNC support-report triage was deliberately NOT made a routine.**
  The reports sit behind an admin endpoint whose token lives in the Signing
  folder; a cloud sandbox has neither the token nor the network permission,
  and this repo will never carry it. That job stays on main-pc or cnc-pc.
- Assessment, findings and the WhatsApp/voice picture:
  `docs/reports/2026-09-07-employee-agent.md`.

## Waiting on Tenis

- 🔒 **Thursday 2026-09-10 at main-pc: bring the employee to the phone.**
  Follow `docs/employee-setup-main-pc.md` steps 1-6 (~20 min). Two steps are
  his alone: creating the Telegram bot with BotFather (account creation), and
  choosing the permission posture - the shipped default keeps prompts and
  approves from the phone, which is the recommended one. Everything else is
  scripted.
- 🔒 **Phase 2 go/no-go: WhatsApp + Managed Agent.** No official WhatsApp
  support exists anywhere in the Claude stack, so it means Meta's Business
  Cloud API plus a Cloudflare Worker bridge in front of a Managed Agent with
  a memory store and a delegation roster - roughly $3-15/day of API usage on
  top of the subscription, and business verification on Meta's side can take
  days. Nothing depends on it; phases 0 and 1 stand alone. Voice calls are a
  further step again (media server + speech-to-text/text-to-speech).

- ✅ **RESOLVED 2026-08-31: the TickCount-wrap defect is fixed, and the suite is GREEN on the failing machine itself.** `Controllers/TickWindow.cs` (5c70d83) carries the wrap-safe predicates; every sentinel comparison converted (E-STOP router, both `_liftFenceTick` gates, `_lastMachMmTick` via saturating AgeMs, UI windows); a `tickwrap` suite section drives the incident's exact tick so ANY machine proves the wrap. Decisive run on cnc-pc at 38 d uptime, TickCount live-negative: **2181 passed / 0 failed**, all nine formerly-red SAFETY checks firing (fires=1/2/3 vs 0). En route the tickwrap section's first shop run exposed a reporter NRE that silently killed 2076 checks while printing an ordinary-looking red - fixed at the reporter (8ce66f1); lesson recorded in NOTES. `test_m0.ngc` recreated and committed at the repo root (e7993d7) - the share copy is unreachable - and ship-1091.cmd repointed. **1.0.91 is one console visit from customers: `git pull` in C:\HelmCNC.bak, then `ship-1091.cmd`** (release -> watched live M0 test -> promote, Tenis's typed words at the gate).
- ✅ **BitLocker on the shop PC: OFF — a reboot is access-safe.** Tenis ran `manage-bde -status C:` elevated 2026-08-28: C: fully decrypted, Protection Off, no key protectors. So a headless reboot cannot hit a recovery prompt, and with Tailscale + RDP both starting at boot, remote access survives one. This clears the last *access* risk of the reboot route. It does NOT make the reboot route free: it still means planting an auto-logon credential on a production-adjacent PC and rebooting it. Recommended path stays the staged console script — the 1.0.91 promote/release runs at the shop console anyway, so the decisive test runs for free the next time Tenis is there to ship. Reboot route remains available if he wants the answer sooner, his explicit call.
- 🔒 **Uncommitted button-sweep work in the laptop helmcnc-app tree needs
  committing by its own session so it is not lost.** A parallel session built an
  offline UI button-sweep harness (SelfTest/ButtonSweepTests.cs, plus UiShots.cs
  and Program.cs/csproj edits) - 99 controls pressed, 0 crashes - and
  independently found that SWITCH PROBE and HOME SWITCH GUIDE cannot build
  offline because their ctors demand a concrete KflopController. It is currently
  UNCOMMITTED and partly UNTRACKED in C:\Projects\HelmCNC\app, with a 71-line
  NOTES entry also uncommitted. This session deliberately did NOT touch that tree
  to avoid clobbering it. Commit it as its own coherent unit (source + NOTES) and
  push.
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
- 🔒 **ScanPen tolerance call** — on the laptop, `sweep-artifacts-verified`
  misses by floating-point dust: `spot_recompute_max_deviation` 1.857e-07 mm
  against a `< 1e-07 mm` gate, suite otherwise 46/47 green (47/0 on main-pc
  and cnc-pc). Cross-machine FP variance, not a regression — but the house
  rule is that a missed threshold is reported, never loosened. Widen the gate
  or pin package versions: Tenis's call.
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
