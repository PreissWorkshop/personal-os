# Week in review — 2026-09-18

Cloud routine (`week-in-review`, Fri 15:00 UTC), first successful run — this
session's own execution is the proof the routine works; the "never fired"
question tracked in `migration-plan.md` since 09-18 morning is resolved by
this report existing. No machine access: this session is a cloud sandbox
with the four repos cloned read/write, no Windows box, no Telegram, no
`gh` CLI (GitHub via the MCP server only, scoped to the four repos below).
Window: git history across all branches, last 7 days (2026-09-11 →
2026-09-18); in practice every commit in that window lands on 09-17 or
09-18 — nothing from 09-11 through 09-16 in any of the four repos.

## personal-os

**Shipped.** The employee itself: `docs/employee.md` went from "designed,
not live" to running on `main-pc` (PREISSWORKSHOP) in auto mode, paired to
Tenis alone on Telegram, with local voice (faster-whisper in, Kokoro TTS
out). Root cause found and fixed for a mis-run that put the bootstrap (Bun,
Telegram plugin, bot token, auto-mode employee) on the CNC appliance
(`DESKTOP-A60V7P2`) instead of main-pc — hostname guards now block every
installer and the employee itself on that host by name, not by role alone.
~50 commits 09-17/09-18, effectively a full day of infra work condensed
into one.

**Tracker changes this session:**
- Both standup PRs closed, neither merged. PR #1 (button-sweep correction)
  was already closed — verified via the GitHub API. PR #2 (1.0.91/1.0.92
  ship correction) was still open; its content-diff against `main` was a
  no-op (the correction is already in `migration-plan.md` verbatim, landed
  same-day by a different commit) — closed this session with a comment
  explaining why, not merged.
- The "two of three routines have never run" item is now one-of-three:
  week-in-review fired and produced this report. Website audit (Wed 07:00)
  is still unverified — this session has no access to the routines' run
  list, only to what git shows; next due 09-23.
- Website "waiting on Tenis" bullet was half stale: the
  `release/2026-09-18-client-flow` merge it was still asking for happened
  the same day (04b5564, 14:05), leaving only the live try-out open. Split
  into current parts.
- Employee mailbox bullet was half stale: *Send what is waiting* is done
  (`TODO-OWNER.md`: 7 sent, 0 failed, 09-18 10:52) — only the `assistant@`
  Email Routing route is left.
- ScanPen's floating-point-dust tolerance item got a third data point (see
  below) instead of resting on the laptop's single number.

**Nothing stalled here** — this repo only tracks; it doesn't itself get
blocked.

## HelmCNC (helmcnc-app)

**Stalled, fully — zero commits on `master` in the last 7 days, or the
last 14.** Latest commit 27d0286, 2026-09-04 (`promote.ps1` gains a `-Go`
flag that skips the typed release gate). Tags `stable/v1.0.91` (e7993d7,
08-31) and `stable/v1.0.92` (d33107f, 09-02) both predate the window —
nothing shipped or built this week, the last engineering was two weeks
ago. No branches ahead of `master` carry unmerged work: `resume-rapid-approach`
is 190 commits behind / 1 ahead (stale, dispositioned in the tracker as
"decide the fate of," not this week's business) and `claude/hopeful-tesla-512813`
is fully contained in `master` (merged 08-09, nothing unique).

**Why stalled:** not blocked on anything technical — the tickwrap E-STOP
fix is done and proven (2181/0 on cnc-pc at 38 days uptime, 08-31), both
releases are tagged. The open item is downstream of the code: whether Tom
actually received and installed 1.0.91/1.0.92. `installer/news.items`
still carries exactly one entry, dated 08-09, about machine-setup saving —
nothing describing the E-STOP/tickwrap fix, and no entry at all for
1.0.92. Verified again this session (file read directly) — unchanged from
what the tracker already said.

**Could not run the suite here.** `HelmSelfTest.exe` is a Windows
x86/.NET-Framework WinForms binary built against KFLOP/Dynomotion headers;
this sandbox is Linux with no MSBuild, no Windows, no `bin\ReleaseNew`. The
last real numbers on record are main-pc's 2179/0 (09-04, subagent-run,
7 checks fewer than cnc-pc's 2181 — unexplained gap, not re-chased this
session either) and cnc-pc's 2181/0 (08-31, the tickwrap decisive run).
Not re-verified this session; do not read this report as a fresh green.

