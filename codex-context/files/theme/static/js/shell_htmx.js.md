# Source snapshot

## `theme/static/js/shell_htmx.js`

Size: 1.5 KB

```javascript
(() => {
    if (window.__opsShellHtmxInitialized) return;
    window.__opsShellHtmxInitialized = true;

    const syncShellNavigation = () => {
        const pageContent = document.getElementById("page-content");
        const activeUrl = pageContent?.dataset.activeNavUrl;
        if (!activeUrl) return;

        document.querySelectorAll("[data-shell-nav-url]").forEach((link) => {
            const isActive = link.dataset.shellNavUrl === activeUrl;
            link.classList.toggle("active", isActive);
            link.classList.toggle("font-semibold", isActive);
            if (isActive) {
                link.setAttribute("aria-current", "page");
            } else {
                link.removeAttribute("aria-current");
            }
        });

        document.querySelectorAll("[data-sidebar-flyout]").forEach((flyout) => {
            const hasActiveChild = Boolean(flyout.querySelector("[data-shell-nav-url].active"));
            flyout.open = hasActiveChild;
            flyout.querySelector("[data-sidebar-flyout-trigger]")
                ?.setAttribute("aria-expanded", String(hasActiveChild));
        });
    };

    document.addEventListener("htmx:afterSettle", syncShellNavigation);
    document.addEventListener("htmx:historyRestore", syncShellNavigation);
    document.addEventListener("htmx:responseError", (event) => {
        const responseUrl = event.detail.xhr.responseURL;
        if (responseUrl) window.location.assign(responseUrl);
    });

    syncShellNavigation();
})();
```
