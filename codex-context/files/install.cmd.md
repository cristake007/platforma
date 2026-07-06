# Source snapshot

## `install.cmd`

Size: 112 B

```batch
@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
exit /b %ERRORLEVEL%
```