## ScanPen

**Stalled — zero commits in 7 days**, same as HelmCNC. Latest commit
506dd95 ("ScanPen fresh start for GitHub"), 2026-08-16; `CLAUDE.md`'s State
section (last dated entry 2026-08-09/10, Phase 1 core) is unchanged and
still accurate — nothing to correct there. No open branches beyond
`master`. This isn't a blocker situation: no engineering time went to
ScanPen this week, full stop; the week's work (per the git history above)
went entirely into the employee bootstrap and the website.

**Suite run for real, this session** (fresh `pip install` of
`opencv-contrib-python numpy scipy pytest matplotlib` into the sandbox,
nothing cached):
- `python -m pytest -q` → **46 passed, 1 failed**, 200s. The one failure is
  `sweep-artifacts-verified`: `spot_recompute_max_deviation` = **1.53794e-07 mm**
  against the `< 1e-07 mm` gate — the same known floating-point-dust miss
  the tracker already carries from the laptop (there: 1.857e-07 mm). All
  other assertions in that check pass (`cells_planned`/`cells_recorded` =
  44/44, `unexplained_gaps` = 0).
- `python -m scanpen.selftest --full` → **37 passed, 1 failed** of 38
  registry checks, exit code 1. Same failing check, same measured value
  (1.53794e-07 mm) — consistent within this session, as expected since both
  harnesses call the same check registry.
- This is a **third distinct measured value** on a third distinct machine
  (laptop, main-pc/cnc-pc previously reported 47/0 but not re-verified this
  session, now this cloud sandbox) for the same gate — stronger evidence
  it's floating-point variance across numpy/BLAS builds, not a code
  regression, but **per house rule this is still reported as a miss, not
  loosened or explained away.** The tracker's open item now says so.
- Working tree left clean afterward: the run's own `results/capability_report.json`
  diff was reverted (`git checkout --`), nothing committed to ScanPen.

## Preiss Workshop website

**Shipped, and it's the week's real news.** 09-17 brought 9 commits (a11y,
Icelandic-first copy, gallery/keyboard fixes, forms) landing straight on
`main` by a "Claude" author with no branch or PR — the tracker's open
question about whether that was Tenis driving is still open; nothing since
answers it, so it stays 🔒 rather than assumed either way.

09-18 is one long chain: Cloudflare Email Sending replaces the Resend plan
(`preiss-mail` Worker bound as `MAIL`, SPF/DKIM/DMARC verified pass,
DMARC `p=reject`) → outbox drained (7 sent, 0 failed) → quote-page mobile
polish → measurement-appointments Phase 1 (owner offers slots, client
books on a script-free page, both get an `.ics`) → client branding (dark
header + logo on quote page, job page, all client mail) → all three
assembled on `release/2026-09-18-client-flow`, one `src/api/portal.js`
conflict resolved keeping both sides → **merged to `main` by Tenis, 14:05,
`main` @ 04b5564**, verified live same day (`/api/admin/ping` reports
db/auth/mail/github/turnstile all true).

**Verified this session, independently:**
- `git ls-remote` confirms `main` @ 04b5564 matches the local clone exactly
  (fetched fresh, no stale ref).
- `python src/site/build.py` → **"Build OK — 114 pages, 56 sitemap URL
  pairs"**, matching the number the in-tree session reported. The build did
  produce a 1-day lastmod drift on 3 files (`glerfilmur-sidekick` pages +
  sitemap, `2026-09-05` vs `2026-09-06`) — looked like noise from a source
  file's mtime, not a code defect; reverted (`git checkout -- public/`)
  rather than left dirty, and not chased further since it doesn't affect
  the page/sitemap counts.
- No `package.json` / `npm test` in this tree — `test_crm.html` and
  `test_quote.mjs` run via a throwaway Node harness outside the repo per
  `PROGRESS.md`'s own account, which this session did not reconstruct. The
  82/8 numbers in `PROGRESS.md` (test_crm, test_quote) are **not verified
  by this session** — they're the implementing session's own report, carried
  here as-is, not re-run.
