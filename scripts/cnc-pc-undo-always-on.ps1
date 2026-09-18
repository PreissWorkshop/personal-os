# cnc-pc-undo-always-on.ps1 - take the always-on setup back OFF the shop PC.
# On 2026-09-18 scripts\main-pc-always-on.ps1 was run on DESKTOP-A60V7P2 (the
# shop PC, a HelmCNC appliance: no installs, no employee) instead of on
# main-pc, and the shop relay session was blocked by its own permission layer
# from undoing it. So this runs at the shop PC's keyboard, by Tenis, and his
# typed YES is the explicit OK the deletions need. Win+R, paste, Enter:
#
#   powershell -NoExit -ExecutionPolicy Bypass -Command "cd C:\Projects\_system\personal-os; git pull; .\scripts\cnc-pc-undo-always-on.ps1"
#
# Refuses on any other machine. In order:
# 1. stops the employee session and unregisters PreissEmployee;
# 2. removes the Telegram state dir (the bot token lives there; never read);
# 3. uninstalls the Telegram plugin (and the marketplace clone if nothing
#    else uses it) and Bun (~180 MB) with its user PATH entry;
# 4. keeps a relay: re-registers PreissRelay so it runs under this machine's
#    own name, "cnc", with permission prompts instead of auto mode, and
#    restarts it. The shop PC's old claude --remote-control autostart was not
#    running any more, so this relay is the laptop's only way in.
#    -RemoveRelay removes the relay instead.
# -DryRun prints the plan and changes nothing. Written 2026-09-18.

param(
    [switch]$RemoveRelay,
    [switch]$DryRun
)

$ErrorActionPreference = 'Continue'
. (Join-Path $PSScriptRoot 'machine-role.ps1')
. (Join-Path $PSScriptRoot 'resolve-claude.ps1')

