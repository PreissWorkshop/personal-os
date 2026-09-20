# money-setup.ps1 - set up the money skill on a development machine.
# Run once on the laptop and once on main-pc, from the personal-os root, on
# the branch that carries .claude\skills\money:
#     powershell -ExecutionPolicy Bypass -File scripts\money-setup.ps1 -Verify
# What it does (idempotent; never overwrites a file you have filled in):
#   1. junction  ~\.claude\skills\money -> <repo>\.claude\skills\money
#      so the skill loads from every project root on this machine
#   2. private folder ~\.preiss\finance with finance-snapshot.json and
#      decisions.md copied from the templates - only if missing. Real
#      numbers go there and nowhere else; personal-os is public on GitHub.
#   3. the one-line rule in ~\.claude\CLAUDE.md and the prompt hook in
#      ~\.claude\settings.json (merged into what is there; a .bak-money
#      copy is kept) - the two backstops for the skill under-triggering
#   4. python scripts\money_model.py selftest
#   5. with -Verify: python scripts\verify_claims.py, the upgrade pass that
#      fetches every load-bearing claim's page; report goes to
#      ~\.preiss\finance\verify-<date>.md (private folder, never the repo)
# Refuses to run on the shop PC (machine roles are law). Reads no secrets.
# Written 2026-09-20 from a Linux sandbox: UNTESTED on Windows - read the
# output line by line the first time and report what differs.
param([switch]$Verify, [switch]$NoHook)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'machine-role.ps1')
Assert-AgentHost 'The money skill'

$repo  = Split-Path -Parent $PSScriptRoot
$skill = Join-Path $repo '.claude\skills\money'
if (-not (Test-Path (Join-Path $skill 'SKILL.md'))) {
    Write-Host "  STOP  $skill has no SKILL.md - run this from the personal-os root on the branch that carries the money skill (git fetch; git checkout claude/profitable-business-debt-situation-6d7hq3, or main once merged). Nothing changed." -ForegroundColor Red
    exit 2
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "  STOP  python is not on PATH (Python 3.11 per the bootstrap doc). Nothing changed." -ForegroundColor Red
    exit 2
}
Write-Host "money-setup on $(Get-MachineRole) ($env:COMPUTERNAME), repo $repo"

