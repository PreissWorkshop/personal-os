# relay-session.ps1 - keep one Remote Control session alive on this machine,
# so the laptop (SendMessage) and the phone (claude.ai/code) can reach it.
# Launched at logon by the PreissRelay task - see scripts\main-pc-always-on.ps1.
# If the session exits it comes back; close this window to stop it until the
# next logon, or `Disable-ScheduledTask PreissRelay` to stop it for good.
# Permission mode `auto` (Tenis 2026-09-18: "automate this so you can do
# everything yourself"): dispatched work runs without prompts, the auto-mode
# safety classifier still blocks risky actions. Never bypassPermissions.
# Written 2026-09-17.

param(
    [string]$Name = 'main-pc',
    [switch]$DryRun
)

$ErrorActionPreference = 'Continue'
. (Join-Path $PSScriptRoot 'resolve-claude.ps1')

# Remote Control rides the claude.ai login; an API key env var silently outranks it.
if ($env:ANTHROPIC_API_KEY)    { Remove-Item Env:\ANTHROPIC_API_KEY }
if ($env:ANTHROPIC_AUTH_TOKEN) { Remove-Item Env:\ANTHROPIC_AUTH_TOKEN }

# Neutral root, like the shop PC's relay: dispatched work names its own project root.
Set-Location $env:USERPROFILE
try { $host.UI.RawUI.WindowTitle = "Claude relay ($Name)" } catch { }

while ($true) {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $claude = Resolve-Claude
    if (-not $claude) {
        Write-Warning "$stamp  claude.exe not found (PATH, ~\.local\bin, Claude app). Retrying in 5 minutes."
        if ($DryRun) { break }
        Start-Sleep -Seconds 300
        continue
    }
    Write-Host "$stamp  starting: $claude --remote-control $Name --permission-mode auto"
    if ($DryRun) { break }

    $started = Get-Date
    & $claude --remote-control $Name --permission-mode auto
    $code = $LASTEXITCODE
    $ran = ((Get-Date) - $started).TotalSeconds

    # A session that dies at once (logged out, broken install) must not spin.
    $wait = if ($ran -lt 60) { 300 } else { 30 }
    Write-Host ("{0}  session ended after {1:N0} s (exit {2}); restarting in {3} s. Close this window to stop." -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $ran, $code, $wait)
    Start-Sleep -Seconds $wait
}
