# Source snapshot

## `runserver.bat`

Size: 116 B

```batch
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" dev %*
exit /b %ERRORLEVEL%
```
