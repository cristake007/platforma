@echo off
setlocal

set "ROOT=%~dp0"
set "ACTIVATE_PS1=%ROOT%.venv\Scripts\Activate.ps1"

if not exist "%ACTIVATE_PS1%" (
    echo Virtual environment not found at "%ACTIVATE_PS1%".
    exit /b 1
)

powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$root = '%ROOT%'; $activate = '%ACTIVATE_PS1%'; $nodeDir = $null; $localNodeDir = Join-Path $env:LOCALAPPDATA 'Programs\nodejs'; if (Test-Path $localNodeDir) { $nodeDir = $localNodeDir }; if (-not $nodeDir) { $wingetRoot = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages\OpenJS.NodeJS.22_Microsoft.Winget.Source_8wekyb3d8bbwe'; $nodeDir = Get-ChildItem $wingetRoot -Directory -Filter 'node-v*-win-x64' -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1 -ExpandProperty FullName }; if ($nodeDir) { $env:Path = $nodeDir + ';' + $env:Path }; Set-Location -LiteralPath $root; & $activate"
