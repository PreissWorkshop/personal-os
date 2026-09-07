# employee-preflight.ps1 - check main-pc can host the employee session.
# Read-only. Prints what is missing and stops at nothing.
# Written 2026-09-07. See docs/employee-setup-main-pc.md.

$ErrorActionPreference = 'Continue'
$missing = @()

function Test-Item($label, $ok, $detail, $fix) {
    if ($ok) { Write-Host ("  OK    {0}  {1}" -f $label, $detail) }
    else {
        Write-Host ("  MISS  {0}  {1}" -f $label, $detail) -ForegroundColor Yellow
        if ($fix) { $script:missing += "$label : $fix" }
    }
}

Write-Host ""
Write-Host "Employee preflight - $(Get-Date -Format 'yyyy-MM-dd HH:mm') on $env:COMPUTERNAME"
Write-Host ""

# --- Claude Code ---
$claudePath = (Get-Command claude -ErrorAction SilentlyContinue).Source
$onPath = $null -ne $claudePath
if (-not $claudePath) {
    $candidate = Join-Path $env:USERPROFILE '.local\bin\claude.exe'
    if (Test-Path $candidate) { $claudePath = $candidate }
}
Test-Item 'Claude Code' ($null -ne $claudePath) $(if ($claudePath) { $claudePath } else { 'not found' }) `
    'install Claude Code, or add its folder to PATH so a scheduled task can launch it'
if ($claudePath -and -not $onPath) {
    Write-Host "  WARN  claude.exe is not on PATH - employee-session.ps1 resolves it, but add it to PATH anyway." -ForegroundColor Yellow
}

# --- Bun (required by the channel plugins) ---
$bun = Get-Command bun -ErrorAction SilentlyContinue
if (-not $bun) {
    $candidate = Join-Path $env:USERPROFILE '.bun\bin\bun.exe'
    if (Test-Path $candidate) { $bun = Get-Item $candidate }
}
Test-Item 'Bun' ($null -ne $bun) $(if ($bun) { $bun.Source } else { 'not found' }) `
    'run:  irm bun.sh/install.ps1 | iex'

# --- git ---
$git = Get-Command git -ErrorAction SilentlyContinue
Test-Item 'git' ($null -ne $git) $(if ($git) { $git.Source } else { 'not found' }) 'install Git for Windows'

# --- repo clones, from the registry's main-pc roots ---
Write-Host ""
Write-Host "Project roots (registry/projects.yaml, main-pc):"
$roots = [ordered]@{
    'personal-os'   = 'C:\Projects\_system\personal-os'
    'scanpen'       = 'C:\Projects\ScanPen\repo'
    'helmcnc-app'   = 'C:\Projects\HelmCNC\app'
    'website'       = 'C:\PREISS_WEBSITE\website'
    'claude-system' = 'C:\PREISS_WORKSHOP_CLAUDE_SYSTEM\PREISS_WORKSHOP_CLAUDE_SYSTEM'
}
foreach ($name in $roots.Keys) {
    $p = $roots[$name]
    $ok = Test-Path (Join-Path $p '.git')
    Test-Item $name $ok $p "clone it - see docs/bootstrap-new-machine.md"
}

# --- telegram channel config (machine-local, never committed) ---
Write-Host ""
$envFile = Join-Path $env:USERPROFILE '.claude\channels\telegram\.env'
Test-Item 'telegram token' (Test-Path $envFile) $envFile `
    'step 2-3 of docs/employee-setup-main-pc.md (BotFather, then /telegram:configure <token>)'

# --- claude.ai login (routines need it; API keys do not work) ---
if ($env:ANTHROPIC_API_KEY -or $env:ANTHROPIC_AUTH_TOKEN) {
    Write-Host "  WARN  ANTHROPIC_API_KEY/AUTH_TOKEN is set - it overrides the claude.ai login," -ForegroundColor Yellow
    Write-Host "        and routines (/schedule) require the claude.ai login. Unset it for this session." -ForegroundColor Yellow
}

Write-Host ""
if ($missing.Count -eq 0) {
    Write-Host "All clear. Next: step 2 of docs/employee-setup-main-pc.md (create the Telegram bot)." -ForegroundColor Green
} else {
    Write-Host "To fix before starting:" -ForegroundColor Yellow
    $missing | ForEach-Object { Write-Host "  - $_" }
}
Write-Host ""
