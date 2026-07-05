# stop_postgres.bat

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `stop_postgres.bat`
- App: none
- Role: `tooling`
- Size: 391 bytes
- Source SHA-256: `c4a3a34c9765ee8874f31a7f54a9627a6e85af6175187941737063033916bc6b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```bat
@echo off
setlocal

set "ROOT=%~dp0"
set "PG_CTL=%ROOT%.postgresql\pgsql\pgsql\bin\pg_ctl.exe"
set "PG_DATA=%ROOT%.postgresql\data"

if not exist "%PG_CTL%" (
    echo PostgreSQL binaries were not found.
    exit /b 1
)

if not exist "%PG_DATA%\PG_VERSION" (
    echo PostgreSQL data directory is not initialized.
    exit /b 1
)

"%PG_CTL%" -D "%PG_DATA%" stop -m fast
exit /b %ERRORLEVEL%
```
