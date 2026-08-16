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

## Waiting on Tenis

- 🔒 **HelmCNC integration commit** — 12 dirty files in `C:\HelmCNC.bak`,
  message prepared at the top of `HELMCNC_NOTES.md`. Paste it from a
  `C:\HelmCNC.bak`-rooted session (or by hand), then push again.
- 🔒 Delete the now-redundant empty `C:\HelmCNC\GitHub\personal-os`
  (verified 0 commits, 0 files before relocation).
- 🔒 **Laptop bootstrap before vacation** — docs/bootstrap-new-machine.md.
- 🔒 Approve later cleanups: empty husks (`Mach3`, `KilnController`, `lbr`,
  `Voiceover`, `New folder` — all verified 0 bytes); archive `HelmCNC.56` +
  `HelmCNC-preclean-2026-07-25-*` as dated zips; remove merged worktrees
  (`.wt-gaps`, `.wt-shepherd`) via `git worktree remove`; decide the fate of
  branch `resume-rapid-approach` (now safe on origin).
- 🔒 **After the laptop clone is verified working**: retire `C:\ScanPen`
  from cnc-pc (frees ~6.6 GB, roughly doubling free disk; the D: archive and
  GitHub remain).

## Standing decisions

- Shop-PC roots are grandfathered (architecture.md) — no moves, ever, of
  `C:\HelmCNC.bak`, `C:\HelmCNC`, KMotion, FlexiCAM-AmpBackups,
  StateBackups, Signing.
- ScanPen's full history stays local + on the stick. If GitHub-hosted history
  is ever wanted, run `git filter-repo` (dropping `capture/`) on **main-pc**,
  never on the shop PC.
- Big media never lands on the cnc-pc disk again.
