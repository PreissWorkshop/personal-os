# Filesystem map

## cnc-pc (DESKTOP-A60V7P2) — shop PC, 111 GB SSD, keep lean

Verified by full discovery 2026-08-16. This machine runs the CNC; nothing new
gets installed or stored here without a reason tied to the machine.

| Path | What it is | Rule |
|---|---|---|
| `C:\HelmCNC` | Installed operator app + live machine state (`Data\`: emc.var, Tool.tbl, trial.dat, logs) | Production. Deploy = documented hot-swap only, app closed |
| `C:\HelmCNC.bak` | **HelmCNC dev repo** (helmcnc-app, master) | The only place HelmCNC source is edited on this PC |
| `C:\HelmCNC.bak\GitHub\HelmCNC` | Site + releases repo checkout | Normal repo |
| `C:\HelmCNC.wt`, `.wt-gaps`, `.wt-shepherd` | Linked git worktrees of `.bak` | Never move `.bak`; remove worktrees only via `git worktree remove`, with approval |
| `C:\HelmCNC.56`, `C:\HelmCNC-preclean-2026-07-25-*` | Old install snapshots | Archive candidates (approval pending) |
| `C:\HelmCNC-StateBackups` | Machine-state snapshots | KEEP |
| `C:\FlexiCAM-AmpBackups` | Servo-amp parameter backups (X/YL/YR/Z) + tune history | KEEP — machine recovery. Never move |
| `C:\KMotion5.4.1`, `_clean`, `5.4.4`, root `.zip` | Dynomotion SDK/source installs | KEEP — machine software |
| `C:\HelmCNC-Signing` | SECRETS (see security.md) | Never in git; mirrored to `D:\` |
| `C:\ScanPen` | ScanPen full-history archive (6.6 GB) | Frozen. Retire after laptop verified → frees ~6.6 GB |
| `C:\Projects\_system\personal-os` | Thin clone of this repo | Keep current |
| `C:\Mach3`, `C:\KilnController`, `C:\lbr`, `C:\Voiceover`, `C:\New folder` | EMPTY husks (verified 0 bytes, 2026-08-16) | Delete on approval |
| `D:\` (SanDisk USB stick, NTFS, 14 GB) | `HelmCNC-Signing` mirror + `ScanPen-backup-2026-08-16` | Backup medium; physically separate; can travel |
| `OneDrive\HelmCNC-Backups` | Stale source bundle (2026-07-24) | Superseded by origin pushes |

Disk reality: ~7.6 GB free before the cleanup; retiring `C:\ScanPen` (after
verification) roughly doubles it.

## main-pc / laptop

Clean layout per architecture.md — everything under `C:\Projects\`, nothing
project-related loose on `C:\`. Big media (ScanPen captures, video footage)
goes to external/cloud storage, never into repos.
