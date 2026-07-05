# theme/static/js/sidebar_state.js

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `theme/static/js/sidebar_state.js`
- App: none
- Role: `static`
- Size: 561 bytes
- Source SHA-256: `49a66676b81a9ef2c1e7b7a0c085aae5b41da5649e2eead50d58c4f391532eba`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(() => {
    const toggle = document.getElementById("ops-sidebar");
    if (!toggle) return;

    const desktop = window.matchMedia("(min-width: 1024px)");
    const startsCollapsed = toggle.dataset.sidebarStartCollapsed === "true";
    let savedState = null;

    try {
        savedState = sessionStorage.getItem("ops-sidebar-expanded");
    } catch {
        // Storage can be unavailable in restricted browser contexts.
    }

    toggle.checked = desktop.matches
        && !startsCollapsed
        && (savedState === null || savedState === "true");
})();
```