# 1. junction -------------------------------------------------------------
$skillsDir = Join-Path $HOME '.claude\skills'
New-Item -ItemType Directory -Force $skillsDir | Out-Null
$link = Join-Path $skillsDir 'money'
if (Test-Path $link) {
    $item   = Get-Item $link -Force
    $target = [string](@($item.Target)[0])
    if ($item.LinkType -ne 'Junction') {
        Write-Host "  STOP  $link is a real folder, not a junction - move it away and re-run"
        exit 1
    } elseif ($target.TrimEnd('\') -ieq $skill.TrimEnd('\')) {
        Write-Host "  ok    junction $link -> $skill"
    } else {
        # The repo moved (first run from a worktree, clone relocated): re-point.
        # rmdir on a junction removes the link only, never the target's files.
        cmd /c rmdir "$link"
        New-Item -ItemType Junction -Path $link -Target $skill | Out-Null
        Write-Host "  done  junction re-pointed $link -> $skill (was $target)"
    }
} else {
    New-Item -ItemType Junction -Path $link -Target $skill | Out-Null
    Write-Host "  done  junction $link -> $skill"
}

# 2. private folder ---------------------------------------------------------
$fin = Join-Path $HOME '.preiss\finance'
New-Item -ItemType Directory -Force $fin | Out-Null
$snap = Join-Path $fin 'finance-snapshot.json'
if (Test-Path $snap) {
    Write-Host "  ok    $snap exists (not touched)"
} else {
    Copy-Item (Join-Path $skill 'assets\finance-snapshot.template.json') $snap
    Write-Host "  done  $snap created from the template - fill in the real numbers there, nowhere else"
}
$log = Join-Path $fin 'decisions.md'
if (Test-Path $log) {
    Write-Host "  ok    $log exists (not touched)"
} else {
    Copy-Item (Join-Path $skill 'assets\decisions-template.md') $log
    Write-Host "  done  $log created (the private decision log)"
}

# 3. global CLAUDE.md rule + prompt hook --------------------------------------
$claudeDir = Join-Path $HOME '.claude'
New-Item -ItemType Directory -Force $claudeDir | Out-Null
$md = Join-Path $claudeDir 'CLAUDE.md'
$marker = 'load the `money` skill first'
if ((Test-Path $md) -and (Select-String -Path $md -SimpleMatch $marker -Quiet)) {
    Write-Host "  ok    $md already carries the money rule"
} else {
    $rule = "`n## Money`n`n- Any question about money, debt, rates, pricing as a business decision, a new income idea, remote work, relocation or financial independence: load the ``money`` skill first. Real figures live only in ~\.preiss\finance, never in a repo.`n"
    Add-Content -Path $md -Value $rule -Encoding UTF8
    Write-Host "  done  money rule appended to $md"
}

if ($NoHook) {
    Write-Host "  skip  prompt hook (-NoHook)"
} else {
    $settingsPath = Join-Path $claudeDir 'settings.json'
    $hookFile = (Join-Path $repo '.claude\hooks\money_trigger.py') -replace '\\', '/'
    $json = if (Test-Path $settingsPath) { Get-Content $settingsPath -Raw -Encoding UTF8 } else { '{}' }
    if ($json -match [regex]::Escape($hookFile)) {
        Write-Host "  ok    $settingsPath already runs $hookFile"
    } elseif ($json -match 'money_trigger\.py') {
        # The repo moved: swap the quoted path, leave the rest of the file untouched.
        $new = [regex]::Replace($json, '(?<=\\")[^"]*money_trigger\.py(?=\\")', $hookFile.Replace('$', '$$'))
        if ($new -match [regex]::Escape($hookFile)) {
            Copy-Item $settingsPath "$settingsPath.bak-money" -Force
            [System.IO.File]::WriteAllText($settingsPath, $new, (New-Object System.Text.UTF8Encoding($false)))
            Write-Host "  done  prompt hook re-pointed to $hookFile (previous copy: $settingsPath.bak-money)"
        } else {
            Write-Host "  WARN  $settingsPath runs money_trigger.py by a path this script cannot rewrite - set the hook command by hand to: python `"$hookFile`""
        }
    } else {
        $settings = $json | ConvertFrom-Json
        if (-not $settings.PSObject.Properties['hooks']) {
            $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([pscustomobject]@{})
        }
        $entry = [pscustomobject]@{
            hooks = @([pscustomobject]@{
                type = 'command'; command = "python `"$hookFile`""; timeout = 10
                statusMessage = 'money-skill trigger check'
            })
        }
        if ($settings.hooks.PSObject.Properties['UserPromptSubmit']) {
            $settings.hooks.UserPromptSubmit = @($settings.hooks.UserPromptSubmit) + @($entry)
        } else {
            $settings.hooks | Add-Member -NotePropertyName UserPromptSubmit -NotePropertyValue @($entry)
        }
        if (Test-Path $settingsPath) { Copy-Item $settingsPath "$settingsPath.bak-money" -Force }
        # WriteAllText with UTF8Encoding($false): no byte-order mark, which a JSON parser may reject.
        [System.IO.File]::WriteAllText($settingsPath, (ConvertTo-Json -InputObject $settings -Depth 16), (New-Object System.Text.UTF8Encoding($false)))
        Write-Host "  done  prompt hook added to $settingsPath (previous copy: $settingsPath.bak-money)"
        Write-Host "        check with /hooks in a Claude Code session; a prompt such as 'which loan first, the overdraft or the card?' should show the money-skill note"
    }
}

# 4. selftest -----------------------------------------------------------------
& python (Join-Path $skill 'scripts\money_model.py') selftest | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Write-Host "  FAIL  selftest did not pass - report it, do not use the numbers" -ForegroundColor Red; exit 1 }

# 5. verification pass ----------------------------------------------------------
if ($Verify) {
    $report = Join-Path $fin ("verify-" + (Get-Date -Format 'yyyy-MM-dd') + ".md")
    Write-Host "  run   verify_claims.py (fetches ~44 pages; a few minutes)"
    & python (Join-Path $skill 'scripts\verify_claims.py') --report $report
    Write-Host "  report $report - VERIFIED rows can be upgraded to [V] in the references with today's date; NOT FOUND rows mean open the page and correct the reference; BLOCKED rows try from the other machine"
} else {
    Write-Host "  skip  verification pass (add -Verify to run it; needs open internet)"
}

Write-Host ""
Write-Host "Next: open Claude Code at $repo and ask a money question; then fill $snap and run"
Write-Host "      python .claude\skills\money\scripts\money_model.py plan --snapshot $snap"
Write-Host "      Carry ~\.preiss\finance to the other machine by USB or cloud, never through git."
