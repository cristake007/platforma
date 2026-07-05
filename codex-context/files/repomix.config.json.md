# Source snapshot

## `repomix.config.json`

Size: 1.3 KB

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