function Say($status, $label, $detail) {
    $color = switch ($status) { 'DONE' { 'Green' } 'OK' { 'Gray' } 'SKIP' { 'Gray' } default { 'Yellow' } }
    Write-Host ("  {0,-5} {1,-18} {2}" -f $status, $label, $detail) -ForegroundColor $color
}
function Get-DirSizeMB($path) {
    if (-not (Test-Path $path)) { return 0 }
    $sum = (Get-ChildItem $path -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    return [math]::Round(($sum / 1MB), 1)
}
function Stop-ByCommandLine($name, $pattern, $label) {
    # Never this shell ($PID): the block that runs it carries the same text.
    Get-CimInstance Win32_Process -Filter "Name='$name'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like $pattern -and $_.ProcessId -ne $PID } |
        ForEach-Object {
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
            Say 'DONE' $label "stopped $name pid $($_.ProcessId)"
        }
}

if ((Get-MachineRole) -ne 'cnc') {
    Write-Host "  STOP  $env:COMPUTERNAME is not the shop PC. This undo is for DESKTOP-A60V7P2 only. Nothing changed." -ForegroundColor Red
    exit 2
}

$up          = $env:USERPROFILE
$tgDir       = Join-Path $up '.claude\channels\telegram'
$bunDir      = Join-Path $up '.bun'
$bunBin      = Join-Path $bunDir 'bin'
$plugin      = 'telegram@claude-plugins-official'
$pluginCache = Join-Path $up '.claude\plugins\cache\claude-plugins-official\telegram'
$mktDir      = Join-Path $up '.claude\plugins\marketplaces\claude-plugins-official'
$registry    = Join-Path $up '.claude\plugins\installed_plugins.json'
$relayLog    = Join-Path $up '.claude\relay-main-pc.log'
$relayScript = Join-Path $PSScriptRoot 'relay-session.ps1'
$claude      = Resolve-Claude
$freeBefore  = [math]::Round((Get-PSDrive C).Free / 1GB, 2)

Write-Host ""
Write-Host "Undo the always-on setup on $env:COMPUTERNAME (shop PC) - $(Get-Date -Format 'yyyy-MM-dd HH:mm'), user $env:USERNAME, C: free $freeBefore GB"
Write-Host ""
Write-Host "Plan:"
$emp = Get-ScheduledTask -TaskName PreissEmployee -ErrorAction SilentlyContinue
Write-Host ("  1. employee session: stop it; PreissEmployee task: {0}" -f $(if ($emp) { "unregister (state $($emp.State))" } else { 'not registered' }))
Write-Host ("  2. Telegram state dir: {0}  {1}" -f $tgDir, $(if (Test-Path $tgDir) { "remove ($((Get-ChildItem $tgDir -Force -ErrorAction SilentlyContinue | Measure-Object).Count) entries, token included)" } else { 'absent' }))
Write-Host ("  3. plugin {0}: uninstall; marketplace clone {1}: remove if unused ({2} MB); Bun {3}: remove ({4} MB) + its user PATH entry" -f $plugin, $mktDir, (Get-DirSizeMB $mktDir), $bunDir, (Get-DirSizeMB $bunDir))
if ($RemoveRelay) { Write-Host "  4. relay: stop it and unregister PreissRelay (-RemoveRelay)" }
else { Write-Host "  4. relay: re-register PreissRelay under this machine's own name 'cnc', permission prompts on, and restart it" }
Write-Host "  Not touched: C:\HelmCNC, C:\HelmCNC.bak, KMotion, backups, Signing, any other Claude session."
Write-Host ""
if ($DryRun) { Write-Host "Dry run - nothing changed."; exit 0 }

$answer = Read-Host "Type YES to do all of the above"
if ($answer -cne 'YES') { Write-Host "Not confirmed - nothing changed."; exit 1 }
Write-Host ""

# --- 1. employee ------------------------------------------------------------
Stop-ByCommandLine 'claude.exe' '*--remote-control employee*' 'employee'
Start-Sleep -Seconds 3
Stop-ByCommandLine 'powershell.exe' '*employee-session.ps1*' 'employee'
if ($emp) {
    Unregister-ScheduledTask -TaskName PreissEmployee -Confirm:$false -ErrorAction SilentlyContinue
    if (Get-ScheduledTask -TaskName PreissEmployee -ErrorAction SilentlyContinue) { Say 'FAIL' 'PreissEmployee' 'still registered' }
    else { Say 'DONE' 'PreissEmployee' 'unregistered' }
} else { Say 'OK' 'PreissEmployee' 'not registered' }

# --- 2. Telegram state (token) ----------------------------------------------
# Guard: exactly the plugin's state dir under this profile, nothing else.
if ((Test-Path $tgDir) -and ($tgDir -eq (Join-Path $up '.claude\channels\telegram'))) {
    Start-Sleep -Seconds 2   # the channel server exits shortly after its session dies
    Remove-Item $tgDir -Recurse -Force -ErrorAction SilentlyContinue
    if (Test-Path $tgDir) { Say 'FAIL' 'Telegram state' "still present: $tgDir (a process may hold it - re-run in a minute)" }
    else { Say 'DONE' 'Telegram state' 'removed, token included' }
} else { Say 'OK' 'Telegram state' 'absent' }

# --- 3. plugin, marketplace, Bun --------------------------------------------
if ($claude) {
    & $claude plugin uninstall $plugin --scope user 2>&1 | Out-Host
} else { Say 'CHECK' 'plugin' 'claude.exe not found - uninstall skipped' }
if (Test-Path $pluginCache) {
    if ($pluginCache -like '*\.claude\plugins\cache\claude-plugins-official\telegram') { Remove-Item $pluginCache -Recurse -Force -ErrorAction SilentlyContinue }
}
Say $(if (Test-Path $pluginCache) { 'FAIL' } else { 'DONE' }) 'plugin' $(if (Test-Path $pluginCache) { "cache still present: $pluginCache" } else { 'uninstalled' })

$othersUseMarketplace = $false
if (Test-Path $registry) {
    $text = Get-Content $registry -Raw
    $othersUseMarketplace = ($text -match '"[^"]+@claude-plugins-official"')
}
if ($othersUseMarketplace) {
    Say 'OK' 'marketplace' 'kept - other plugins from it are installed'
} elseif (Test-Path $mktDir) {
    if ($claude) { & $claude plugin marketplace remove claude-plugins-official 2>&1 | Out-Host }
    if ((Test-Path $mktDir) -and ($mktDir -like '*\.claude\plugins\marketplaces\claude-plugins-official')) { Remove-Item $mktDir -Recurse -Force -ErrorAction SilentlyContinue }
    Say $(if (Test-Path $mktDir) { 'FAIL' } else { 'DONE' }) 'marketplace' $(if (Test-Path $mktDir) { "still present: $mktDir" } else { 'removed' })
} else { Say 'OK' 'marketplace' 'absent' }

# Guard: ~\.bun with bun.exe inside it, nothing else.
if ((Test-Path (Join-Path $bunBin 'bun.exe')) -and ($bunDir -eq (Join-Path $up '.bun'))) {
    Remove-Item $bunDir -Recurse -Force -ErrorAction SilentlyContinue
    Say $(if (Test-Path $bunDir) { 'FAIL' } else { 'DONE' }) 'Bun' $(if (Test-Path $bunDir) { "still present: $bunDir" } else { 'removed' })
} else { Say 'OK' 'Bun' 'absent' }
# The installer put ~\.bun\bin on the user PATH (registry). Take exactly that
# entry out, keeping the value's registry type as it was.
try {
    $envKey = Get-Item 'HKCU:\Environment'
    $raw = $envKey.GetValue('Path', '', 'DoNotExpandEnvironmentNames')
    $kind = $envKey.GetValueKind('Path').ToString()
    $parts = @($raw -split ';' | Where-Object { $_ })
    $kept = @($parts | Where-Object { ([Environment]::ExpandEnvironmentVariables($_)).TrimEnd('\') -ine $bunBin })
    if ($kept.Count -ne $parts.Count) {
        Set-ItemProperty -Path 'HKCU:\Environment' -Name Path -Value ($kept -join ';') -Type $kind
        Say 'DONE' 'user PATH' "removed $bunBin (new windows see it after the next logon)"
    } else { Say 'OK' 'user PATH' 'no Bun entry' }
    if ($null -ne $envKey.GetValue('BUN_INSTALL', $null)) { Remove-ItemProperty -Path 'HKCU:\Environment' -Name BUN_INSTALL; Say 'DONE' 'BUN_INSTALL' 'removed' }
} catch { Say 'CHECK' 'user PATH' "could not edit it: $($_.Exception.Message)" }

# --- 4. relay ---------------------------------------------------------------
Stop-ScheduledTask -TaskName PreissRelay -ErrorAction SilentlyContinue
Stop-ByCommandLine 'powershell.exe' '*relay-session.ps1*' 'relay'      # the restart loop first
Stop-ByCommandLine 'claude.exe' '*--remote-control main-pc*' 'relay'   # then the wrongly named session
if (Test-Path $relayLog) { Remove-Item $relayLog -Force -ErrorAction SilentlyContinue }
if ($RemoveRelay) {
    Unregister-ScheduledTask -TaskName PreissRelay -Confirm:$false -ErrorAction SilentlyContinue
    Say $(if (Get-ScheduledTask -TaskName PreissRelay -ErrorAction SilentlyContinue) { 'FAIL' } else { 'DONE' }) 'PreissRelay' 'unregistered'
} else {
    # No -Name: relay-session.ps1 derives "cnc" from the hostname and keeps
    # permission prompts on this machine.
    $action = New-ScheduledTaskAction -Execute 'powershell.exe' `
        -Argument "-NoLogo -NoProfile -WindowStyle Minimized -ExecutionPolicy Bypass -File `"$relayScript`"" `
        -WorkingDirectory $up
    $trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
        -ExecutionTimeLimit ([TimeSpan]::Zero) -StartWhenAvailable -MultipleInstances IgnoreNew
    try {
        Register-ScheduledTask -TaskName PreissRelay -Action $action -Trigger $trigger -Settings $settings `
            -RunLevel Limited -Force -ErrorAction Stop `
            -Description "Keeps 'claude --remote-control cnc' alive from logon so the laptop can reach the shop PC; permission prompts on. personal-os scripts\cnc-pc-undo-always-on.ps1" | Out-Null
        Start-ScheduledTask -TaskName PreissRelay
        Start-Sleep -Seconds 4
        $relay = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object { $_.CommandLine -like '*relay-session.ps1*' } | Select-Object -First 1
        if ($relay) { Say 'DONE' 'PreissRelay' "re-registered as 'cnc' with prompts, running (pid $($relay.ProcessId))" }
        else { Say 'FAIL' 'PreissRelay' 're-registered but no process - Get-ScheduledTaskInfo PreissRelay' }
    } catch { Say 'FAIL' 'PreissRelay' $_.Exception.Message }
}

# --- report -----------------------------------------------------------------
Write-Host ""
Write-Host "After:"
Get-ScheduledTask -TaskName PreissEmployee, PreissRelay -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  task $($_.TaskName): $($_.State)" }
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(claude|bun|powershell)\.exe$' -and $_.CommandLine -match 'relay-session|employee-session|remote-control|server\.ts' -and $_.ProcessId -ne $PID } |
    ForEach-Object { Write-Host ("  {0} {1} :: {2}" -f $_.ProcessId, $_.Name, $_.CommandLine.Substring(0, [Math]::Min(120, $_.CommandLine.Length))) }
Write-Host ("  C: free {0} GB -> {1} GB" -f $freeBefore, [math]::Round((Get-PSDrive C).Free / 1GB, 2))
Write-Host ""
Write-Host "The shop PC now shows up as 'cnc' in ListAgents on the laptop. Next: the same bootstrap paste on main-pc (PREISSWORKSHOP)."
Write-Host ""
