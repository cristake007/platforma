# start_postgres.bat

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `start_postgres.bat`
- App: none
- Role: `tooling`
- Size: 2822 bytes
- Source SHA-256: `1fbbd5a11114b6df415764349300fba29f9082bb8bd72a7009028a8523c01d65`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```bat
@echo off
setlocal

set "ROOT=%~dp0"
set "PG_BIN=%ROOT%.postgresql\pgsql\pgsql\bin"
set "PG_ISREADY=%PG_BIN%\pg_isready.exe"
set "PG_CTL=%PG_BIN%\pg_ctl.exe"
set "PG_INITDB=%PG_BIN%\initdb.exe"
set "PG_PSQL=%PG_BIN%\psql.exe"
set "PG_CREATEDB=%PG_BIN%\createdb.exe"
set "PG_DATA=%ROOT%.postgresql\data"
set "PG_LOG=%ROOT%.postgresql\postgresql.log"

if not defined POSTGRES_DB set "POSTGRES_DB=platforma_tuvtk"
if not defined POSTGRES_USER set "POSTGRES_USER=postgres"
if not defined POSTGRES_PASSWORD set "POSTGRES_PASSWORD=postgres"
if not defined POSTGRES_HOST set "POSTGRES_HOST=127.0.0.1"
if not defined POSTGRES_PORT set "POSTGRES_PORT=5432"
if not defined PGPASSWORD set "PGPASSWORD=%POSTGRES_PASSWORD%"

if not exist "%PG_CTL%" (
    echo PostgreSQL binaries were not found in "%PG_BIN%".
    exit /b 1
)

if not exist "%PG_DATA%\PG_VERSION" (
    echo Initializing a new UTF8 PostgreSQL cluster at "%PG_DATA%"...
    "%PG_INITDB%" -D "%PG_DATA%" -U "%POSTGRES_USER%" --encoding=UTF8 --locale=C --auth=trust
    if errorlevel 1 exit /b 1
)

"%PG_ISREADY%" -h "%POSTGRES_HOST%" -p "%POSTGRES_PORT%" >nul 2>nul
if not errorlevel 1 goto postgres_ready

"%PG_CTL%" -D "%PG_DATA%" -l "%PG_LOG%" start
if errorlevel 1 exit /b 1

set /a READY_ATTEMPTS=0
:wait_for_postgres
"%PG_ISREADY%" -h "%POSTGRES_HOST%" -p "%POSTGRES_PORT%" >nul 2>nul
if not errorlevel 1 goto postgres_ready
set /a READY_ATTEMPTS+=1
if %READY_ATTEMPTS% GEQ 30 goto postgres_timeout
>nul 2>nul ping 127.0.0.1 -n 2
goto wait_for_postgres

:postgres_timeout
echo PostgreSQL did not become ready on %POSTGRES_HOST%:%POSTGRES_PORT%.
exit /b 1

:postgres_ready
set "ENCODING_FILE=%TEMP%\tuvtk_postgres_encoding_%RANDOM%.txt"
"%PG_PSQL%" -h "%POSTGRES_HOST%" -p "%POSTGRES_PORT%" -U "%POSTGRES_USER%" -d postgres -Atc "SELECT pg_encoding_to_char(encoding) FROM pg_database WHERE datname = '%POSTGRES_DB%';" > "%ENCODING_FILE%"
if errorlevel 1 (
    del "%ENCODING_FILE%" >nul 2>nul
    exit /b 1
)
set "DB_ENCODING="
set /p DB_ENCODING=<"%ENCODING_FILE%"
del "%ENCODING_FILE%" >nul 2>nul

if not defined DB_ENCODING (
    echo Creating UTF8 database "%POSTGRES_DB%"...
    "%PG_CREATEDB%" -h "%POSTGRES_HOST%" -p "%POSTGRES_PORT%" -U "%POSTGRES_USER%" --encoding=UTF8 --locale=C --template=template0 "%POSTGRES_DB%"
    if errorlevel 1 exit /b 1
    set "DB_ENCODING=UTF8"
)

if /I not "%DB_ENCODING%"=="UTF8" (
    echo ERROR: Database "%POSTGRES_DB%" uses %DB_ENCODING%, not UTF8.
    echo PostgreSQL cannot change a database encoding in place.
    echo Back up any required data, drop and recreate this database, then rerun start_postgres.bat.
    echo Example: "%PG_BIN%\dropdb.exe" -h "%POSTGRES_HOST%" -p "%POSTGRES_PORT%" -U "%POSTGRES_USER%" "%POSTGRES_DB%"
    exit /b 1
)

echo PostgreSQL is ready. Database "%POSTGRES_DB%" uses UTF8.
exit /b 0
```
