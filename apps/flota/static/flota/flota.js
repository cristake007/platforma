(() => {
    const MS_PER_DAY = 24 * 60 * 60 * 1000;

    function startOfToday() {
        const now = new Date();
        return new Date(now.getFullYear(), now.getMonth(), now.getDate());
    }

    function pluralizedDays(value) {
        return `${value} ${value === 1 ? "zi" : "zile"}`;
    }

    function setTone(badge, tone) {
        badge.classList.remove("badge-success", "badge-warning", "badge-error", "badge-ghost");
        badge.classList.toggle("badge-outline", tone !== "neutral");
        badge.classList.add(tone === "neutral" ? "badge-ghost" : `badge-${tone}`);
    }

    function refreshDeadlines() {
        const today = startOfToday();
        document.querySelectorAll("[data-deadline][data-due-date]").forEach((badge) => {
            const parts = badge.dataset.dueDate.split("-").map(Number);
            if (parts.length !== 3 || parts.some(Number.isNaN)) return;
            const due = new Date(parts[0], parts[1] - 1, parts[2]);
            const days = Math.round((due - today) / MS_PER_DAY);
            if (days < 0) {
                badge.textContent = `Expirat de ${pluralizedDays(Math.abs(days))}`;
                setTone(badge, "error");
            } else if (days === 0) {
                badge.textContent = "Scadent astăzi";
                setTone(badge, "error");
            } else if (days <= 30) {
                badge.textContent = `Scadent în ${pluralizedDays(days)}`;
                setTone(badge, "warning");
            } else {
                badge.textContent = "Valabil";
                setTone(badge, "success");
            }
        });
    }

    refreshDeadlines();
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) refreshDeadlines();
    });
})();
