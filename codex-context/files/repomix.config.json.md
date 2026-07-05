# repomix.config.json

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `repomix.config.json`
- App: none
- Role: `tooling`
- Size: 1293 bytes
- Source SHA-256: `36d5ece4e5f5c66b71c0ebe0b3f6d07935d2c526327faae9a498c80ff654012f`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```json
{
  "$schema": "https://repomix.com/schemas/latest/schema.json",
  "output": {
    "filePath": "repomix-codex.xml",
    "style": "xml",
    "parsableStyle": true,
    "truncateBase64": true
  },
  "ignore": {
    "useGitignore": true,
    "useDotIgnore": true,
    "useDefaultPatterns": true,
    "customPatterns": [
      ".agents/**",
      ".bootstrap_icons_cache/**",
      ".vscode/**",
      ".git/**",
      ".venv/**",
      ".postgresql/**",

      "plugins/playwright/**",
      "**/.playwright-mcp/**",
      "**/playwright-report/**",
      "**/test-results/**",
      "**/.codex-plugin/**",

      "**/__pycache__/**",
      "**/*.pyc",
      "**/*.pyo",

      "**/node_modules/**",
      "**/staticfiles/**",
      "**/media/**",
      "**/private_media/**",
      "apps/planificator-main/**",

      "theme/static/css/dist/**",
      "theme/static/fonts/**",
      "theme/static/images/**",

      "**/*.woff",
      "**/*.woff2",
      "**/*.ttf",
      "**/*.otf",
      "**/*.eot",

      "**/*.svg",
      "**/*.png",
      "**/*.jpg",
      "**/*.jpeg",
      "**/*.gif",
      "**/*.webp",
      "**/*.ico",

      "**/*.map",

      "repomix-output.*",
      "repomix-codex.*",
      "codex-file-map.txt"
    ]
  },
  "security": {
    "enableSecurityCheck": true
  }
}
```
