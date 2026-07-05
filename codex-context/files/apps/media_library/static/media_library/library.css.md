# apps/media_library/static/media_library/library.css

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/media_library/static/media_library/library.css`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `static`
- Size: 302 bytes
- Source SHA-256: `7d5ecd95a776924c5b8d638f790f7214f7ec63e7574ecb950e5057a3238e0350`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```css
.media-asset-preview {
    position: relative;
    width: 100%;
    min-height: 0;
    flex: 0 0 auto;
    overflow: hidden;
    aspect-ratio: 4 / 3;
}

.media-asset-preview img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    padding: 0.75rem;
    object-fit: contain;
}
```
