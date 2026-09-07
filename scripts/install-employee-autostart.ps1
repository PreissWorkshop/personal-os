# install-employee-autostart.ps1 - run the employee session at logon on main-pc.
# Per-user scheduled task, minimized, no elevation. Written 2026-09-07.
# Mirrors the shop PC's `claude --remote-control` autostart pattern.
# Remove with:  Unregister-ScheduledTask -TaskName PreissEmployee -Confirm:$false

$ErrorActionPreference = 'Stop'

$taskName = 'PreissEmployee'
$script   = 'C:\Projects\_system\personal-os\scripts\employee-session.ps1'

if (-not (Test-Path $script)) { Write-Error "Not found: $script - run git pull in personal-os first." }

$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Task '$taskName' already exists - replacing it."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument "-NoLogo -WindowStyle Minimized -ExecutionPolicy Bypass -File `"$script`"" `
    -WorkingDirectory 'C:\Projects\_system\personal-os'

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

# Never stop it for being long-running or for running on battery: it is
# supposed to sit there for days.
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5) `
    -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -RunLevel Limited `
    -Description 'Preiss Workshop employee: always-on Claude Code session rooted in personal-os, Telegram channel enabled. See docs/employee-setup-main-pc.md.' | Out-Null

Write-Host "Registered '$taskName' - runs at logon for $env:USERNAME." -ForegroundColor Green
Write-Host "Start it now without logging out:  Start-ScheduledTask -TaskName $taskName"
Write-Host "Check it:                          Get-ScheduledTaskInfo -TaskName $taskName"
