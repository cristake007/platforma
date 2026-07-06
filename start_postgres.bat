@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" setup dev
exit /b %ERRORLEVEL%
