$ErrorActionPreference = "Stop"

$vendor = Join-Path $PSScriptRoot "vendor\tweego"
$exe = Join-Path $vendor "tweego.exe"
$zip = Join-Path $env:TEMP "tweego-2.1.1-windows-x64.zip"
$url = "https://github.com/tmedwards/tweego/releases/download/v2.1.1/tweego-2.1.1-windows-x64.zip"

if (Test-Path $exe) {
    Write-Host "Tweego already present at $exe"
    exit 0
}

New-Item -ItemType Directory -Force -Path $vendor | Out-Null
Invoke-WebRequest -Uri $url -OutFile $zip
Expand-Archive -LiteralPath $zip -DestinationPath $vendor -Force

if (!(Test-Path $exe)) {
    throw "Tweego bootstrap failed; expected $exe"
}

Write-Host "Tweego installed at $exe"
