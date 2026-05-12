<#
.SYNOPSIS
Install Lantern Chat autostart for the current Windows user.

.DESCRIPTION
Creates or updates a per-user Scheduled Task named LanternChatWatchdog. The task
runs at user logon and calls scripts/watch_lantern_chat.ps1 to start Lantern Chat
if it is not already running.

This is intentionally not a classic Windows Service because Lantern Chat is a GUI
app and should run inside Alex's logged-in desktop session.

Usage:
  .\scripts\install_lantern_chat_autostart.ps1
  .\scripts\install_lantern_chat_autostart.ps1 -Remove

Boundary:
- current Windows user only;
- starts only the local Lantern Chat desktop app;
- no repo sync/reset/clean/merge/push;
- no agent, tunnel, deployment, or browser control.
#>

[CmdletBinding()]
param(
    [string]$TaskName = "LanternChatWatchdog",
    [int]$IntervalSeconds = 30,
    [switch]$Remove
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $scriptDir = Split-Path -Parent $PSCommandPath
    return (Resolve-Path (Join-Path $scriptDir "..")).Path
}

$repoRoot = Get-RepoRoot
$watchdog = Join-Path $repoRoot "scripts\watch_lantern_chat.ps1"

if ($Remove) {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "Removed Scheduled Task: $TaskName"
    }
    else {
        Write-Host "Scheduled Task not found: $TaskName"
    }
    return
}

if (-not (Test-Path $watchdog)) {
    throw "Watchdog script not found: $watchdog"
}

$argument = "-NoProfile -ExecutionPolicy Bypass -File `"$watchdog`" -IntervalSeconds $IntervalSeconds -NoWindow"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $argument -WorkingDirectory $repoRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
$task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Starts Lantern Chat if it is not running in the current user session."

Register-ScheduledTask -TaskName $TaskName -InputObject $task -Force | Out-Null
Write-Host "Installed Scheduled Task: $TaskName"
Write-Host "Repo: $repoRoot"
Write-Host "Watchdog: $watchdog"
Write-Host "To test once now: powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$watchdog`" -Once"
