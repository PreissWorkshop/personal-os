# personal-os — agent instructions

You are working in the control layer for Tenis Preiss's projects. This repo
is the source of truth for the machine map, project registry, and
cross-project plans. Local session memory is cache; this repo is truth.

## First moves in any session here

1. Read `registry/projects.yaml` — what exists and where it lives on the
   machine you're on.
2. Read `docs/migration-plan.md` — current cross-project state and queue.
3. If the task belongs to ONE project, say so and have Tenis run it in that
   project's root (one session, one project). Sessions here are for
   cross-project coordination, planning, and this repo's own docs.

## Hard rules

- **No secrets in this repo, ever** — no tokens, keys, or values quoted from
  `C:\HelmCNC-Signing` or anywhere else. Locations may be named; contents
  may not be read or reproduced.
- **Machine roles are law**: cnc-pc = HelmCNC appliance (weak, low disk — no
  new installs, no heavy data); main-pc + laptop = development. The
  grandfathered shop-PC roots in `docs/architecture.md` are deliberate —
  never "clean them up".
- **Production is untouchable**: `C:\HelmCNC`, KMotion, FlexiCAM amp
  backups, state backups, Signing folders.
- **Destructive actions** (delete / move / history rewrite) need Tenis's
  explicit OK — and a verification guard immediately before execution, even
  for things "verified earlier".
- A session that changed this repo ends with a commit AND a push, and keeps
  `docs/migration-plan.md` current — it is the living tracker.

## Writing style here

Concise, factual, dated; overwrite stale statements rather than accumulating
history (git keeps the history). Session reports go to
`docs/reports/YYYY-MM-DD-<topic>.md`.
