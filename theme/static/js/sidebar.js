(() => {
    const toggle = document.getElementById("ops-sidebar");
    if (!toggle) return;

    const desktop = window.matchMedia("(min-width: 1024px)");
    const startsCollapsed = Boolean(document.querySelector('[data-sidebar-start-collapsed="true"]'));
    const flyouts = Array.from(document.querySelectorAll("[data-sidebar-flyout]"));
    const closeTimers = new WeakMap();
    const exitTimers = new WeakMap();
    const CLOSE_DELAY = 220;
    const EXIT_DURATION = 160;
    const isCollapsed = () => desktop.matches && !toggle.checked;

    const clearCloseTimer = (flyout) => {
        const timer = closeTimers.get(flyout);
        if (timer) window.clearTimeout(timer);
        closeTimers.delete(flyout);
    };

    const cancelClose = (flyout) => {
        clearCloseTimer(flyout);
        const timer = exitTimers.get(flyout);
        if (timer) window.clearTimeout(timer);
        exitTimers.delete(flyout);
        if (flyout.open) {
            flyout.classList.remove("is-flyout-closing");
            flyout.querySelector("[data-sidebar-flyout-trigger]")?.setAttribute("aria-expanded", "true");
        }
    };

    const finishClose = (flyout) => {
        clearCloseTimer(flyout);
        const timer = exitTimers.get(flyout);
        if (timer) window.clearTimeout(timer);
        exitTimers.delete(flyout);
        flyout.classList.remove("is-flyout-active", "is-flyout-closing", "is-flyout-preparing");
        flyout.open = false;
        flyout.querySelector("[data-sidebar-flyout-trigger]")?.setAttribute("aria-expanded", "false");
    };

    const closeFlyout = (flyout, { immediate = false, restoreFocus = false } = {}) => {
        clearCloseTimer(flyout);
        if (!flyout.open) return;

        const trigger = flyout.querySelector("[data-sidebar-flyout-trigger]");
        if (restoreFocus) trigger?.focus();
        trigger?.setAttribute("aria-expanded", "false");

        if (immediate || !isCollapsed() || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            finishClose(flyout);
            return;
        }

        flyout.classList.add("is-flyout-closing");
        exitTimers.set(flyout, window.setTimeout(() => finishClose(flyout), EXIT_DURATION));
    };

    const scheduleClose = (flyout) => {
        if (!isCollapsed() || !flyout.open) return;
        const panel = flyout.querySelector("[data-sidebar-flyout-panel]");
        if (panel?.contains(document.activeElement)) return;
        clearCloseTimer(flyout);
        closeTimers.set(flyout, window.setTimeout(() => closeFlyout(flyout), CLOSE_DELAY));
    };

    const prepareOpenAnimation = (flyout) => {
        if (!isCollapsed()) return;
        flyout.classList.remove("is-flyout-closing");
        flyout.classList.add("is-flyout-preparing");
        window.requestAnimationFrame(() => {
            window.requestAnimationFrame(() => flyout.classList.remove("is-flyout-preparing"));
        });
    };

    flyouts.forEach((flyout) => {
        const trigger = flyout.querySelector("[data-sidebar-flyout-trigger]");
        trigger?.setAttribute("aria-expanded", String(flyout.open));

        flyout.addEventListener("toggle", () => {
            if (flyout.open) {
                trigger?.setAttribute("aria-expanded", "true");
                if (isCollapsed()) {
                    flyouts.forEach((other) => {
                        if (other !== flyout) closeFlyout(other, { immediate: true });
                    });
                    flyout.classList.add("is-flyout-active");
                    prepareOpenAnimation(flyout);
                }
            } else {
                flyout.classList.remove("is-flyout-active", "is-flyout-closing", "is-flyout-preparing");
                trigger?.setAttribute("aria-expanded", "false");
            }
        });
        flyout.addEventListener("pointerenter", () => cancelClose(flyout));
        flyout.addEventListener("pointerleave", () => scheduleClose(flyout));
        flyout.addEventListener("focusin", () => clearCloseTimer(flyout));
        flyout.addEventListener("focusout", (event) => {
            if (!flyout.contains(event.relatedTarget)) scheduleClose(flyout);
        });
        flyout.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && isCollapsed() && flyout.open) {
                event.preventDefault();
                closeFlyout(flyout, { restoreFocus: true });
            }
        });
    });

    const applyState = () => {
        if (desktop.matches) {
            if (startsCollapsed) {
                toggle.checked = false;
            } else {
                const saved = sessionStorage.getItem("ops-sidebar-expanded");
                toggle.checked = saved === null ? true : saved === "true";
            }
        } else {
            toggle.checked = false;
        }
        if (isCollapsed()) flyouts.forEach((flyout) => closeFlyout(flyout, { immediate: true }));
    };

    toggle.addEventListener("change", () => {
        if (desktop.matches) {
            sessionStorage.setItem("ops-sidebar-expanded", String(toggle.checked));
        }
        flyouts.forEach((flyout) => {
            cancelClose(flyout);
            if (isCollapsed()) closeFlyout(flyout, { immediate: true });
        });
    });
    document.addEventListener("pointerdown", (event) => {
        if (!isCollapsed()) return;
        flyouts.forEach((flyout) => {
            if (flyout.open && !flyout.contains(event.target)) closeFlyout(flyout);
        });
    });
    desktop.addEventListener("change", applyState);
    applyState();
})();
