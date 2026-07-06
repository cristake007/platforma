@echo off
setlocal
set "ROOT=%~dp0"
if not exist "%ROOT%.venv\Scripts\Activate.ps1" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%install.ps1" setup dev
    if errorlevel 1 exit /b %ERRORLEVEL%
)
powershell.exe -NoExit -ExecutionPolicy Bypass -Command "Set-Location -LiteralPath '%ROOT%'; & '%ROOT%.venv\Scripts\Activate.ps1'"
