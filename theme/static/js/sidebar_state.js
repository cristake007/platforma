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
