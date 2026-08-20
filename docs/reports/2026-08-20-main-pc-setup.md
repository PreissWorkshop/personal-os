# 2026-08-20 — main-pc bootstrapped, ScanPen verified

Session on main-pc (hostname PREISSWORKSHOP), executing
`Post/MAIN-PC-SETUP.md` from the workshop session. Full result in that Post
folder (`SETUP-RESULT.md`); essentials here.

- **Tools**: installed Python 3.11.9 (user, `py -3.11`; 3.13 stays default),
  VS Code 1.132.0 (user), gh 2.97.0 (user/portable). Already present: git
  2.55.0, GitHub Desktop 3.6.4, Node 24.18.0 LTS. Zero UAC prompts.
- **Auth**: GCM already held a push-capable PreissWorkshop credential —
  Tenis's sign-in step was unnecessary. `gh` itself not authed (not needed).
- **Clones** per registry roots: personal-os main@d3f7013 ·
  scanpen master@506dd95 · helmcnc-app master@0a0b493 (no build, per rules).
- **ScanPen gates on the fresh clone**: suite `pytest -q` **47/0** (231 s);
  `selftest --full` **38 checks / 0 failed**. Synthetic-only, no captures
  copied. Regenerated `capability_report.json` was restored — clone left
  byte-identical to origin.
- Note: main-pc also has a `C:\HelmCNC` directory, unmapped in the registry
  (untouched, unexamined) — filesystem.md may want a line on it.
