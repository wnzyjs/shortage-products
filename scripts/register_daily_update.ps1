$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$pythonExe = "C:\Users\Jason Yang\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$scriptPath = Join-Path $PSScriptRoot "update_dashboard.py"
$taskName = "GlobalShortageDashboardDailyUpdate"

if (-not (Test-Path $pythonExe)) {
  throw "Bundled Python not found: $pythonExe"
}

if (-not (Test-Path $scriptPath)) {
  throw "Update script not found: $scriptPath"
}

$action = New-ScheduledTaskAction -Execute $pythonExe -Argument "`"$scriptPath`"" -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Daily -At 08:30
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

Register-ScheduledTask `
  -TaskName $taskName `
  -Action $action `
  -Trigger $trigger `
  -Principal $principal `
  -Settings $settings `
  -Force | Out-Null

Write-Output "Registered daily task: $taskName"
