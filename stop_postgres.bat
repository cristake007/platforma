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
