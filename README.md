# personal-os

The control layer for Tenis Preiss's projects and machines — the repo that
knows where everything lives, how the machines divide the work, and how AI
agents should behave wherever they run. It sits **above** the projects:
HelmCNC, ScanPen, the website, and whatever comes next.

**Source of truth is GitHub, not any one computer.** Every machine is a
working environment that clones what it needs and pushes what it produces.

## Map

| Machine | Role | Holds |
|---|---|---|
| **cnc-pc** (DESKTOP-A60V7P2, shop) | HelmCNC appliance — production + HelmCNC dev only; weak, keep lean | `C:\HelmCNC` (installed app), `C:\HelmCNC.bak` (dev repo), machine config + backups |
| **main-pc** (the RDP source) | Primary dev workstation | `C:\Projects\...` clones of everything |
| **laptop** (Samsung, travel) | Portable workstation | clones of whatever the trip needs |
| **GitHub** (PreissWorkshop) | Source of truth | helmcnc-app · HelmCNC (site) · scanpen · personal-os |

## Start here

- [docs/architecture.md](docs/architecture.md) — the rules that keep this from becoming chaos again
- [registry/projects.yaml](registry/projects.yaml) — every project, its repos and canonical roots
- [docs/projects.md](docs/projects.md) — the projects in prose
- [docs/backups.md](docs/backups.md) — every backup, where it lives, how fresh
- [docs/bootstrap-new-machine.md](docs/bootstrap-new-machine.md) — set up a new computer in ~30 minutes
- [docs/migration-plan.md](docs/migration-plan.md) — the 2026-08 cleanup: done, pending, decisions

No secrets in this repo, ever. See [docs/security.md](docs/security.md).
