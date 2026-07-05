@echo off
setlocal EnableExtensions

echo This compatibility command now uses generate_codex_context_v3_ascii.bat.
call "%~dp0generate_codex_context_v3_ascii.bat"
exit /b %ERRORLEVEL%
