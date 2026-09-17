# main-pc-always-on.ps1 - make this machine the always-on agent host.
# Run once at main-pc, in a normal (not admin) PowerShell window:
#
#   cd C:\Projects\_system\personal-os; git pull; powershell -ExecutionPolicy Bypass -File scripts\main-pc-always-on.ps1
#
# 1. Checks Claude Code: found, >= 2.1.234 (Remote Control on Windows), and a
#    CLI login exists (file existence only - never read).
# 2. Registers PreissRelay: at every logon, scripts\relay-session.ps1 keeps a
#    `claude --remote-control main-pc` session alive, and starts it now. From
#    then on the laptop reaches this PC by SendMessage and the phone through
#    claude.ai/code. It replaces the laptop's dead "Claude Relay" task.
# 3. Employee prerequisites (docs/employee-setup-main-pc.md steps 1 and 3):
#    Bun and the Telegram channel plugin, installed if missing.
# 4. Reports whether this PC sleeps. An asleep host is an offline relay.
# It does NOT start the employee: that needs the Telegram bot token first
# (setup doc steps 2-5). Idempotent - safe to re-run. Written 2026-09-17.

param(
    [string]$RelayName = 'main-pc',
    [switch]$NoInstalls
)

$ErrorActionPreference = 'Continue'
. (Join-Path $PSScriptRoot 'resolve-claude.ps1')
$todo = @()

function Say($status, $label, $detail) {
    $color = switch ($status) { 'OK' { 'Gray' } 'DONE' { 'Green' } 'SKIP' { 'Gray' } default { 'Yellow' } }
    Write-Host ("  {0,-5} {1,-17} {2}" -f $status, $label, $detail) -ForegroundColor $color
}

Write-Host ""
Write-Host "main-pc always-on setup - $(Get-Date -Format 'yyyy-MM-dd HH:mm') on $env:COMPUTERNAME"
Write-Host ""

# --- 1. Claude Code -----------------------------------------------------------
$claude = Resolve-Claude
if (-not $claude) {
    Say 'MISS' 'Claude Code' 'not on PATH, not in ~\.local\bin, not inside the Claude app'
    Write-Host ""
    Write-Host "Install it, then run this script again:  irm https://claude.ai/install.ps1 | iex" -ForegroundColor Yellow
    exit 1
}
$versionText = (& $claude --version 2>$null | Select-Object -First 1)
[version]$version = '0.0'
if ("$versionText" -match '(\d+\.\d+\.\d+)') { [void][version]::TryParse($Matches[1], [ref]$version) }
if ($version -ge [version]'2.1.234') {
    Say 'OK' 'Claude Code' "$version  $claude"
} else {
    Say 'WARN' 'Claude Code' "'$versionText' - Remote Control on Windows needs 2.1.234 or later"
    $todo += "update Claude Code ($claude update), then run this script again"
}

if (Test-Path (Join-Path $env:USERPROFILE '.claude\.credentials.json')) {
    Say 'OK' 'CLI login' 'present'
} else {
    Say 'WARN' 'CLI login' 'none yet - the relay window will ask you to log in, once'
    $todo += "log in once in the 'Claude relay' window (taskbar)"
}

# --- 2. Relay autostart -------------------------------------------------------
$taskName = 'PreissRelay'
$launcher = Join-Path $PSScriptRoot 'relay-session.ps1'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument "-NoLogo -NoProfile -WindowStyle Minimized -ExecutionPolicy Bypass -File `"$launcher`" -Name $RelayName" `
    -WorkingDirectory $env:USERPROFILE
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
# Never stopped for running long or on battery: it is meant to sit there for days.
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) -StartWhenAvailable -MultipleInstances IgnoreNew
try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings `
        -RunLevel Limited -Force -ErrorAction Stop `
        -Description "Keeps 'claude --remote-control $RelayName' alive from logon so the laptop and the phone can reach this PC. personal-os scripts\main-pc-always-on.ps1" | Out-Null
    Say 'DONE' 'PreissRelay task' "at logon -> relay-session.ps1 -Name $RelayName"
} catch {
    Say 'FAIL' 'PreissRelay task' $_.Exception.Message
    $todo += 'PreissRelay was not registered - see the error above'
}

