$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path '.\files' | Out-Null
if (-not (Test-Path '.\automation_config.json')) {
  $bytes = New-Object byte[] 32
  [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
  $token = [Convert]::ToHexString($bytes).ToLowerInvariant()
  @{ token = $token } | ConvertTo-Json | Set-Content -Encoding utf8 '.\automation_config.json'
  Write-Host 'Created local automation_config.json. Keep its token private.' -ForegroundColor Green
} else {
  Write-Host 'Using existing automation_config.json (not overwritten).' -ForegroundColor Yellow
}
Write-Host 'Next: docker compose up -d --build'
Write-Host 'Dashboard: http://localhost:8000  |  n8n: http://localhost:5678'
