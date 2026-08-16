# Architecture

## Principles

1. **GitHub is the source of truth.** A dead computer should cost hours, not
   work. Every session that produces commits ends with a push.
2. **Machines have roles.** The shop PC is a HelmCNC appliance (weak, low
   disk, runs the machine). Heavy dev, media, business, and agent work happen
   on main-pc / laptop.
3. **Separate the categories** — source code, project docs, project assets,
   local/generated data, backups, installed software, the AI layer, business
   data. A git repo carries source-controlled material only; generated, heavy,
   or machine-local files stay out (enforced by .gitignore, documented per
   project).
4. **Local paths are per-machine, registered, and stable.** New machines use
   the clean layout below. Live roots on the shop PC are **grandfathered** —
   the registry, not uniformity, is what prevents chaos.
5. **Archives get dates, not deletions.** Old versions become
   `Name-YYYY-MM-DD` archives; duplicates are reported, never auto-cleaned.

## The clean layout (main-pc, laptop, all future machines)

    C:\Projects\
    ├── _system\personal-os\      # this repo — always clone first
    ├── ScanPen\repo\             # + docs\ assets\ local\ added when they become real
    ├── HelmCNC\app\              # optional off-shop clone
    │           site\
    └── <FutureProject>\

Only create subfolders (docs/assets/local) when real content exists for them.

## Grandfathered roots (cnc-pc only)

`C:\HelmCNC.bak` (HelmCNC dev) and `C:\ScanPen` (frozen archive) stay where
they are. Moving them would break: linked git worktrees (absolute paths in
both directions), per-root Claude session memory, the documented
build→hot-swap deploy procedure, and emergency muscle memory on a production
machine — for zero functional gain. GitHub makes the work portable; the
registry makes the roots findable.

## Why personal-os sits above the projects

It carries what no single project should: the machine map, the project
registry, security policy, agent behavior, and cross-project plans. An agent
on ANY machine reads this repo first and knows the world; per-machine session
memory is cache, this repo is truth.
