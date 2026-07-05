# apps/diplome/static/diplome/generation.js

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/static/diplome/generation.js`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `static`
- Size: 3357 bytes
- Source SHA-256: `22f9f0fa61627935e6c61a090b1ba8bd76fad9edfb40f3e3e02b1326a7bc9005`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(function () {
    "use strict";

    const listSelect = document.querySelector("[data-generation-list]");
    const participantTable = document.querySelector("[data-participant-table]");
    if (!listSelect || !participantTable) return;

    const participantRows = participantTable
        ? Array.from(participantTable.querySelectorAll("[data-participant-row]"))
        : [];
    const participantCount = participantTable.querySelector("[data-participant-count]");
    const participantEmpty = participantTable.querySelector("[data-participant-empty]");
    const participantTableBody = participantTable.querySelector("[data-participant-rows]");
    const participantScroll = participantTable.querySelector("[data-participant-scroll]");

    function syncSelectedRow() {
        let selectedCount = 0;
        participantRows.forEach((row) => {
            const checkbox = row.querySelector("[data-participant-checkbox]");
            const isSelected = checkbox.checked;
            if (!row.hidden && isSelected) selectedCount += 1;
            row.classList.toggle("bg-primary/10", isSelected);
            row.classList.toggle("hover:bg-base-200/70", !isSelected);
            row.setAttribute("aria-selected", String(isSelected));
        });
        participantCount.textContent = String(selectedCount);
    }

    function syncParticipantTable() {
        if (!participantTable) return;

        const listId = listSelect.value;
        let visibleCount = 0;
        participantRows.forEach((row) => {
            const isVisible = Boolean(listId && row.dataset.participantListId === listId);
            row.hidden = !isVisible;
            if (!isVisible) row.querySelector("[data-participant-checkbox]").checked = false;
            if (isVisible) visibleCount += 1;
        });
        participantTableBody.hidden = visibleCount === 0;
        participantEmpty.hidden = visibleCount > 0;
        participantEmpty.textContent = listId
            ? "Lista selectată nu conține participanți."
            : "Selectează mai întâi o listă cu participanți.";
        syncSelectedRow();
        const selectedRow = participantRows.find(
            (row) => !row.hidden && row.querySelector("[data-participant-checkbox]").checked
        );
        if (selectedRow) {
            participantScroll.scrollTop = Math.max(
                0,
                selectedRow.offsetTop - participantScroll.clientHeight / 2
            );
        }
    }

    function selectOnly(checkbox) {
        participantRows.forEach((row) => {
            const rowCheckbox = row.querySelector("[data-participant-checkbox]");
            if (rowCheckbox !== checkbox) rowCheckbox.checked = false;
        });
        syncSelectedRow();
    }

    participantRows.forEach((row) => {
        const checkbox = row.querySelector("[data-participant-checkbox]");
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) selectOnly(checkbox);
            else syncSelectedRow();
        });
        row.addEventListener("click", (event) => {
            if (row.hidden) return;
            if (event.target !== checkbox) {
                checkbox.checked = true;
                selectOnly(checkbox);
            }
        });
    });

    listSelect.addEventListener("change", syncParticipantTable);
    syncParticipantTable();
})();
```
