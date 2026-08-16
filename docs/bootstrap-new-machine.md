# Bootstrap a new machine (Windows)

Target: the Samsung laptop (vacation) and main-pc. ~30–45 minutes.

1. **Install**: Git for Windows, VS Code, Python 3.11.x, Claude Code
   (claude.com/claude-code — desktop app or CLI). Optional but handy:
   GitHub Desktop (easiest sign-in) and the `gh` CLI.
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

   Building needs the roslyn toolset restored per the repo's `.gitignore`
   note. Nothing built off-shop touches the machine except through the
   documented deploy on the shop PC.
6. **Open Claude Code at `C:\Projects\_system\personal-os`** and say what
   you're working on — the registry and docs do the rest.
