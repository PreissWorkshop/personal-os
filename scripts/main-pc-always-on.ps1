# main-pc-always-on.ps1 - make this machine the always-on agent host.
# Run once at main-pc: Win+R, paste, Enter:
#
#   powershell -NoExit -ExecutionPolicy Bypass -Command "cd C:\Projects\_system\personal-os; git pull; .\scripts\main-pc-always-on.ps1"
#
# 1. Checks Claude Code: found, >= 2.1.234 (Remote Control on Windows), and a
#    CLI login exists (file existence only - never read).
# 2. Registers PreissRelay: at every logon, scripts\relay-session.ps1 keeps a
#    `claude --remote-control main-pc` session alive, and starts it now. From
#    then on the laptop reaches this PC by SendMessage and the phone through
#    claude.ai/code. It replaces the laptop's dead "Claude Relay" task.
#    The relay window is brought to the front at the end, because a first
#    run can wait on a login or folder-trust question in a minimized window.
# 3. Employee prerequisites (docs/employee-setup-main-pc.md steps 1 and 3):
#    Bun and the Telegram channel plugin, installed if missing - and the
#    plugin kept disabled user-wide, so only the employee session polls.
# 4. Reports whether this PC sleeps. An asleep host is an offline relay.
# 5. Asks for the Telegram bot token if there is none (hidden prompt; Enter
#    skips), then registers PreissEmployee and starts the employee.
# Both sessions run in permission mode auto (Tenis 2026-09-18). Everything
# after this run is driven from the laptop through the relay.
# Idempotent - safe to re-run. Written 2026-09-17, extended 2026-09-18.

param(
    [string]$RelayName,
    [switch]$NoInstalls
)

$ErrorActionPreference = 'Continue'
. (Join-Path $PSScriptRoot 'resolve-claude.ps1')
. (Join-Path $PSScriptRoot 'machine-role.ps1')

# Refuses on the shop PC (2026-09-18: it was run there, and registered the
# CNC appliance as "main-pc"). The relay name follows the machine, so a run
# on the wrong PC can never impersonate main-pc again.
Assert-AgentHost 'The always-on host'
if (-not $RelayName) { $RelayName = Get-MachineRole }
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

function Get-RelayProcess {
    Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like '*relay-session.ps1*' } | Select-Object -First 1
}
$relay = Get-RelayProcess
if ($relay) {
    Say 'OK' 'relay session' "already running (pid $($relay.ProcessId))"
} else {
    Start-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 4
    $relay = Get-RelayProcess
    if ($relay) { Say 'DONE' 'relay session' "started (pid $($relay.ProcessId))" }
    else { Say 'FAIL' 'relay session' 'the task did not start a process - Get-ScheduledTaskInfo PreissRelay'; $todo += 'the relay did not start' }
}

# What the relay has been doing, without opening its window.
$relayLog = Join-Path $env:USERPROFILE ".claude\relay-$RelayName.log"
if (Test-Path $relayLog) {
    Write-Host "  ...   relay log (last lines):"
    Get-Content $relayLog -Tail 4 | ForEach-Object { Write-Host "        $_" -ForegroundColor DarkGray }
}

# Bring the relay window to the front. It starts minimized, and on a first
# run it can sit on a login or folder-trust question nobody sees - which is
# an offline relay with no error anywhere. Whatever it asks, answer it once.
if ($relay) {
    try {
        if (-not ('PreissRelay.Win' -as [type])) {
            Add-Type -Namespace PreissRelay -Name Win -MemberDefinition @'
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
'@
        }
        $hwnd = [IntPtr]::Zero
        foreach ($i in 1..10) {
            $hwnd = (Get-Process -Id $relay.ProcessId -ErrorAction Stop).MainWindowHandle
            if ($hwnd -ne [IntPtr]::Zero) { break }
            Start-Sleep -Milliseconds 500
        }
        if ($hwnd -ne [IntPtr]::Zero) {
            [void][PreissRelay.Win]::ShowWindow($hwnd, 9)   # SW_RESTORE
            [void][PreissRelay.Win]::SetForegroundWindow($hwnd)
            Say 'DONE' 'relay window' 'brought to the front - if it asks for a login or folder trust, answer it, then minimize it'
        } else {
            Say 'CHECK' 'relay window' "no window yet - look for 'Claude relay ($RelayName)' in the taskbar"
        }
    } catch {
        Say 'CHECK' 'relay window' "could not raise it ($($_.Exception.Message)) - open 'Claude relay ($RelayName)' from the taskbar"
    }
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

    # Installed, but NOT enabled for every session: with a token, each session
    # that loads it polls the bot - relay and desktop sessions too - and
    # Telegram allows one poller per bot (409 Conflict, lost messages).
    # employee-session.ps1 enables it for the employee alone via --settings.
    $userSettings = Join-Path $env:USERPROFILE '.claude\settings.json'
    $enabled = $false
    try { $enabled = ((Get-Content $userSettings -Raw | ConvertFrom-Json).enabledPlugins.$plugin -eq $true) } catch { }
    if ($enabled) {
        & $claude plugin disable $plugin --scope user | Out-Null
        Say 'DONE' 'Telegram plugin' 'disabled user-wide - only the employee session loads it'
    } else {
        Say 'OK' 'Telegram plugin' 'not enabled user-wide - only the employee session loads it'
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

# --- 5. The employee: token, autostart, start ---------------------------------
$tokenFile = Join-Path $env:USERPROFILE '.claude\channels\telegram\.env'
if (-not (Test-Path $tokenFile)) {
    Write-Host ""
    Write-Host "  Telegram bot token: @BotFather -> /newbot gives it. A small window opens - paste it there (Ctrl+V works)." -ForegroundColor Cyan
    Write-Host "  Skip leaves the employee waiting until a token exists." -ForegroundColor Cyan
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'employee-set-token.ps1')
}
if (Test-Path $tokenFile) {
    Say 'OK' 'bot token' 'present'
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'install-employee-autostart.ps1') | Out-Null
    if (Get-ScheduledTask -TaskName 'PreissEmployee' -ErrorAction SilentlyContinue) {
        Say 'DONE' 'PreissEmployee' 'registered: at logon -> employee-session.ps1'
        $employee = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
            Where-Object { $_.CommandLine -like '*employee-session.ps1*' } | Select-Object -First 1
        if ($employee) { Say 'OK' 'employee' "already running (pid $($employee.ProcessId))" }
        else { Start-ScheduledTask -TaskName 'PreissEmployee'; Say 'DONE' 'employee' "started - window in the taskbar, Remote Control name 'employee'" }
    } else {
        Say 'FAIL' 'PreissEmployee' 'not registered - see the output above'
        $todo += 'PreissEmployee autostart failed to register'
    }
} else {
    Say 'SKIP' 'employee' 'no bot token yet - re-run this script once you have one'
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
Write-Host "Last step is yours alone: message your bot from the phone and send Claude the 6-letter code it replies with."
Write-Host ""
