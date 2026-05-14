$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$tweego = Join-Path $root "tools\vendor\tweego\tweego.exe"
$build = Join-Path $root "build"
$out = Join-Path $build "index.html"

if (!(Test-Path $tweego)) {
    throw "Tweego not found. Run tools\bootstrap_tweego.ps1 first."
}

New-Item -ItemType Directory -Force -Path $build | Out-Null
& $tweego -f sugarcube-2 -o $out `
    (Join-Path $root "src\passages") `
    (Join-Path $root "src\styles") `
    (Join-Path $root "src\scripts") `
    (Join-Path $root "src\assets")

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (!(Test-Path $out)) {
    throw "Build failed; expected $out"
}

Write-Host "Built $out"
