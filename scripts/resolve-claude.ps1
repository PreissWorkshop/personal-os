# resolve-claude.ps1 - find claude.exe on this machine. Dot-source it:
#   . (Join-Path $PSScriptRoot 'resolve-claude.ps1'); $claude = Resolve-Claude
# Order: PATH, the native installer's ~\.local\bin, then the newest CLI that
# ships inside the Claude desktop app (Store and non-Store installs).
# Resolve at every launch, never at install time: the laptop's first relay
# task baked in a versioned path (claude-code\2.1.237) and failed silently at
# every logon once the app updated past it. Written 2026-09-17.

function Resolve-Claude {
    $cmd = Get-Command claude -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $native = Join-Path $env:USERPROFILE '.local\bin\claude.exe'
    if (Test-Path $native) { return $native }

    $roots = @(Join-Path $env:APPDATA 'Claude\claude-code')
    $packages = Join-Path $env:LOCALAPPDATA 'Packages'
    if (Test-Path $packages) {
        foreach ($pkg in Get-ChildItem $packages -Directory -Filter 'Claude_*' -ErrorAction SilentlyContinue) {
            $roots += Join-Path $pkg.FullName 'LocalCache\Roaming\Claude\claude-code'
        }
    }

    $best = $null
    [version]$bestVersion = '0.0'
    foreach ($root in $roots) {
        if (-not (Test-Path $root)) { continue }
        foreach ($dir in Get-ChildItem $root -Directory -ErrorAction SilentlyContinue) {
            [version]$v = '0.0'
            if (-not [version]::TryParse($dir.Name, [ref]$v)) { continue }
            $exe = Join-Path $dir.FullName 'claude.exe'
            if ((Test-Path $exe) -and $v -gt $bestVersion) { $best = $exe; $bestVersion = $v }
        }
    }
    return $best
}
