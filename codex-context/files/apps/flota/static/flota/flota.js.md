# apps/flota/static/flota/flota.js

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/flota/static/flota/flota.js`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `static`
- Size: 1760 bytes
- Source SHA-256: `f8f5d951940e4322a4d4a6483acddca67119cb9dea1ee9b76e48a543d7fc6934`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
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
```
