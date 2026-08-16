# Master setup — session report, 2026-08-16

Session on **cnc-pc** (DESKTOP-A60V7P2), rooted at `C:\HelmCNC`, cross-project
by explicit instruction. Read-only discovery first; execution approved same
day ("do everything yourself"). Result: **every project now has an
off-machine copy**, the control layer is live, and nothing production was
touched.

## 1 · What discovery found

Machine: Win10 Pro, 111 GB Kingston SSD with **7.6 GB free**; D: = SanDisk
USB stick (14 GB, NTFS, physically separate). Tools: git 2.55 + LFS, Python
3.11.9, VS Code, framework MSBuild, GitHub Desktop 3.6.4; absent: gh CLI,
Node, Docker, WSL. Operator app not running during the work.

Git estate (7 repos):

| Repo | State found |
|---|---|
| `C:\HelmCNC.bak` (PreissWorkshop/helmcnc-app) | **ahead 20 commits, 12 dirty files** (08-10 integration + 08-12 wind caption; commit message prepared in `HELMCNC_NOTES.md`) |
| `C:\HelmCNC.wt` / `.wt-gaps` / `.wt-shepherd` | linked worktrees, all clean; `resume-rapid-approach` unmerged and local-only; shepherd branches merged |
| `C:\HelmCNC.bak\GitHub\HelmCNC` (site/releases) | clean, synced |
| `C:\ScanPen` | **no remote, no backup anywhere** — 6.6 GB, 3.4 GB git objects, capture mp4s up to 785 MB committed (blocks any plain GitHub push) |
| `C:\HelmCNC\GitHub\personal-os` | empty (0 commits, 0 files), remote wired, nested inside the production install dir |

Also verified: `C:\HelmCNC` = 6 MB production install + live machine state;
`C:\HelmCNC-Signing` secrets (license key + tokens) deliberately outside git,
mirrored to `D:\`; machine-critical `KMotion×3`, `FlexiCAM-AmpBackups`,
`HelmCNC-StateBackups`; five empty 0-byte husk dirs (`Mach3`,
`KilnController`, `lbr`, `Voiceover`, `New folder`); OneDrive held one stale
source bundle (07-24).

Top risks identified: (1) ScanPen existed on exactly one disk; (2) 20
unpushed + 12 uncommitted HelmCNC changes; (3) personal-os sat inside the
production install folder; (4) 7.6 GB free disk.

## 2 · Decisions

- **GitHub is the source of truth**; machines are roles: cnc-pc = HelmCNC
  appliance only · main-pc (RDP source) = primary dev · Samsung laptop =
  travel dev.
- **Grandfather the live shop roots** (`C:\HelmCNC.bak`, `C:\ScanPen`) —
  moving them breaks worktree links, session memory, and the documented
  deploy; the registry makes them findable. Clean `C:\Projects\` layout
  applies to other machines and new work.
- **ScanPen goes to GitHub as a fresh-start history** (no capture blobs; a
  filtered full-history push stays possible later, on main-pc). Captures are
  out-of-git data with provenance mapping.
- Machine backups stay physically where procedures expect them; personal-os
  documents them instead of moving them.

## 3 · Executed (all verified)

1. **ScanPen safety copy** → `D:\ScanPen-backup-2026-08-16`: 552 dirs,
   **843 files, 6.504 GB, 0 failures** (robocopy, ~10 min), including `.git`
   and the three uncommitted capture takes.
2. **personal-os live**: cloned to `C:\Projects\_system\personal-os`, seeded
   with README, `registry/projects.yaml`, and docs (architecture, filesystem,
   security, development-workflow, agent-system, migration-plan,
   bootstrap-new-machine). Commits `80f1358`, `c986ec0`, `c15a529` pushed to
   `origin/main`.
3. **scanpen on GitHub**: staging copy built minus `capture/`/caches (10.4 MB),
   `PROVENANCE.md` added, committed as `506dd95` (135 files, largest blob
   1.5 MB). Tenis created the empty private repo (computer-use on GitHub
   Desktop was declined — recorded; no UI automation used); push verified:
   `PreissWorkshop/scanpen` `master` = `506dd95`.
4. **helmcnc-app pushed**: `master` 22fc611 → 0a0b493 (**20 commits now on
   GitHub**) plus `resume-rapid-approach` as a remote backup branch. Zero
   working-tree changes — the 12-file integration commit remains Tenis's
   paste.
5. **Records**: migration state maintained as the living doc
   `docs/migration-plan.md`; session memory updated.

## 4 · Deliberately untouched

`C:\HelmCNC` + `Data\` (production), the `.bak` working tree (dirty files
await the prepared commit), KMotion, FlexiCAM-AmpBackups, StateBackups,
Signing folders (contents never read), the husk dirs (nothing deleted
anywhere), and no software installed.

## 5 · Before → after

| Risk | Before | After |
|---|---|---|
| ScanPen | 1 copy, one SSD | SSD + USB stick + GitHub (code) |
| HelmCNC commits | 20 unpushed | 0 unpushed (12 dirty files = Tenis's paste) |
| personal-os | empty, inside production dir | live on GitHub, clean root, 3 commits |
| `resume-rapid-approach` | local-only branch | on origin |
| Shop disk | 7.6 GB free | unchanged; +6.6 GB once `C:\ScanPen` retires |

## 6 · Remaining queue

**Tenis:** HelmCNC commit paste (from a `.bak` session) → push · laptop
bootstrap before vacation (`docs/bootstrap-new-machine.md`; take the D: stick
for captures) · OK the deletion of the empty old `C:\HelmCNC\GitHub\personal-os`.

**Later, each with approval:** delete husks · archive `HelmCNC.56` +
`HelmCNC-preclean-*` · remove merged worktrees, decide
`resume-rapid-approach` fate · retire `C:\ScanPen` after the laptop clone is
verified (frees ~6.6 GB) · third offline copy of the signing key · refresh or
retire the stale OneDrive bundle.

## 7 · Reference

- personal-os: <https://github.com/PreissWorkshop/personal-os> ·
  local `C:\Projects\_system\personal-os`
- scanpen: <https://github.com/PreissWorkshop/scanpen> (private, fresh-start)
- helmcnc-app: <https://github.com/PreissWorkshop/helmcnc-app> ·
  site: <https://github.com/PreissWorkshop/HelmCNC>
- Living plan: `docs/migration-plan.md` (this repo)
