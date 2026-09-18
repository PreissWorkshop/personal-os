# machine-role.ps1 - which machine this is, per registry/projects.yaml.
# Dot-source:  . (Join-Path $PSScriptRoot 'machine-role.ps1')
# Names are the tailnet names, and they become the Remote Control names, so a
# script run on the wrong PC can never impersonate another machine.
# Machine roles are law: the shop PC is a HelmCNC appliance - no installs and
# no employee there. A relay may run on it (it is how the laptop reaches the
# CNC PC), under its own name and with permission prompts. On 2026-09-18 the
# always-on bootstrap was run on the shop PC by mistake and its relay
# registered as "main-pc"; this file exists so that cannot happen twice.
# Written 2026-09-18.

$MachineRoles = @{
    'PREISSWORKSHOP'  = 'main-pc'
    'SAMSUNG-FLEX'    = 'laptop'
    'DESKTOP-A60V7P2' = 'cnc'
}

function Get-MachineRole {
    $role = $MachineRoles[$env:COMPUTERNAME]
    if ($role) { return $role }
    return $env:COMPUTERNAME.ToLower()
}

function Assert-AgentHost {
    # Refuse installs and the employee on the shop PC. Exits the calling script.
    param([string]$What = 'This')
    if ((Get-MachineRole) -eq 'cnc') {
        Write-Host "  STOP  $env:COMPUTERNAME is the shop PC (cnc): HelmCNC appliance, no installs, no employee. $What belongs on main-pc (PREISSWORKSHOP). Nothing changed." -ForegroundColor Red
        exit 2
    }
}
