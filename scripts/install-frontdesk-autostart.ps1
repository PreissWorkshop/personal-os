# install-frontdesk-autostart.ps1 - run the front desk at logon on main-pc.
# Per-user scheduled task, minimized, no elevation. Mirrors
# install-employee-autostart.ps1 exactly. Written 2026-09-18.
# Remove with:  Unregister-ScheduledTask -TaskName PreissFrontDesk -Confirm:$false
#
# Note the order this creates: once PreissFrontDesk exists and is enabled,
# employee-session.ps1 detects it and starts the employee WITHOUT the Telegram
# channel, because one bot token allows exactly one poller. So after running
# this, restart the employee task as well - the last lines say how.

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'machine-role.ps1')
Assert-AgentHost 'The front desk autostart'

$taskName = 'PreissFrontDesk'
$repo     = 'C:\Projects\_system\personal-os'
$script   = Join-Path $repo 'scripts\frontdesk-session.ps1'

if (-not (Test-Path $script)) { Write-Error "Not found: $script - run git pull in personal-os first." }

$envFile = Join-Path $env:USERPROFILE '.claude\frontdesk\.env'
if (-not (Test-Path $envFile)) {
    Write-Warning "No secrets at $envFile yet. Run scripts\frontdesk-set-key.ps1, or the task will exit at every logon."
}

$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Task '$taskName' already exists - replacing it."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument "-NoLogo -WindowStyle Minimized -ExecutionPolicy Bypass -File `"$script`"" `
    -WorkingDirectory $repo

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

# Never stop it for being long-running or for running on battery: it is
# supposed to sit there for days holding the phone.
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5) `
    -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Settings $settings -RunLevel Limited `
    -Description 'Preiss Workshop front desk: the fast agent that owns the Telegram bot and delegates real work to a Claude Code session. See docs/frontdesk.md.' | Out-Null

Write-Host "Registered '$taskName' - runs at logon for $env:USERNAME." -ForegroundColor Green
Write-Host ""
Write-Host "Now hand the phone over, so the two do not fight for the bot:" -ForegroundColor Cyan
Write-Host "  Start-ScheduledTask -TaskName $taskName"
Write-Host "  Stop-ScheduledTask  -TaskName PreissEmployee; Start-ScheduledTask -TaskName PreissEmployee"
Write-Host ""
Write-Host "The front desk window prints a pairing code; send it '/pair <code>' from your phone."
Write-Host "Check it:  Get-ScheduledTaskInfo -TaskName $taskName"
