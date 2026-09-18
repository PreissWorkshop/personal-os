# frontdesk-set-key.ps1 - store the front desk's secrets on this machine.
#   powershell -ExecutionPolicy Bypass -File scripts\frontdesk-set-key.ps1
#
# Two secrets, one optional:
#   ANTHROPIC_API_KEY          console.anthropic.com - the fast model is called
#                              directly, so this is NOT the claude.ai login
#   TELEGRAM_BOT_TOKEN         reused from the Telegram plugin's own .env if it
#                              is already there, so you never enter it twice
#   FRONTDESK_WEBHOOK_TOKEN    optional; only needed to let the NVR, CI or a
#                              script push an alert to the phone. Generated here.
#
# Written to ~\.claude\frontdesk\.env - machine-local, never committed, never
# through an agent or a transcript (docs/security.md). Same masked-dialog
# pattern as employee-set-token.ps1: in the black console window Ctrl+V does
# not paste, it types one invisible control character. Written 2026-09-18.

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'machine-role.ps1')
Assert-AgentHost 'The front desk'

$dir     = Join-Path $env:USERPROFILE '.claude\frontdesk'
$envFile = Join-Path $dir '.env'
$pluginEnv = Join-Path $env:USERPROFILE '.claude\channels\telegram\.env'

function Read-SecretDialog {
    param([string]$Title, [string]$Blurb)
    # Returns the entered text, '' when skipped, $null when no dialog is possible.
    if (-not [Environment]::UserInteractive) { return $null }
    try {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
    } catch { return $null }

    $form = New-Object System.Windows.Forms.Form
    $form.Text = $Title
    $form.ClientSize = New-Object System.Drawing.Size(560, 150)
    $form.StartPosition = 'CenterScreen'
    $form.FormBorderStyle = 'FixedDialog'
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false
    $form.TopMost = $true

    $label = New-Object System.Windows.Forms.Label
    $label.Text = $Blurb
    $label.SetBounds(12, 12, 536, 44)

    $box = New-Object System.Windows.Forms.TextBox
    $box.UseSystemPasswordChar = $true
    $box.SetBounds(12, 60, 536, 24)

    $paste = New-Object System.Windows.Forms.Button
    $paste.Text = 'Paste from clipboard'
    $paste.SetBounds(12, 104, 160, 30)
    $paste.Add_Click({
        try { $box.Text = [System.Windows.Forms.Clipboard]::GetText().Trim() } catch { }
    }.GetNewClosure())

    $save = New-Object System.Windows.Forms.Button
    $save.Text = 'Save'
    $save.SetBounds(368, 104, 85, 30)
    $save.DialogResult = [System.Windows.Forms.DialogResult]::OK

    $skip = New-Object System.Windows.Forms.Button
    $skip.Text = 'Skip'
    $skip.SetBounds(463, 104, 85, 30)
    $skip.DialogResult = [System.Windows.Forms.DialogResult]::Cancel

    $form.Controls.AddRange(@($label, $box, $paste, $save, $skip))
    $form.AcceptButton = $save
    $form.CancelButton = $skip
    $form.Add_Shown({ $form.Activate(); $box.Focus() }.GetNewClosure())

    $result = $form.ShowDialog()
    $text = $box.Text
    $form.Dispose()
    if ($result -ne [System.Windows.Forms.DialogResult]::OK) { return '' }
    return $text.Trim()
}

function Read-Secret {
    param([string]$Title, [string]$Blurb, [string]$ConsolePrompt)
    $value = Read-SecretDialog -Title $Title -Blurb $Blurb
    if ($null -eq $value) {
        Write-Host 'No desktop for a dialog - console prompt instead. Paste with a RIGHT-CLICK; Ctrl+V does not paste here.'
        $secure = Read-Host $ConsolePrompt -AsSecureString
        $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
        try { $value = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr).Trim() }
        finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
    }
    return $value
}

# --- read whatever is already stored, so a re-run only changes what you enter
$existing = @{}
if (Test-Path $envFile) {
    foreach ($line in (Get-Content $envFile)) {
        if ($line -match '^\s*([A-Z_]+)\s*=\s*(.*)$') { $existing[$Matches[1]] = $Matches[2].Trim() }
    }
}

