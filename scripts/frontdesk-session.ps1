# frontdesk-session.ps1 - run the front desk on main-pc.
#   powershell -ExecutionPolicy Bypass -File scripts\frontdesk-session.ps1
#
# The front desk is the fast agent that owns the Telegram bot: it answers in
# about a second and hands real work to a Claude Code session. See
# docs/frontdesk.md. Restart loop and logging follow the same pattern as
# relay-session.ps1 and employee-session.ps1.
#
# IMPORTANT: Telegram allows one poller per bot token. Once this is running,
# the employee session must NOT also load the Telegram plugin, or the two
# fight for updates (409 Conflict) and messages are lost to whichever won.
# employee-session.ps1 checks for this and drops its channel automatically.
# Written 2026-09-18.

param(
    [switch]$Once,        # run in the foreground without the restart loop
    [switch]$SelfTest     # run the offline checks and exit
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'machine-role.ps1')
Assert-AgentHost 'The front desk'

$repo = 'C:\Projects\_system\personal-os'
if (-not (Test-Path (Join-Path $repo '.git'))) {
    Write-Error "personal-os not found at $repo - clone it first (docs/bootstrap-new-machine.md)."
}
Set-Location $repo

# --- the front desk's own venv --------------------------------------------
# Separate from the voice venv: that one carries torch-sized wheels and is
# shared with scripts\stt.py. This one needs two packages.
$venv = Join-Path $env:USERPROFILE '.venvs\frontdesk'
$py   = Join-Path $venv 'Scripts\python.exe'

if (-not (Test-Path $py)) {
    Write-Host "Creating the front desk environment (once, about a minute)..."
    $python = $null
    foreach ($candidate in @('python', 'python3', 'py')) {
        try {
            if ((& $candidate --version 2>&1) -match 'Python 3\.(\d+)' -and [int]$Matches[1] -ge 9) {
                $python = $candidate; break
            }
        } catch { }
    }
    if (-not $python) {
        Write-Host "Python 3.9+ not found. Install it from python.org, TICK" -ForegroundColor Red
        Write-Host "'Add python.exe to PATH', then run this again."
        exit 1
    }
    & $python -m venv $venv
    & $py -m pip install --upgrade pip --quiet
    & $py -m pip install -r (Join-Path $repo 'frontdesk\requirements.txt')
}

if ($SelfTest) {
    & $py -m frontdesk.selftest
    exit $LASTEXITCODE
}

$envFile = Join-Path $env:USERPROFILE '.claude\frontdesk\.env'
if (-not (Test-Path $envFile)) {
    Write-Error "No secrets at $envFile. Run scripts\frontdesk-set-key.ps1 first."
}

try { $host.UI.RawUI.WindowTitle = 'Front desk (main-pc)' } catch { }

$log = Join-Path $env:USERPROFILE '.claude\frontdesk.log'
function Log($text) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $text"
    Write-Host $line
    try { Add-Content -Path $log -Value $line -Encoding ascii } catch { }
}

if ($Once) {
    & $py -m frontdesk
    exit $LASTEXITCODE
}

$ErrorActionPreference = 'Continue'
while ($true) {
    # Start from current origin, so the digest and the rules are today's.
    git pull --ff-only --quiet
    if ($LASTEXITCODE -ne 0) { Log 'git pull failed; continuing on the local tree.' }

    Log "starting: $py -m frontdesk"
    $started = Get-Date
    & $py -m frontdesk
    $code = $LASTEXITCODE
    $ran = ((Get-Date) - $started).TotalSeconds

    # A process that dies at once (bad key, no token) must not spin. Its own
    # error is already on screen and in this log's neighbour.
    $wait = if ($ran -lt 60) { 300 } else { 15 }
    Log ("front desk ended after {0:N0} s (exit {1}); restarting in {2} s. Close this window to stop." -f $ran, $code, $wait)
    Start-Sleep -Seconds $wait
}
