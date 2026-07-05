# generate_codex_context.bat

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `generate_codex_context.bat`
- App: none
- Role: `tooling`
- Size: 106 bytes
- Source SHA-256: `737191a754c4bd99bd5a5bae2bc60cfd35f64801db409da8ca27858cddc01954`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```bat
@echo off
setlocal EnableExtensions

call "%~dp0generate_codex_context_v3_ascii.bat"
exit /b %ERRORLEVEL%
```
