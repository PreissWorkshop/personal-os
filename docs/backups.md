# Backup index

Every backup, where it physically lives, and how fresh. Standing rule:
backups are documented here, **not** physically consolidated — emergency
procedures expect them where they already are.

| What | Where | Medium | As of | Notes |
|---|---|---|---|---|
| ScanPen — full (incl. `.git` + uncommitted takes) | `D:\ScanPen-backup-2026-08-16` | SanDisk USB stick (separate device from the SSD) | 2026-08-16 · verified 843 files / 6.504 GB / 0 failures | Only full-history + captures copy besides `C:\ScanPen` itself |
| ScanPen — code | github.com/PreissWorkshop/scanpen | GitHub | live | Fresh-start history, no captures |
| HelmCNC — source | github.com/PreissWorkshop/helmcnc-app | GitHub | live (master pushed 2026-08-16) | 12-file integration commit stays local until Tenis's paste |
| HelmCNC — site/releases | github.com/PreissWorkshop/HelmCNC | GitHub | live | |
| Signing secrets | `C:\HelmCNC-Signing` + `D:\HelmCNC-Signing` | shop SSD + USB stick | files dated 2026-07-23/28 | **TODO: third offline copy** — both current copies sit in one room, and sticks die |
| Machine state snapshots | `C:\HelmCNC-StateBackups` | shop SSD | 2026-08-05 | Tool table / offsets / state |
| Servo amp parameters | `C:\FlexiCAM-AmpBackups` | shop SSD | 2026-07-26/30 | X / Y-left / Y-right / Z `.ap0` + tune history — machine-recovery gold, never move |
| Old install snapshots | `C:\HelmCNC.56`, `C:\HelmCNC-preclean-2026-07-25-*` | shop SSD | July 2026 | To become dated zip archives (approval pending) |
| KMotion software | `C:\KMotion5.4.1`, `_clean`, `5.4.4`, root zip | shop SSD | June–July 2026 | Machine software + SDK |
| HelmCNC source bundle | `OneDrive\HelmCNC-Backups\helmcnc-source-2026-07-24.bundle` | OneDrive | 2026-07-24 — **stale** | Superseded by the GitHub push; refresh or retire (Tenis's call) |

## Gaps to close

- Third copy of the signing key, offline (USB in a drawer, or paper/QR).
- ScanPen captures have no cloud copy (shop SSD + one stick). Acceptable
  while takes are re-creatable; revisit the moment they aren't.
