# employee-session.ps1 - start the always-on employee session on main-pc.
# Rooted in personal-os, Telegram channel enabled, permission mode auto; it is
# Remote Control session "employee" in claude.ai/code. It restarts itself
# when the session exits (/exit in its window = fresh session in 30 s); to
# stop it for good: Disable-ScheduledTask PreissEmployee, then close the window.
# Written 2026-09-07, launch line fixed 2026-09-17, auto mode + loop 2026-09-18.
# See docs/employee-setup-main-pc.md and docs/employee.md.

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'machine-role.ps1')
Assert-AgentHost 'The employee'
$repo = 'C:\Projects\_system\personal-os'

if (-not (Test-Path (Join-Path $repo '.git'))) {
    Write-Error "personal-os not found at $repo - clone it first (docs/bootstrap-new-machine.md)."
}
Set-Location $repo

. (Join-Path $PSScriptRoot 'resolve-claude.ps1')
$claude = Resolve-Claude
if (-not $claude) { Write-Error "Claude Code not found. Run scripts\employee-preflight.ps1." }

# No bot token, no channel: refuse rather than park a deaf session at logon.
$envFile = Join-Path $env:USERPROFILE '.claude\channels\telegram\.env'
if (-not (Test-Path $envFile)) {
    Write-Error "No Telegram bot token on this machine ($envFile). Do docs/employee-setup-main-pc.md steps 2-3 first."
}

# The channel server runs on Bun, which may have been installed minutes ago
# by the bootstrap: make sure this process can see it.
$bunDir = Join-Path $env:USERPROFILE '.bun\bin'
if ((Test-Path $bunDir) -and -not (Get-Command bun -ErrorAction SilentlyContinue)) { $env:PATH = "$bunDir;$env:PATH" }

# Routines and channels both require the claude.ai login; an API key env var
# silently outranks it, so clear it for this process only.
if ($env:ANTHROPIC_API_KEY)    { Remove-Item Env:\ANTHROPIC_API_KEY }
if ($env:ANTHROPIC_AUTH_TOKEN) { Remove-Item Env:\ANTHROPIC_AUTH_TOKEN }

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

# `--channels` is variadic: without the `--` it swallows the brief as a second
# channel and the CLI exits with "--channels entries must be tagged" - the
# 2026-09-07 line never could have started. `--remote-control employee` is
# what makes the phone approvals above possible. Order verified 2026-09-17.
# The plugin is DISABLED user-wide on purpose (main-pc-always-on.ps1): with a
# token, every session that loads it polls the bot, and Telegram allows one
# poller per bot. `--settings` enables it for this session only - verified
# 2026-09-18 that `--channels` alone does not load a disabled plugin.
# Permission mode `auto` (Tenis 2026-09-18): unattended work runs without
# prompts; the auto-mode classifier still blocks risky actions.
$settings = Join-Path $PSScriptRoot 'employee-settings.json'

# Restart loop, same as relay-session.ps1: a session that exits (or that
# started before a login existed, 2026-09-18) comes back by itself in 30 s.
# Start/exit lines go to a log; Claude's own output is never logged.
$log = Join-Path $env:USERPROFILE '.claude\employee.log'
function Log($text) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $text"
    Write-Host $line
    try { Add-Content -Path $log -Value $line -Encoding ascii } catch { }
}
# 'Continue' from here: under 'Stop', PowerShell 5.1 turns git's ordinary
# stderr chatter into a terminating error and the pull reads as failed.
$ErrorActionPreference = 'Continue'
while ($true) {
    # Start from current origin so the employee reads today's rules, not last week's.
    git pull --ff-only --quiet
    if ($LASTEXITCODE -ne 0) { Log "git pull failed; continuing on the local tree." }

    Log "starting: $claude --remote-control employee --permission-mode auto --settings $settings --channels plugin:telegram@claude-plugins-official"
    $started = Get-Date
    & $claude --remote-control employee --permission-mode auto --settings $settings --channels plugin:telegram@claude-plugins-official -- $brief
    $code = $LASTEXITCODE
    $ran = ((Get-Date) - $started).TotalSeconds

    # A session that dies at once (logged out, broken plugin) must not spin.
    $wait = if ($ran -lt 60) { 300 } else { 30 }
    Log ("session ended after {0:N0} s (exit {1}); restarting in {2} s. Close this window to stop." -f $ran, $code, $wait)
    Start-Sleep -Seconds $wait
}
