# Source snapshot

## `apps/tasks/static/tasks/tasks.js`

Size: 11.3 KB

```javascript
(() => {
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
        document.querySelectorAll("[data-task-timer]").forEach((element) => {
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

    let timerInterval = null;
    const initTimers = () => {
        updateTimers();
        if (!timerInterval && document.querySelector("[data-task-timer]")) {
            timerInterval = window.setInterval(updateTimers, 1000);
        }
    };

    const getDialog = () => document.getElementById("task-create-dialog");
    const getRoot = () => document.querySelector("[data-kanban-root]");
    const getCsrf = () => document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    let draggedCard = null;
    let requestInFlight = false;
    let knownSignature = null;
    let pollInterval = null;

    const updateCounts = () => document.querySelectorAll("[data-stage-column]").forEach((column) => {
        const count = column.querySelectorAll(":scope [data-stage-cards] > [data-task-card]").length;
        const target = column.querySelector("[data-stage-count]");
        if (target) target.textContent = String(count);
        const emptyState = column.querySelector("[data-stage-empty]");
        if (emptyState) emptyState.classList.toggle("hidden", count > 0);
    });

    const setDropState = (container, active) => {
        container.classList.toggle("outline", active);
        container.classList.toggle("outline-2", active);
        container.classList.toggle("outline-primary", active);
        container.classList.toggle("outline-offset-2", active);
        container.classList.toggle("border-primary", active);
        container.classList.toggle("bg-primary/10", active);
    };

    const setDragContext = (active) => {
        const board = document.querySelector("[data-kanban-board]");
        if (board) board.toggleAttribute("data-kanban-dragging", active);
        document.querySelectorAll("[data-stage-drop-zone]").forEach((container) => {
            container.classList.toggle("border-dashed", active);
            container.classList.toggle("border-base-300", active);
            container.classList.toggle("bg-base-100", active);
            container.classList.toggle("opacity-90", active);
        });
    };

    const markMoved = (card) => {
        card.classList.add("ring-2", "ring-success", "bg-success/10");
        window.setTimeout(() => card.classList.remove("ring-2", "ring-success", "bg-success/10"), 900);
    };

    const setDragDisabled = (disabled) => {
        document.querySelectorAll("[data-task-card][draggable=true]").forEach((card) => {
            card.classList.toggle("opacity-60", disabled);
            card.toggleAttribute("aria-disabled", disabled);
        });
    };

    const updateMovedCardTimer = (card, taskPayload) => {
        const timer = card.querySelector("[data-task-timer]");
        if (!timer || !Object.prototype.hasOwnProperty.call(taskPayload, "completedAt")) return;
        if (taskPayload.completedAt) timer.dataset.completedAt = taskPayload.completedAt;
        else delete timer.dataset.completedAt;
        updateTimers();
    };

    const initDragDrop = () => {
        document.querySelectorAll("[data-task-card][draggable=true]:not([data-kanban-drag-bound])").forEach((card) => {
            card.dataset.kanbanDragBound = "true";
            card.addEventListener("dragstart", () => {
                if (requestInFlight) return;
                draggedCard = card;
                setDragContext(true);
                card.classList.add("opacity-70", "ring-2", "ring-primary", "cursor-grabbing");
            });
            card.addEventListener("dragend", () => {
                card.classList.remove("opacity-70", "ring-2", "ring-primary", "cursor-grabbing");
                document.querySelectorAll("[data-stage-cards]").forEach((container) => setDropState(container, false));
                setDragContext(false);
                draggedCard = null;
            });
        });

        document.querySelectorAll("[data-stage-cards]:not([data-kanban-drop-bound])").forEach((container) => {
            container.dataset.kanbanDropBound = "true";
            container.addEventListener("dragover", (event) => {
                event.preventDefault();
                if (draggedCard && !requestInFlight) setDropState(container, true);
            });
            container.addEventListener("dragleave", (event) => {
                if (!container.contains(event.relatedTarget)) setDropState(container, false);
            });
            container.addEventListener("drop", async (event) => {
                event.preventDefault();
                setDropState(container, false);
                if (!draggedCard || requestInFlight) return;
                const card = draggedCard;
                const stageColumn = container.closest("[data-stage-column]");
                if (!stageColumn) return;
                const cards = Array.from(container.querySelectorAll(":scope > [data-task-card]")).filter((item) => item !== card);
                const target = event.target.closest("[data-task-card]");
                const targetIndex = target && target !== card ? cards.indexOf(target) : cards.length;
                const oldParent = card.parentElement;
                const reference = cards[targetIndex] || container.querySelector("[data-open-task-dialog]");
                container.insertBefore(card, reference || null);
                updateCounts();
                requestInFlight = true;
                setDragDisabled(true);
                card.setAttribute("aria-busy", "true");
                try {
                    const response = await fetch(card.dataset.moveUrl, {
                        method: "POST",
                        headers: {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": getCsrf()},
                        body: new URLSearchParams({stage: stageColumn.dataset.stageId, target_index: String(targetIndex), expected_version: card.dataset.taskVersion}),
                    });
                    const payload = await response.json();
                    if (!response.ok) throw new Error(payload.error || "Mutarea nu a putut fi salvată.");
                    card.dataset.taskVersion = String(payload.task.version);
                    const fallbackVersion = card.querySelector("[name=expected_version]");
                    if (fallbackVersion) fallbackVersion.value = String(payload.task.version);
                    const fallbackStage = card.querySelector("[name=stage]");
                    if (fallbackStage) fallbackStage.value = payload.task.stageId;
                    updateMovedCardTimer(card, payload.task);
                    knownSignature = null;
                    markMoved(card);
                } catch (error) {
                    oldParent.insertBefore(card, oldParent.querySelector("[data-open-task-dialog]") || null);
                    updateCounts();
                    window.alert(error.message);
                } finally {
                    card.removeAttribute("aria-busy");
                    setDragDisabled(false);
                    requestInFlight = false;
                }
            });
        });
    };

    const pollState = async () => {
        const root = getRoot();
        const dialog = getDialog();
        if (!root || document.hidden || requestInFlight || dialog?.open) return;
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

    const initPolling = () => {
        if (!pollInterval && getRoot()) {
            pollState();
            pollInterval = window.setInterval(pollState, 30000);
        }
    };

    const initKanban = ({resetSignature = false} = {}) => {
        initTimers();
        initDragDrop();
        if (resetSignature) knownSignature = null;
        initPolling();
    };

    document.addEventListener("change", (event) => {
        const select = event.target.closest("[data-board-switcher]");
        if (select) window.location.assign(select.value);
    });

    document.addEventListener("click", (event) => {
        const openButton = event.target.closest("[data-open-task-dialog]");
        if (openButton) getDialog()?.showModal();
        const closeButton = event.target.closest("[data-close-task-dialog]");
        if (closeButton) getDialog()?.close();
    });

    document.addEventListener("taskKanban:taskCreated", () => getDialog()?.close());
    document.addEventListener("htmx:afterSwap", () => initKanban({resetSignature: true}));
    document.addEventListener("htmx:oobAfterSwap", () => initKanban({resetSignature: true}));

    initKanban();
})();
```
