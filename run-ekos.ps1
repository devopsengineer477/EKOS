$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "Building EKOS local search index..." -ForegroundColor Cyan
python tools/build_index.py
if ($LASTEXITCODE -ne 0) { throw "Index build failed." }
Write-Host "Starting EKOS local web application..." -ForegroundColor Green
python app/server.py
