(() => {
    const timerElements = Array.from(document.querySelectorAll("[data-task-timer]"));

    const formatDuration = (milliseconds) => {
        const totalSeconds = Math.max(0, Math.floor(Math.abs(milliseconds) / 1000));
        const days = Math.floor(totalSeconds / 86400);
        const hours = Math.floor((totalSeconds % 86400) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        if (days > 0) return `${days}z ${String(hours).padStart(2, "0")}h`;
        if (hours > 0) return `${String(hours).padStart(2, "0")}h ${String(minutes).padStart(2, "0")}m`;
        return `${String(minutes).padStart(2, "0")}m ${String(seconds).padStart(2, "0")}s`;
    };

    const setTimerTone = (element, tone) => {
        element.classList.remove("border-success", "text-success", "border-warning", "text-warning", "border-error", "text-error", "border-info", "text-info", "border-base-300");
        if (tone === "success") element.classList.add("border-success", "text-success");
        else if (tone === "warning") element.classList.add("border-warning", "text-warning");
        else if (tone === "error") element.classList.add("border-error", "text-error");
        else element.classList.add("border-info", "text-info");
    };

    const updateTimers = () => {
        const now = Date.now();
        timerElements.forEach((element) => {
            const label = element.querySelector("[data-timer-label]");
            if (!label) return;
            if (element.dataset.completedAt) {
                label.textContent = "Finalizat";
                setTimerTone(element, "success");
                return;
            }
            const start = Date.parse(element.dataset.startAt);
            const due = Date.parse(element.dataset.dueAt);
            if (!Number.isFinite(start) || !Number.isFinite(due) || due <= start) {
                label.textContent = "Termen invalid";
                setTimerTone(element, "error");
                return;
            }
            if (now < start) {
                label.textContent = `Începe în ${formatDuration(start - now)}`;
                setTimerTone(element, "success");
                return;
            }
            const progress = (now - start) / (due - start);
            if (now >= due) {
                label.textContent = `Depășit cu ${formatDuration(now - due)}`;
                setTimerTone(element, "error");
            } else {
                label.textContent = `${formatDuration(due - now)} rămase`;
                setTimerTone(element, progress < 0.5 ? "success" : progress < 0.8 ? "warning" : "error");
            }
        });
    };
    updateTimers();
    if (timerElements.length) window.setInterval(updateTimers, 1000);

    document.querySelectorAll("[data-board-switcher]").forEach((select) => {
        select.addEventListener("change", () => { window.location.assign(select.value); });
    });

    const dialog = document.getElementById("task-create-dialog");
    document.querySelectorAll("[data-open-task-dialog]").forEach((button) => button.addEventListener("click", () => dialog?.showModal()));
    document.querySelectorAll("[data-close-task-dialog]").forEach((button) => button.addEventListener("click", () => dialog?.close()));

    const root = document.querySelector("[data-kanban-root]");
    if (!root) return;
    const csrf = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    let draggedCard = null;
    let requestInFlight = false;

    const updateCounts = () => document.querySelectorAll("[data-stage-column]").forEach((column) => {
        const count = column.querySelectorAll(":scope [data-stage-cards] > [data-task-card]").length;
        const target = column.querySelector("[data-stage-count]");
        if (target) target.textContent = String(count);
    });

    document.querySelectorAll("[data-task-card][draggable=true]").forEach((card) => {
        card.addEventListener("dragstart", () => { draggedCard = card; card.classList.add("opacity-50"); });
        card.addEventListener("dragend", () => { card.classList.remove("opacity-50"); draggedCard = null; });
    });

    document.querySelectorAll("[data-stage-cards]").forEach((container) => {
        container.addEventListener("dragover", (event) => event.preventDefault());
        container.addEventListener("drop", async (event) => {
            event.preventDefault();
            if (!draggedCard || requestInFlight) return;
            const card = draggedCard;
            const cards = Array.from(container.querySelectorAll(":scope > [data-task-card]")).filter((item) => item !== card);
            const target = event.target.closest("[data-task-card]");
            const targetIndex = target && target !== card ? cards.indexOf(target) : cards.length;
            const oldParent = card.parentElement;
            const reference = cards[targetIndex] || container.querySelector("[data-open-task-dialog]");
            container.insertBefore(card, reference || null);
            updateCounts();
            requestInFlight = true;
            try {
                const response = await fetch(card.dataset.moveUrl, {
                    method: "POST",
                    headers: {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": csrf},
                    body: new URLSearchParams({stage: container.closest("[data-stage-column]").dataset.stageId, target_index: String(targetIndex), expected_version: card.dataset.taskVersion}),
                });
                const payload = await response.json();
                if (!response.ok) throw new Error(payload.error || "Mutarea nu a putut fi salvată.");
                card.dataset.taskVersion = String(payload.task.version);
                const fallbackVersion = card.querySelector("[name=expected_version]");
                if (fallbackVersion) fallbackVersion.value = String(payload.task.version);
                const fallbackStage = card.querySelector("[name=stage]");
                if (fallbackStage) fallbackStage.value = payload.task.stageId;
            } catch (error) {
                oldParent.insertBefore(card, oldParent.querySelector("[data-open-task-dialog]") || null);
                updateCounts();
                window.alert(error.message);
            } finally {
                requestInFlight = false;
            }
        });
    });

    let knownSignature = null;
    const pollState = async () => {
        if (document.hidden || requestInFlight || dialog?.open) return;
        try {
            const response = await fetch(root.dataset.stateUrl, {headers: {"Accept": "application/json"}});
            if (!response.ok) return;
            const payload = await response.json();
            if (knownSignature === null) knownSignature = payload.signature;
            else if (knownSignature !== payload.signature) window.location.reload();
        } catch (_) {
            // A later poll retries; local task operations remain server-authoritative.
        }
    };
    pollState();
    window.setInterval(pollState, 30000);
})();
