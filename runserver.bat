@echo off
setlocal

set "ROOT=%~dp0"
set "PYTHON=%ROOT%.venv\Scripts\python.exe"
set "PG_BIN=%ROOT%.postgresql\pgsql\pgsql\bin"
set "PG_ISREADY=%PG_BIN%\pg_isready.exe"
set "PG_CTL=%PG_BIN%\pg_ctl.exe"
set "PG_DATA=%ROOT%.postgresql\data"
set "PG_LOG=%ROOT%.postgresql\postgresql.log"

if not exist "%PYTHON%" (
    echo Virtual environment not found at "%PYTHON%".
    exit /b 1
)

pushd "%ROOT%"

if exist "%PG_ISREADY%" if exist "%PG_DATA%\PG_VERSION" (
    "%PG_ISREADY%" -h 127.0.0.1 -p 5432 >nul 2>nul
    if errorlevel 1 (
        echo Starting local PostgreSQL...
        "%PG_CTL%" -D "%PG_DATA%" -l "%PG_LOG%" start >nul
        if errorlevel 1 (
            echo Failed to start local PostgreSQL.
            popd
            exit /b 1
        )
        timeout /t 2 /nobreak >nul
    )
)

"%PYTHON%" manage.py migrate
if errorlevel 1 (
    popd
    exit /b 1
)

echo Starting Django and Tailwind CSS watcher...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%runserver.ps1" %*
set "EXIT_CODE=%ERRORLEVEL%"

popd
exit /b %EXIT_CODE%
