<#
.SYNOPSIS
Keep Lantern Chat running in the current Windows user session.

.DESCRIPTION
This watchdog checks whether the native Lantern Chat desktop app is already
running for the current user. If not, it starts it from the repo.

Use this from an interactive user session or a logon Scheduled Task. Do not run
this as a classic Windows Service for the GUI app: services run outside the
normal desktop session and cannot reliably show the Tkinter window.

Boundary:
- local Windows user session only;
- starts only apps/lantern-desktop/lantern_desktop.py;
- no repo sync, reset, clean, merge, push, or agent start;
- no network tunnel;
- no hosted GPT/Claude/API call from this launcher.
#>

[CmdletBinding()]
param(
    [int]$IntervalSeconds = 30,
    [switch]$Once,
    [switch]$NoWindow
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $scriptDir = Split-Path -Parent $PSCommandPath
    return (Resolve-Path (Join-Path $scriptDir "..")).Path
}

function Get-LanternProcess {
    param([string]$AppPath)

    $escaped = [Regex]::Escape($AppPath)
    Get-CimInstance Win32_Process -Filter "name = 'python.exe' or name = 'pythonw.exe'" |
        Where-Object { $_.CommandLine -match $escaped }
}

function Start-LanternChat {
    param([string]$RepoRoot, [string]$AppPath, [switch]$NoWindow)

    if (-not (Test-Path $AppPath)) {
        throw "Lantern Chat app not found: $AppPath"
    }

    $pythonw = Join-Path (Split-Path -Parent (Get-Command python.exe).Source) "pythonw.exe"
    $python = if ($NoWindow -and (Test-Path $pythonw)) { $pythonw } else { (Get-Command python.exe).Source }

    Start-Process -FilePath $python -ArgumentList @($AppPath) -WorkingDirectory $RepoRoot | Out-Null
    Write-Host "Started Lantern Chat: $AppPath"
}

$repoRoot = Get-RepoRoot
$appPath = Join-Path $repoRoot "apps\lantern-desktop\lantern_desktop.py"

while ($true) {
    $running = @(Get-LanternProcess -AppPath $appPath)
    if ($running.Count -eq 0) {
        Start-LanternChat -RepoRoot $repoRoot -AppPath $appPath -NoWindow:$NoWindow
    }
    else {
        Write-Host "Lantern Chat already running. PID(s): $($running.ProcessId -join ', ')"
    }

    if ($Once) {
        break
    }
    Start-Sleep -Seconds ([Math]::Max(5, $IntervalSeconds))
}
