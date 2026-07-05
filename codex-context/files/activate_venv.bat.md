# activate_venv.bat

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `activate_venv.bat`
- App: none
- Role: `tooling`
- Size: 883 bytes
- Source SHA-256: `dd6708165ae91ef50371db8848ec9eb9e57d62286b5563cb2c673d0230401f92`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```bat
@echo off
setlocal

set "ROOT=%~dp0"
set "ACTIVATE_PS1=%ROOT%.venv\Scripts\Activate.ps1"

if not exist "%ACTIVATE_PS1%" (
    echo Virtual environment not found at "%ACTIVATE_PS1%".
    exit /b 1
)

powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$root = '%ROOT%'; $activate = '%ACTIVATE_PS1%'; $nodeDir = $null; $localNodeDir = Join-Path $env:LOCALAPPDATA 'Programs\nodejs'; if (Test-Path $localNodeDir) { $nodeDir = $localNodeDir }; if (-not $nodeDir) { $wingetRoot = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages\OpenJS.NodeJS.22_Microsoft.Winget.Source_8wekyb3d8bbwe'; $nodeDir = Get-ChildItem $wingetRoot -Directory -Filter 'node-v*-win-x64' -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1 -ExpandProperty FullName }; if ($nodeDir) { $env:Path = $nodeDir + ';' + $env:Path }; Set-Location -LiteralPath $root; & $activate"
```
