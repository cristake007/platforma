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
