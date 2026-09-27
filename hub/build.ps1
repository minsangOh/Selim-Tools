# Selim Tools 허브 빌드: 테스트 → PyInstaller 폴더형 빌드 → NSIS 설치 파일 (dist\installer)
param(
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"

Push-Location $root
try {
    if (-not (Test-Path -LiteralPath $python)) {
        py -3.13 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "가상환경을 만들지 못했습니다. Python 3.13이 필요합니다." }
    }
    & $python -m pip install --disable-pip-version-check -q -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "라이브러리 설치에 실패했습니다." }

    # 다른 프로그램의 Qt·ICU DLL이 빌드에 섞이지 않게 PATH를 좁힌다 (작업지도서 앱과 같은 처리)
    $env:PATH = "$(Join-Path $root '.venv\Scripts');$env:SystemRoot\System32;$env:SystemRoot;$env:SystemRoot\System32\Wbem"

    if (-not $SkipTests) {
        $env:QT_QPA_PLATFORM = "offscreen"
        & $python -m unittest discover -s tests -v
        if ($LASTEXITCODE -ne 0) { throw "테스트에 실패했습니다." }
        Remove-Item Env:QT_QPA_PLATFORM
    }

    & $python -m PyInstaller --noconfirm --clean SelimTools.spec
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller 빌드에 실패했습니다." }

    $version = (Select-String -LiteralPath main.py -Pattern '^APP_VERSION = "(\d+\.\d+\.\d+)"$').Matches[0].Groups[1].Value
    # NSIS를 따로 설치하지 않았다면 Tauri(FileRay 빌드)가 받아 둔 NSIS를 쓴다
    $makensis = @(
        "${env:ProgramFiles(x86)}\NSIS\makensis.exe",
        "$env:ProgramFiles\NSIS\makensis.exe",
        "$env:LOCALAPPDATA\tauri\NSIS\makensis.exe"
    ) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $makensis) { throw "NSIS(makensis.exe)를 찾지 못했습니다. NSIS를 설치한 뒤 다시 실행하세요." }

    New-Item -ItemType Directory -Path (Join-Path $root "dist\installer") -Force | Out-Null
    & $makensis /INPUTCHARSET UTF8 "/DAPP_VERSION=$version" (Join-Path $root "installer\SelimTools.nsi")
    if ($LASTEXITCODE -ne 0) { throw "설치 파일을 만들지 못했습니다." }

    Write-Host "완료: dist\installer\SelimTools-Setup-$version.exe"
}
finally {
    Pop-Location
}
