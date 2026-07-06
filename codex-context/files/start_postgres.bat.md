# Source snapshot

## `start_postgres.bat`

Size: 119 B

```batch
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" setup dev
exit /b %ERRORLEVEL%
```
