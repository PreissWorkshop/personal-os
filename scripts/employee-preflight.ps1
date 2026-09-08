# employee-preflight.ps1 - check this machine can host the employee session.
# Read-only. Prints what is missing and stops at nothing.
# Works on main-pc and on the laptop: project roots are per-machine, so each
# project is checked against every registered root (registry/projects.yaml).
# Written 2026-09-07, made machine-aware 2026-09-08.
# See docs/employee-setup-main-pc.md.

$ErrorActionPreference = 'Continue'
$missing = @()

function Test-Item($label, $ok, $detail, $fix) {
    if ($ok) { Write-Host ("  OK    {0,-16} {1}" -f $label, $detail) }
    else {
        Write-Host ("  MISS  {0,-16} {1}" -f $label, $detail) -ForegroundColor Yellow
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

# --- Bun (the channel plugins are Bun scripts) ---
$bunPath = (Get-Command bun -ErrorAction SilentlyContinue).Source
if (-not $bunPath) {
    $candidate = Join-Path $env:USERPROFILE '.bun\bin\bun.exe'
    if (Test-Path $candidate) { $bunPath = $candidate }
}
Test-Item 'Bun' ($null -ne $bunPath) $(if ($bunPath) { $bunPath } else { 'not found' }) `
    'run:  irm bun.sh/install.ps1 | iex'

# --- git ---
$git = (Get-Command git -ErrorAction SilentlyContinue).Source
Test-Item 'git' ($null -ne $git) $(if ($git) { $git } else { 'not found' }) 'install Git for Windows'

# --- telegram channel plugin ---
$pluginRoot = Join-Path $env:USERPROFILE '.claude\plugins\marketplaces\claude-plugins-official\external_plugins\telegram'
Test-Item 'telegram plugin' (Test-Path $pluginRoot) $(if (Test-Path $pluginRoot) { 'installed' } else { 'not installed' }) `
    'claude plugin install telegram@claude-plugins-official --scope user --yes'

# --- the bot token: machine-local, never committed ---
$envFile = Join-Path $env:USERPROFILE '.claude\channels\telegram\.env'
Test-Item 'bot token' (Test-Path $envFile) $envFile `
    'step 2-3 of docs/employee-setup-main-pc.md (BotFather, then /telegram:configure <token>)'

# --- project roots: per-machine, so accept any registered root ---
Write-Host ""
Write-Host "Project roots (any registered root counts - they differ per machine):"
$roots = [ordered]@{
    'personal-os'   = @('C:\Projects\_system\personal-os')
    'scanpen'       = @('C:\Projects\ScanPen\repo', 'C:\ScanPen')
    'helmcnc-app'   = @('C:\Projects\HelmCNC\app', 'C:\HelmCNC.bak')
    'website'       = @('C:\Projects\PreissWebsite\website', 'C:\PREISS_WEBSITE\website')
    'claude-system' = @('C:\Projects\PreissClaudeSystem\repo', 'C:\PREISS_WORKSHOP_CLAUDE_SYSTEM\PREISS_WORKSHOP_CLAUDE_SYSTEM')
}
foreach ($name in $roots.Keys) {
    $found = $roots[$name] | Where-Object { Test-Path (Join-Path $_ '.git') } | Select-Object -First 1
    Test-Item $name ($null -ne $found) $(if ($found) { $found } else { "none of: $($roots[$name] -join ' | ')" }) `
        'clone it - see docs/bootstrap-new-machine.md (optional: the employee runs without it)'
}

# --- claude.ai login (routines need it; API keys silently outrank it) ---
Write-Host ""
if ($env:ANTHROPIC_API_KEY -or $env:ANTHROPIC_AUTH_TOKEN) {
    Write-Host "  WARN  ANTHROPIC_API_KEY/AUTH_TOKEN is set - it overrides the claude.ai login," -ForegroundColor Yellow
    Write-Host "        and routines (/schedule) require that login. employee-session.ps1 clears" -ForegroundColor Yellow
    Write-Host "        it for its own process, but clear it in your shell too." -ForegroundColor Yellow
} else {
    Write-Host "  OK    no API-key env var shadowing the claude.ai login"
}

Write-Host ""
if ($missing.Count -eq 0) {
    Write-Host "All clear. Start it with scripts\employee-session.ps1" -ForegroundColor Green
} else {
    Write-Host "To fix before starting:" -ForegroundColor Yellow
    $missing | ForEach-Object { Write-Host "  - $_" }
}
Write-Host ""