$relay = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like '*relay-session.ps1*' } | Select-Object -First 1
if ($relay) {
    Say 'OK' 'relay session' "already running (pid $($relay.ProcessId))"
} else {
    Start-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    Say 'DONE' 'relay session' "started - minimized window 'Claude relay ($RelayName)' in the taskbar"
}

# --- 3. Employee prerequisites ------------------------------------------------
if ($NoInstalls) {
    Say 'SKIP' 'Bun, plugin' '-NoInstalls'
} else {
    $bun = (Get-Command bun -ErrorAction SilentlyContinue).Source
    if (-not $bun -and (Test-Path (Join-Path $env:USERPROFILE '.bun\bin\bun.exe'))) {
        $bun = Join-Path $env:USERPROFILE '.bun\bin\bun.exe'
    }
    if ($bun) {
        Say 'OK' 'Bun' $bun
    } else {
        Write-Host "  ...   installing Bun with the official installer (bun.sh)"
        # Child process: an installer that calls `exit` must not end this script.
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://bun.sh/install.ps1 | iex"
        if (Test-Path (Join-Path $env:USERPROFILE '.bun\bin\bun.exe')) { Say 'DONE' 'Bun' 'installed' }
        else { Say 'FAIL' 'Bun' 'installer did not leave ~\.bun\bin\bun.exe'; $todo += 'install Bun:  irm bun.sh/install.ps1 | iex' }
    }

    $plugin = 'telegram@claude-plugins-official'
    $registry = Join-Path $env:USERPROFILE '.claude\plugins\installed_plugins.json'
    $installed = (Test-Path $registry) -and ((Get-Content $registry -Raw) -match [regex]::Escape("`"$plugin`""))
    if ($installed) {
        Say 'OK' 'Telegram plugin' 'installed'
    } else {
        Write-Host "  ...   installing $plugin (user scope)"
        & $claude plugin install $plugin --scope user --yes | Out-Host
        if ($LASTEXITCODE -ne 0) {
            & $claude plugin marketplace add anthropics/claude-plugins-official | Out-Host
            & $claude plugin install $plugin --scope user --yes | Out-Host
        }
        if ($LASTEXITCODE -eq 0) { Say 'DONE' 'Telegram plugin' 'installed' }
        else { Say 'FAIL' 'Telegram plugin' 'see the output above'; $todo += "install the plugin:  claude plugin install $plugin --scope user --yes" }
    }
}

# --- 4. Sleep -----------------------------------------------------------------
foreach ($setting in @(@('STANDBYIDLE', 'sleep on AC', 'standby-timeout-ac'), @('HIBERNATEIDLE', 'hibernate on AC', 'hibernate-timeout-ac'))) {
    $query = powercfg /query SCHEME_CURRENT SUB_SLEEP $setting[0] 2>$null
    $match = $query | Select-String 'AC Power Setting Index:\s*0x([0-9a-fA-F]+)' | Select-Object -First 1
    if (-not $match) {
        Say 'CHECK' $setting[1] "could not read it - check: powercfg /query SCHEME_CURRENT SUB_SLEEP $($setting[0])"
        continue
    }
    $seconds = [Convert]::ToInt32($match.Matches[0].Groups[1].Value, 16)
    if ($seconds -eq 0) {
        Say 'OK' $setting[1] 'never'
    } else {
        Say 'WARN' $setting[1] ("after {0} min - asleep means the relay is offline" -f [math]::Round($seconds / 60))
        $todo += "your call - keep it awake on mains power:  powercfg /change $($setting[2]) 0"
    }
}

# --- Summary ------------------------------------------------------------------
Write-Host ""
Write-Host "The relay shows up as '$RelayName' - in ListAgents on the laptop, in claude.ai/code on the phone."
Write-Host "First start only: if the relay window asks to log in or to trust the folder, answer it once."
Write-Host "After a reboot it returns when someone logs in to Windows (logon task)."
if ($todo.Count -gt 0) {
    Write-Host ""
    Write-Host "Still to do:" -ForegroundColor Yellow
    $todo | ForEach-Object { Write-Host "  - $_" }
}
Write-Host ""
Write-Host "Next, for the employee: docs\employee-setup-main-pc.md steps 2-5 (bot token, pair, autostart)."
Write-Host ""
