# theme/static/js/user_menu.js

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `theme/static/js/user_menu.js`
- App: none
- Role: `static`
- Size: 2297 bytes
- Source SHA-256: `4eae8f5fc2b8bc9403a8bd5a71ddb931901a254c3157a700af0b41e867abc7bf`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(() => {
    const flyout = document.querySelector("[data-user-flyout]");
    if (!flyout) return;

    const trigger = flyout.querySelector("[data-user-flyout-trigger]");
    const panel = flyout.querySelector("[data-user-flyout-panel]");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const EXIT_DURATION = 160;
    let exitTimer = null;

    const finishClose = () => {
        if (exitTimer) window.clearTimeout(exitTimer);
        exitTimer = null;
        flyout.classList.remove("is-flyout-active", "is-flyout-closing", "is-flyout-preparing");
        flyout.open = false;
    };

    const openFlyout = () => {
        if (exitTimer) window.clearTimeout(exitTimer);
        exitTimer = null;
        flyout.open = true;
        flyout.classList.remove("is-flyout-closing");
        flyout.classList.add("is-flyout-active", "is-flyout-preparing");
        trigger?.setAttribute("aria-expanded", "true");
        window.requestAnimationFrame(() => {
            window.requestAnimationFrame(() => flyout.classList.remove("is-flyout-preparing"));
        });
    };

    const closeFlyout = ({ restoreFocus = false } = {}) => {
        if (!flyout.open || flyout.classList.contains("is-flyout-closing")) return;
        trigger?.setAttribute("aria-expanded", "false");
        if (restoreFocus) trigger?.focus();

        if (reducedMotion.matches) {
            finishClose();
            return;
        }

        flyout.classList.add("is-flyout-closing");
        exitTimer = window.setTimeout(finishClose, EXIT_DURATION);
    };

    trigger?.addEventListener("click", (event) => {
        event.preventDefault();
        if (flyout.open && !flyout.classList.contains("is-flyout-closing")) {
            closeFlyout();
        } else {
            openFlyout();
        }
    });

    document.addEventListener("pointerdown", (event) => {
        if (flyout.open && !flyout.contains(event.target)) closeFlyout();
    });

    flyout.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && flyout.open) {
            event.preventDefault();
            closeFlyout({ restoreFocus: true });
        }
    });

    panel?.addEventListener("click", (event) => {
        if (event.target.closest("a")) closeFlyout();
    });
})();
```
