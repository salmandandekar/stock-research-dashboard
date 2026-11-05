<#
Create a Windows Task Scheduler job that updates private_reports/latest.html
every Mon–Fri at 4:45 PM *computer local time*. Intended for Central Time.
Uses user-profile DPAPI encryption for Alpaca credentials; no secrets in task
arguments, public GitHub, source code, or URL.
Run from PowerShell after creating .venv and installing requirements.
#>
param(
    [string]$TaskName = "StockResearchPrivateDaily",
    [string]$AtLocalTime = "16:45",
    [switch]$KeepExistingCredential
)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $repo ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Missing venv Python. Run: py -3.12 -m venv .venv ; .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
}
$secretDir = Join-Path $env:APPDATA "StockResearch"
if (-not (Test-Path $secretDir)) { New-Item -Path $secretDir -ItemType Directory | Out-Null }
$secretPath = Join-Path $secretDir "alpaca-credentials.xml"
if (-not $KeepExistingCredential -or -not (Test-Path $secretPath)) {
    Write-Host "Enter an Alpaca paper/data API key ID in Username and its secret in Password."
    $credential = Get-Credential -Message "Alpaca data API (NOT live-trading keys)"
    if ($null -eq $credential) { throw "Credential setup cancelled." }
    $credential | Export-Clixml -Path $secretPath
    Write-Host "Encrypted credential saved for this Windows user and this computer."
}
$runner = Join-Path $PSScriptRoot "run_windows_private_report.ps1"
$arguments = '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + $runner + '" -PythonExe "' + $python + '"'
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $arguments -WorkingDirectory $repo
try { $clock = [DateTime]::Today.Add([TimeSpan]::Parse($AtLocalTime)) }
catch { throw "AtLocalTime must be HH:MM, e.g. 16:45." }
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday, Tuesday, Wednesday, Thursday, Friday -At $clock
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 25)
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Private, read-only, delayed end-of-day swing research. No trades." -Force | Out-Null
Write-Host "Task registered: $TaskName"
Write-Host "Scheduled at $AtLocalTime on weekdays using the COMPUTER'S LOCAL TIME. Set Windows timezone to Central, or adjust -AtLocalTime."
Write-Host "Run manually for a first test: Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "View report: $(Join-Path $repo 'private_reports\latest.html')"
