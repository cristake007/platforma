# theme/static_src/package.json

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `theme/static_src/package.json`
- App: none
- Role: `theme`
- Size: 781 bytes
- Source SHA-256: `b8ce596b0247722d3380363f615f350f5ac75e6c50195e9bc17ddccd65072a5c`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```json
{
  "name": "theme",
  "version": "4.5.0",
  "description": "",
  "scripts": {
    "start": "npm run dev",
    "build": "npm run build:clean && npm run build:tailwind",
    "build:clean": "rimraf ../static/css/dist",
    "build:tailwind": "cross-env NODE_ENV=production postcss ./src/styles.css -o ../static/css/dist/styles.css --minify",
    "dev": "cross-env NODE_ENV=development CHOKIDAR_USEPOLLING=1 CHOKIDAR_INTERVAL=300 postcss ./src/styles.css -o ../static/css/dist/styles.css --watch"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "devDependencies": {
    "@tailwindcss/postcss": "^4.3.0",
    "daisyui": "^5.5.23",
    "cross-env": "^10.1.0",
    "postcss": "^8.5.15",
    "postcss-cli": "^11.0.1",
    "rimraf": "^6.1.3",
    "tailwindcss": "^4.3.0"
  }
}
```
