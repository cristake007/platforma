@echo off
setlocal EnableExtensions

call "%~dp0generate_codex_context_v3_ascii.bat"
exit /b %ERRORLEVEL%
