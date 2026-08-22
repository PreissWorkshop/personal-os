# Bootstrap a new machine (Windows)

Target: the Samsung laptop (vacation) and main-pc. ~30–45 minutes.

## Paste this into Claude Code on the new machine

> You're on Tenis's laptop (fresh Windows) — set it up for ScanPen + HelmCNC code
> work away from the shop. Everything lives under github.com/PreissWorkshop.
>
> 1. Verify/install: Git for Windows, Python 3.11.x, VS Code. Tell me what you
>    can't install yourself.
> 2. Clone the control layer first (I'll complete the GitHub browser sign-in when
>    the first private clone asks):
>    `git clone https://github.com/PreissWorkshop/personal-os C:\Projects\_system\personal-os`
> 3. Read its README.md and registry/projects.yaml, then follow
>    docs/bootstrap-new-machine.md exactly — it clones every project at its
>    laptop root and runs each one's readiness check: scanpen (pytest +
>    selftest green = machine ready), helmcnc-app, the website (build.py →
>    "Build OK"), the workshop Claude system.
> 4. Rules that don't bend: read each repo's CLAUDE.md / in-tree workflow docs
>    before touching it (HelmCNC: top of HELMCNC_NOTES.md first; website:
>    AGENT_WORKFLOW.md + FABLE-HANDOFF.md are binding, and main never merges
>    without Tenis's OK). The HelmCNC test gate is `HelmSelfTest.exe offline` —
>    NEVER run it without arguments. Release/promote scripts never run
>    off-shop. Big media (ScanPen captures, website photo raws) is
>    deliberately not in git — never commit media.
> 5. Report back: installed versions, each project's check result, and the top
>    HELMCNC_NOTES entry, so Tenis knows exactly where work stands.

## The steps themselves

1. **Install**: Git for Windows, VS Code, Python 3.11.x, Claude Code
   (claude.com/claude-code — desktop app or CLI). Optional but handy:
   GitHub Desktop (easiest sign-in) and the `gh` CLI.
   On **main-pc** additionally: Node.js LTS and the `gh` CLI are wanted —
   the agent/automation phase runs there (never on the shop PC).
2. **Sign in to GitHub once** — GitHub Desktop login, or just run the first
   `git push`/private clone and complete the credential-manager browser flow.
3. **Control layer first**:

       mkdir C:\Projects\_system
       git clone https://github.com/PreissWorkshop/personal-os C:\Projects\_system\personal-os

   Read its README.md — it maps everything else.
4. **ScanPen**:

       mkdir C:\Projects\ScanPen
       git clone https://github.com/PreissWorkshop/scanpen C:\Projects\ScanPen\repo
       cd C:\Projects\ScanPen\repo
       pip install -r requirements.txt
       python -m pytest -q                 # suite green = machine ready
       python -m scanpen.selftest --full   # full audit

   Real-footage work (`fieldmeasure`, replay) additionally needs capture
   clips — copy the takes you need from the USB stick
   (`D:\ScanPen-backup-2026-08-16\capture`) or from the shop PC. They are
   deliberately not in git.
5. **HelmCNC code work** (optional, off-shop):

       git clone https://github.com/PreissWorkshop/helmcnc-app C:\Projects\HelmCNC\app

   Building needs the roslyn toolset restored first — the how-to sits at the
   top of the repo's `.gitignore` (Microsoft.Net.Compilers 4.8.0 nupkg from
   nuget.org, unzipped so `csc.exe` lands at `tools/roslyn/tasks/net472/csc.exe`),
   then `build.cmd ReleaseNew`. The test gate on ANY machine is
   `HelmSelfTest.exe offline` — never no-args (that form is the live-board
   test on the shop PC; keep the habit machine-independent). Read
   `HELMCNC_NOTES.md` (top section) and `CLAUDE.md` before working; the
   release/promote scripts run only at the shop-PC console. Nothing built
   off-shop touches the machine except through the documented deploy on the
   shop PC.
6. **Preiss Workshop website** (optional — homepage work):

       git clone https://github.com/PreissWorkshop/preiss-workshop-website C:\Projects\PreissWebsite\website
       cd C:\Projects\PreissWebsite\website
       git checkout feature/fable-design-refinement
       python src\site\build.py              # expect "Build OK - ... pages"
       python -m http.server 8790 -d public  # preview at http://localhost:8790

   Stdlib Python only, nothing to pip-install. Read `AGENT_WORKFLOW.md` and
   `FABLE-HANDOFF.md` before changing anything — they are binding. The raw
   photo archives (`PHOTOS_RAW`, `photos_new` — ~27 GB) are deliberately not
   in git and exist only on main-pc; the repo's optimized images are all the
   site needs.
7. **Workshop Claude system** (quoting/ops sessions):

       git clone https://github.com/PreissWorkshop/PREISS_WORKSHOP_CLAUDE_SYSTEM- C:\Projects\PreissClaudeSystem\repo
       git -C C:\Projects\PreissClaudeSystem\repo config core.fileMode false

   The trailing hyphen is part of the repo name. Knowledge base + 14
   agents + 13 skills; open Claude Code at that root for quoting and
   workshop-operations work.
8. **Open Claude Code at `C:\Projects\_system\personal-os`** and say what
   you're working on — the registry and docs do the rest.
