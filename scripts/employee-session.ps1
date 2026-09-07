# employee-session.ps1 - start the always-on employee session on main-pc.
# Rooted in personal-os, Telegram channel enabled, permission prompts INTACT
# (approve from the phone via Remote Control). Written 2026-09-07.
# See docs/employee-setup-main-pc.md and docs/employee.md.

$ErrorActionPreference = 'Stop'
$repo = 'C:\Projects\_system\personal-os'

if (-not (Test-Path (Join-Path $repo '.git'))) {
    Write-Error "personal-os not found at $repo - clone it first (docs/bootstrap-new-machine.md)."
}
Set-Location $repo

# Resolve claude.exe: PATH first, then the usual per-user install.
$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) {
    $candidate = Join-Path $env:USERPROFILE '.local\bin\claude.exe'
    if (Test-Path $candidate) { $claude = $candidate }
}
if (-not $claude) { Write-Error "Claude Code not found. Run scripts\employee-preflight.ps1." }

# Routines and channels both require the claude.ai login; an API key env var
# silently outranks it, so clear it for this process only.
if ($env:ANTHROPIC_API_KEY)    { Remove-Item Env:\ANTHROPIC_API_KEY }
if ($env:ANTHROPIC_AUTH_TOKEN) { Remove-Item Env:\ANTHROPIC_AUTH_TOKEN }

# Start from current origin so the employee reads today's rules, not last week's.
try { git pull --ff-only 2>&1 | Out-Null } catch { Write-Warning "git pull failed; continuing on the local tree." }

$brief = @'
You are the employee. Read docs/employee.md in this repo now, then
registry/projects.yaml and docs/migration-plan.md, and work by those rules
for the rest of this session.

You are reachable from Tenis's phone over the Telegram channel and will get
messages while he is away from the keyboard. Answer in at most five lines;
put detail in the repo, not the message.

Standing duties between his messages:
- Keep docs/migration-plan.md current. It is the living tracker.
- Review the cloud routines' overnight runs and surface anything that needs
  a decision. Do not repeat a report he has already seen.
- File work that needs a machine you are not on as a GitHub issue on
  PreissWorkshop/personal-os, labelled machine:main-pc / machine:cnc-pc /
  machine:any, with everything needed to act in the body.
- Push whatever you commit before the session ends.

Do not ship HelmCNC, merge the website to main, take destructive action, or
touch production without his explicit OK. No secrets, ever. A missed
threshold is reported, never loosened.

Start by telling him, in five lines or fewer: what the routines found since
the last sitting, the open needs-Tenis items, and the single thing most worth his
attention today.
'@

Write-Host "Starting the employee session in $repo ..." -ForegroundColor Green
& $claude --channels plugin:telegram@claude-plugins-official $brief
