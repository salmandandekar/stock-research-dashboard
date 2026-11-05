<# Read encrypted user DPAPI credentials and generate a PRIVATE report. #>
param([Parameter(Mandatory=$true)][string]$PythonExe)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$secretPath = Join-Path $env:APPDATA "StockResearch\alpaca-credentials.xml"
if (-not (Test-Path $secretPath)) { throw "Encrypted credentials are missing. Run setup_windows_auto_report.ps1." }
$credential = Import-Clixml -Path $secretPath
$env:ALPACA_API_KEY_ID = $credential.UserName
$env:ALPACA_API_SECRET_KEY = $credential.GetNetworkCredential().Password
try {
    Push-Location $repo
    & $PythonExe (Join-Path $repo "private_trade_report.py") --source alpaca --feed sip
    if ($LASTEXITCODE -ne 0) { throw "Private research report failed; previous report retained." }
} finally {
    Pop-Location
    Remove-Item Env:ALPACA_API_KEY_ID -ErrorAction SilentlyContinue
    Remove-Item Env:ALPACA_API_SECRET_KEY -ErrorAction SilentlyContinue
}
