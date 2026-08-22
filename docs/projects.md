# Projects

Narrative overview. Machine paths and remotes live in
[`registry/projects.yaml`](../registry/projects.yaml) — the registry is the
source of truth; this page is the story.

## HelmCNC — active, shipping

CNC control application (C# WinForms, .NET Framework, x86, KFLOP/Dynomotion)
that runs Tenis's own machine and ships to customers. Two repos:
**helmcnc-app** (private dev, branch `master`, self-test-suite-gated) and
**HelmCNC** (public site + releases). Development happens on cnc-pc in
`C:\HelmCNC.bak`, one documented hot-swap away from the operator install —
which is why its procedures (in-tree `CLAUDE.md` + `HELMCNC_NOTES.md`) are
binding. Customer bug/feature reports arrive through the app's SUPPORT
screen (triage via the helm-reports skill).

## ScanPen / Scan Pen Probe — active, Phase 1

Phone + printed-marker tactile probe for millimetre measurement (windows,
films, templating). Python 3.11 + OpenCV core, Android capture-probe app;
the selftest suite is the only source of truth for what works. Phase 0
complete with a won blind field test (window measured to 0 mm at ~3 m);
Phase 1 (live audio hold-feedback) built and replay-verified. Repo:
**scanpen** (private; fresh-start history 2026-08-16 — capture footage lives
outside git, see that repo's `PROVENANCE.md`). Development belongs on
main-pc / laptop; the CNC-cut truth artifact is its only tie to the shop.

## personal-os — active

This repo: the control layer (machine map, registry, policies, plans,
reports). Not a product.

## Preiss Workshop website — active, redesign

Static generated site for the workshop's public presence — premium,
architectural, material-focused. Stdlib-Python generator in `src/site/`,
committed output in `public/`. Repo: **preiss-workshop-website**; newest
work on `feature/fable-design-refinement`. In-tree `AGENT_WORKFLOW.md` is
binding; never merge to `main` without approval. The raw photo archives
(~27 GB) stay on main-pc outside git — the repo carries only optimized
images and builds without the raws.

## Claude system (workshop ops) — active

The operations brain for Claude Code sessions: numbered knowledge folders
(master context, brand/client style, quoting and pricing, woodworking,
signmaking, plastics/adhesives, finishing, ...) plus 14 agents and 13
skills under `.claude/`. Repo: **PREISS_WORKSHOP_CLAUDE_SYSTEM-** (the
trailing hyphen is part of the name; business facts inside — keep it
private). Clone to any machine where quoting/workshop sessions should run.

## Ideas / dormant

- **KilnController** — name reserved once (an empty 0-byte dir existed on
  cnc-pc). If it ever gets real, it starts life as
  `C:\Projects\KilnController` on a dev machine, with a repo from day one.
