# employee-set-token.ps1 - store the Telegram bot token for the employee.
# Opens a small dialog with a masked box: Ctrl+V pastes there, or use the
# "Paste from clipboard" button. The token goes straight to
# ~\.claude\channels\telegram\.env and through no agent or transcript.
#   powershell -ExecutionPolicy Bypass -File scripts\employee-set-token.ps1
# Why a dialog: in the black console window Ctrl+V does not paste - it types
# one invisible control character (0x16), shown as a single "*", which is
# exactly what happened on main-pc 2026-09-18. The console prompt remains as
# the fallback when no desktop is available; there, paste by right-click.
# Written without a trailing newline on purpose: the plugin splits the file on
# "\n" only, so a Windows CRLF would leave "\r" glued to the token and every
# Telegram call would fail. Written 2026-09-18.

$ErrorActionPreference = 'Stop'

$dir = if ($env:TELEGRAM_STATE_DIR) { $env:TELEGRAM_STATE_DIR } else { Join-Path $env:USERPROFILE '.claude\channels\telegram' }
$envFile = Join-Path $dir '.env'

function Read-TokenDialog {
    # Returns the entered text, '' when skipped, $null when no dialog can be shown.
    if (-not [Environment]::UserInteractive) { return $null }
    try {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
    } catch { return $null }

    $form = New-Object System.Windows.Forms.Form
    $form.Text = 'Employee - Telegram bot token'
    $form.ClientSize = New-Object System.Drawing.Size(520, 140)
    $form.StartPosition = 'CenterScreen'
    $form.FormBorderStyle = 'FixedDialog'
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false
    $form.TopMost = $true

    $label = New-Object System.Windows.Forms.Label
    $label.Text = 'Paste the token from @BotFather (Ctrl+V works here). It is stored only on this PC.'
    $label.SetBounds(12, 12, 496, 36)

    $box = New-Object System.Windows.Forms.TextBox
    $box.UseSystemPasswordChar = $true
    $box.SetBounds(12, 52, 496, 24)

    $paste = New-Object System.Windows.Forms.Button
    $paste.Text = 'Paste from clipboard'
    $paste.SetBounds(12, 96, 160, 30)
    $paste.Add_Click({
        try { $box.Text = [System.Windows.Forms.Clipboard]::GetText().Trim() } catch { }
    }.GetNewClosure())

    $save = New-Object System.Windows.Forms.Button
    $save.Text = 'Save'
    $save.SetBounds(328, 96, 85, 30)
    $save.DialogResult = [System.Windows.Forms.DialogResult]::OK

    $skip = New-Object System.Windows.Forms.Button
    $skip.Text = 'Skip'
    $skip.SetBounds(423, 96, 85, 30)
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

$token = Read-TokenDialog
if ($null -eq $token) {
    Write-Host 'No desktop for a dialog - console prompt instead. Paste with a RIGHT-CLICK; Ctrl+V does not paste here.'
    $secure = Read-Host 'Bot token from BotFather (input hidden)' -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr).Trim() }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
}

if (-not $token) { Write-Host 'Skipped - no token written.'; exit 0 }

if ($token -match '[\x00-\x1F]') {
    Write-Error 'That was a control character, not the token (Ctrl+V in the console types one). Paste with a right-click, or use the dialog. Nothing written.'
}

# BotFather tokens look like 123456789:AAH... - digits, colon, 30+ url-safe chars.
if ($token -notmatch '^\d+:[A-Za-z0-9_-]{30,}$') {
    Write-Error 'That does not look like a BotFather token (digits, a colon, then a long code). Nothing written.'
}

New-Item -ItemType Directory -Force $dir | Out-Null
[IO.File]::WriteAllText($envFile, "TELEGRAM_BOT_TOKEN=$token", (New-Object System.Text.UTF8Encoding $false))
$token = $null

Write-Host "Saved to $envFile (the bot id before the colon is $((Get-Content $envFile -Raw) -replace '^TELEGRAM_BOT_TOKEN=(\d+):.*$', '$1'))." -ForegroundColor Green
