# Development workflow

## Sessions

- **One session, one project, rooted at that project's canonical root** (see
  registry/projects.yaml). Cross-project work: name it first, get an explicit
  OK, and treat the host project's tree as read-only.
- Session start: read the project's in-tree instructions (CLAUDE.md) and its
  handoff notes (HelmCNC: `HELMCNC_NOTES.md` top; ScanPen: CLAUDE.md state
  section).
- Session end, if commits were produced: **push**. Unpushed commits on the
  shop PC were historically the #1 data risk of the whole operation.

## Per project

- **HelmCNC on cnc-pc** — the in-tree procedure is binding: `build.cmd
  ReleaseNew`; suite green (offline self-test) before anything ships; deploy
  is a file-level hot-swap only while the operator app is closed; releases go
  through `installer\release.ps1` and are Tenis's call.
- **HelmCNC off-shop** — code work from clones is fine. `tools/` (roslyn
  toolset) is gitignored; restore it per the `.gitignore` note before
  building. Nothing built off-shop touches the machine except through the
  documented deploy on cnc-pc.
- **ScanPen (main-pc / laptop)** — the suite is the only truth:
  `python -m pytest -q` and `python -m scanpen.selftest --full`. Accuracy
  numbers only from tests/runs in the current session. Captures are
  out-of-git data; `fieldmeasure`/replay work needs clips copied locally.
- **Site (HelmCNC public repo)** — normal web workflow; release announcements
  coordinate with helmcnc-app's release procedure.

## Git conventions

- Story-carrying commit subjects (house style). Suite green before commit
  wherever a suite exists. master/main stays shippable; experiments live on
  branches and get pushed (a local-only branch is a liability, not privacy).
- Old versions become dated archives (`Name-YYYY-MM-DD`), never `-final2`
  siblings. Duplicates are reported, not silently deleted.