# --- the bot token: reuse the plugin's, or ask -----------------------------
$token = $existing['TELEGRAM_BOT_TOKEN']
if (-not $token -and (Test-Path $pluginEnv)) {
    $found = [regex]::Match((Get-Content $pluginEnv -Raw), '\b(\d{6,}:[A-Za-z0-9_-]{30,})\b')
    if ($found.Success) {
        $token = $found.Groups[1].Value
        Write-Host "Reusing the bot token already stored for the Telegram plugin." -ForegroundColor Green
    }
}
if (-not $token) {
    $token = Read-Secret -Title 'Front desk - Telegram bot token' `
        -Blurb 'Paste the token from @BotFather (Ctrl+V works here). Stored only on this PC.' `
        -ConsolePrompt 'Telegram bot token (input hidden)'
}
if ($token -and $token -notmatch '^\d+:[A-Za-z0-9_-]{30,}$') {
    Write-Error 'That does not look like a BotFather token (digits, a colon, then a long code). Nothing written.'
}

# --- the API key -----------------------------------------------------------
$key = Read-Secret -Title 'Front desk - Anthropic API key' `
    -Blurb ('Paste an API key from console.anthropic.com. This is NOT the claude.ai ' +
            'login: the front desk calls the fast model directly, which is what makes ' +
            'it answer in about a second. Skip to keep the stored one.') `
    -ConsolePrompt 'Anthropic API key (input hidden)'
if (-not $key) { $key = $existing['ANTHROPIC_API_KEY'] }
if ($key -and $key -match '[\x00-\x1F]') {
    Write-Error 'That was a control character, not the key (Ctrl+V in the console types one). Nothing written.'
}
if ($key -and $key -notmatch '^sk-ant-') {
    Write-Warning 'That does not start with sk-ant-. Storing it anyway, but check it if the front desk reports 401.'
}

# --- the webhook token: generated, not typed -------------------------------
$hook = $existing['FRONTDESK_WEBHOOK_TOKEN']
if (-not $hook) {
    $bytes = New-Object byte[] 16
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    # Hex, not base64: base64 needs its non-alphanumerics stripped and the
    # result is then not a guaranteed length, so Substring could throw.
    $hook = [System.BitConverter]::ToString($bytes).Replace('-', '').ToLower()
    Write-Host 'Generated a webhook token so the NVR and CI can push alerts to the phone.'
}

if (-not $token) { Write-Error "No bot token. Run scripts\employee-set-token.ps1 first, or enter it here. Nothing written." }
if (-not $key)   { Write-Error "No API key, and none stored. Nothing written." }

New-Item -ItemType Directory -Force $dir | Out-Null
$body = @(
    "# Front desk secrets - machine-local. Never commit, never paste into a chat.",
    "TELEGRAM_BOT_TOKEN=$token",
    "ANTHROPIC_API_KEY=$key",
    "FRONTDESK_WEBHOOK_TOKEN=$hook"
) -join "`n"
[IO.File]::WriteAllText($envFile, $body, (New-Object System.Text.UTF8Encoding $false))

# Owner-only ACL: the default inherits Users, and this file holds two live keys.
try {
    $acl = Get-Acl $envFile
    $acl.SetAccessRuleProtection($true, $false)
    @($acl.Access) | ForEach-Object { $acl.RemoveAccessRule($_) | Out-Null }
    $acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
        "$env:USERDOMAIN\$env:USERNAME", 'FullControl', 'Allow')))
    Set-Acl $envFile $acl
    Write-Host 'Locked the file to this user only.' -ForegroundColor Green
} catch {
    Write-Warning "Could not tighten the file permissions: $($_.Exception.Message)"
}

$botId = ($token -split ':')[0]
$token = $null; $key = $null

Write-Host ""
Write-Host "Saved to $envFile" -ForegroundColor Green
Write-Host "  bot id                  $botId"
Write-Host "  API key                 stored (not shown)"
Write-Host "  webhook token           stored (not shown)"
Write-Host ""
Write-Host "To let the NVR alert your phone, read the token out of that file yourself"
Write-Host "and set it as the webhook URL in the Surveillance settings:"
Write-Host "  http://main-pc:8787/event?token=<the FRONTDESK_WEBHOOK_TOKEN line>"
Write-Host ""
Write-Host "Next: scripts\frontdesk-session.ps1"
