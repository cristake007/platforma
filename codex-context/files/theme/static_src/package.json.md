# Source snapshot

## `theme/static_src/package.json`

Size: 1.1 KB

```json
{
  "name": "theme",
  "version": "4.5.0",
  "description": "",
  "scripts": {
    "start": "npm run dev",
    "build": "npm run build:clean && npm run build:tailwind && npm run build:vendor",
    "build:clean": "rimraf ../static/css/dist",
    "build:tailwind": "cross-env NODE_ENV=production postcss ./src/styles.css -o ../static/css/dist/styles.css --minify",
    "build:vendor": "shx mkdir -p ../static/js/vendor && shx cp node_modules/htmx.org/dist/htmx.min.js ../static/js/vendor/htmx.min.js && shx cp node_modules/alpinejs/dist/cdn.min.js ../static/js/vendor/alpine.min.js",
    "dev": "cross-env NODE_ENV=development CHOKIDAR_USEPOLLING=1 CHOKIDAR_INTERVAL=300 postcss ./src/styles.css -o ../static/css/dist/styles.css --watch"
  },
  "keywords": [],
  "author": "",
  "license": "MIT",
  "devDependencies": {
    "@tailwindcss/postcss": "^4.3.0",
    "cross-env": "^10.1.0",
    "daisyui": "^5.5.23",
    "postcss": "^8.5.15",
    "postcss-cli": "^11.0.1",
    "rimraf": "^6.1.3",
    "shx": "0.4.0",
    "tailwindcss": "^4.3.0"
  },
  "dependencies": {
    "alpinejs": "3.15.12",
    "htmx.org": "2.0.10"
  }
}
```
