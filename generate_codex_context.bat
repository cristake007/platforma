@echo off
python "%~dp0scripts\generate_codex_context.py" %*
exit /b %ERRORLEVEL%
