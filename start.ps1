# Launch SecureVision AI Backend and Frontend in separate windows
Write-Host "Launching SecureVision AI..." -ForegroundColor Green
Start-Process cmd -ArgumentList "/k `"$PSScriptRoot\run_backend.bat`""
Start-Process cmd -ArgumentList "/k `"$PSScriptRoot\run_frontend.bat`""
Write-Host "Backend and Frontend launched successfully!" -ForegroundColor Cyan
