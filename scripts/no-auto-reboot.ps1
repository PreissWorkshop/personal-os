# no-auto-reboot.ps1 - stop Windows Update from restarting main-pc on its own.
# Written 2026-09-19 after KB5129195 rebooted PREISSWORKSHOP at 22:10 on 09-18
# and the employee stayed down until Tenis logged on at 09:37.
#
# Run ELEVATED on main-pc only. Never on cnc-pc (machine roles are law).
#   powershell -ExecutionPolicy Bypass -File scripts\no-auto-reboot.ps1          # apply
#   powershell -ExecutionPolicy Bypass -File scripts\no-auto-reboot.ps1 -Undo    # back to Windows defaults
#
# What it sets (registry only, fully reversible with -Undo):
#   1. AUOptions=2  - Windows tells you an update is ready; it does not download
#                     or install until you click. No install = no pending restart.
#   2. NoAutoRebootWithLoggedOnUsers=1 - belt and braces while a user is logged on
#                     (a locked session counts as logged on).
#   3. Active hours 08:00-02:00 (18 h is the maximum Windows allows), smart
#                     active hours off, restart notifications on.
# Windows 11 HOME does not officially support these policies. The script reads the
# effective setting back through the Windows Update agent and prints it - trust
# that line, not this comment.
param([switch]$Undo, [string]$Log)

if ($Log) { Start-Transcript -Path $Log -Force | Out-Null }
$ErrorActionPreference = 'Stop'

if ($env:COMPUTERNAME -ne 'PREISSWORKSHOP') { Write-Output "REFUSED: this is $env:COMPUTERNAME, not main-pc."; if ($Log) { Stop-Transcript | Out-Null }; exit 2 }
$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $admin) { Write-Output "REFUSED: not elevated."; if ($Log) { Stop-Transcript | Out-Null }; exit 3 }

$wu = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate'
$au = "$wu\AU"
$ux = 'HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings'

if ($Undo) {
    if (Test-Path $au) { Remove-Item $au -Recurse -Force -Confirm:$false }
    foreach ($n in 'SetActiveHours','ActiveHoursStart','ActiveHoursEnd') { Remove-ItemProperty -Path $wu -Name $n -ErrorAction SilentlyContinue }
    Set-ItemProperty -Path $ux -Name SmartActiveHoursState -Value 1 -Type DWord
    Write-Output "UNDONE: update policy keys removed; Windows defaults apply."
} else {
    New-Item -Path $au -Force | Out-Null
    Set-ItemProperty -Path $au -Name NoAutoUpdate                  -Value 0 -Type DWord
    Set-ItemProperty -Path $au -Name AUOptions                     -Value 2 -Type DWord
    Set-ItemProperty -Path $au -Name NoAutoRebootWithLoggedOnUsers -Value 1 -Type DWord
    Set-ItemProperty -Path $wu -Name SetActiveHours   -Value 1 -Type DWord
    Set-ItemProperty -Path $wu -Name ActiveHoursStart -Value 8 -Type DWord
    Set-ItemProperty -Path $wu -Name ActiveHoursEnd   -Value 2 -Type DWord
    Set-ItemProperty -Path $ux -Name ActiveHoursStart             -Value 8 -Type DWord
    Set-ItemProperty -Path $ux -Name ActiveHoursEnd               -Value 2 -Type DWord
    Set-ItemProperty -Path $ux -Name SmartActiveHoursState        -Value 0 -Type DWord
    Set-ItemProperty -Path $ux -Name RestartNotificationsAllowed2 -Value 1 -Type DWord
    Write-Output "APPLIED."
}

Write-Output "--- read-back"
if (Test-Path $au) { Get-ItemProperty $au | Select-Object NoAutoUpdate, AUOptions, NoAutoRebootWithLoggedOnUsers | Format-List | Out-String | Write-Output }
Get-ItemProperty $ux | Select-Object ActiveHoursStart, ActiveHoursEnd, SmartActiveHoursState, RestartNotificationsAllowed2 | Format-List | Out-String | Write-Output
try {
    $lvl = (New-Object -ComObject Microsoft.Update.AutoUpdate).Settings.NotificationLevel
    Write-Output "EFFECTIVE NotificationLevel (agent's own view): $lvl   [2 = notify before download, 4 = fully automatic, 0 = not configured]"
} catch { Write-Output "Could not read the agent's effective setting: $_" }
if ($Log) { Stop-Transcript | Out-Null }
