# employee-set-token.ps1 - store the Telegram bot token for the employee.
# You type the token at a hidden prompt; it goes straight to
# ~\.claude\channels\telegram\.env and through no agent or transcript.
#   powershell -ExecutionPolicy Bypass -File scripts\employee-set-token.ps1
# Written without a trailing newline on purpose: the plugin splits the file on
# "\n" only, so a Windows CRLF would leave "\r" glued to the token and every
# Telegram call would fail. Written 2026-09-18.

$ErrorActionPreference = 'Stop'

$dir = if ($env:TELEGRAM_STATE_DIR) { $env:TELEGRAM_STATE_DIR } else { Join-Path $env:USERPROFILE '.claude\channels\telegram' }
$envFile = Join-Path $dir '.env'

$secure = Read-Host 'Paste the bot token from BotFather (input hidden)' -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try { $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr).Trim() }
finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }

# BotFather tokens look like 123456789:AAH... - digits, colon, 30+ url-safe chars.
if ($token -notmatch '^\d+:[A-Za-z0-9_-]{30,}$') {
    Write-Error 'That does not look like a BotFather token (digits, a colon, then a long code). Nothing written.'
}

New-Item -ItemType Directory -Force $dir | Out-Null
[IO.File]::WriteAllText($envFile, "TELEGRAM_BOT_TOKEN=$token", (New-Object System.Text.UTF8Encoding $false))
$token = $null

Write-Host "Saved to $envFile (the bot id before the colon is $((Get-Content $envFile -Raw) -replace '^TELEGRAM_BOT_TOKEN=(\d+):.*$', '$1'))." -ForegroundColor Green
Write-Host "Next: powershell -ExecutionPolicy Bypass -File scripts\employee-session.ps1"