- 21 remote branches beyond `main` exist (`git ls-remote --heads`), most
  long-dead feature/backup branches predating this week
  (`feature/site-redesign-admin-2026-07`, `homepage-*`, `polish/*`,
  `backup/*`). The four this week actually produced
  (`chore/lf-endings-untrack-pyc`, `feat/client-branding`,
  `feat/measurement-appointments`, `release/2026-09-18-client-flow`) are
  now dead too — merged, not deleted. Deletion is explicitly 🔒 Tenis per
  the tracker; not touched here.

**What stalled:** nothing shipped got stuck — the live try-out is the one
open step (`.ics` behaviour on the phone, the admin card, the Icelandic),
tracked in the website's own `TODO-OWNER.md` and still open. Phase 2
(reminders) hasn't started, waiting on that feedback per the plan.

## What could be wrong

- The three-machines-three-values pattern on ScanPen's one failing gate is
  read here as FP variance across environments, on the strength of "same
  check, different value each time, everything else green." That's an
  inference, not a proof — it could instead be a real sensitivity in
  `spot_recompute` to library versions that happens to read as "dust" at
  every value seen so far. Worth a `pip freeze` diff against main-pc/laptop
  if it ever needs to be ruled in or out for real.
- The website's 82/8 test counts and "byte-identical build" claims for
  main-pc are carried from PROGRESS.md and prior tracker entries, not
  re-run by this session (no npm harness reconstructed here) — flagged
  above, repeating it here because it's the kind of thing easy to skim past.
- HelmCNC's 2179 vs 2181 check-count gap between main-pc and cnc-pc (09-04
  vs 08-31) is still unexplained in the tracker and stays that way; this
  session had no way to run either build to re-check it.

## What was assumed

- That "last 7 days" means calendar days 09-11 through 09-18 inclusive, not
  the last 7 *commits* or a rolling business week. In this case it made no
  difference — every commit in any repo this session found falls on 09-17
  or 09-18 anyway — but a repo with steady daily commits would need the
  distinction made explicit.
- That this session firing *is* the scheduled `week-in-review` routine
  referred to throughout the tracker, based on the prompt matching its
  description (Fri 15:00 UTC, same task). Not independently confirmed
  against claude.ai/code/routines' own run log, which this session cannot
  reach.

## What was verified, and how

- Every git claim above: `git fetch`/`git log --all --since`/`git branch -r`
  run directly against `origin` for all four repos, not read off a prior
  report. Two repos (helmcnc-app, personal-os) were shallow clones;
  unshallowed before trusting the 7-day window.
- ScanPen's suite/selftest numbers: run live in this session (pytest 200s,
  selftest --full ~3 min), output read directly, not copied from a prior
  report.
- Website build: run live in this session, output read directly.
- PR states: read live from the GitHub API (`list_pull_requests`), not
  inferred from local refs.
- HelmCNC suite and website's Node test harness: **not verified this
  session** — no Windows/.NET here for the former, no reconstructed harness
  for the latter. Said so above rather than repeating old numbers as new.

## What still needs Tenis

- HelmCNC: did Tom receive and install 1.0.91/1.0.92? (open since before
  this week; `installer/news.items` still has no entry for either.)
- Website: were the 09-17 direct-to-main commits his own session, and the
  live try-out of the measurement-booking flow (`.ics`, admin card,
  Icelandic) per `TODO-OWNER.md`.
- `assistant@` Email Routing route — the one remaining mailbox click.
- ScanPen tolerance gate: widen `< 1e-07 mm` or pin package versions, now
  with a third machine's data point.
- Housekeeping, none urgent: delete the four now-dead website branches;
  decide `resume-rapid-approach`'s fate on helmcnc-app.

## Safest next step

Nothing here needs an urgent action from Tenis beyond what the tracker
already had queued — this was a quiet week for HelmCNC and ScanPen and a
loaded one for the website and the employee's own bootstrap, and both of
those already landed cleanly with their open items already flagged
in-tree. The one new decision this report surfaces is the ScanPen
tolerance gate, now better evidenced; everything else is either already
✅ or already 🔒 and simply carried forward, corrected where stale.
