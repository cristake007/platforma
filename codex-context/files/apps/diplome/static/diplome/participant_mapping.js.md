# apps/diplome/static/diplome/participant_mapping.js

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/static/diplome/participant_mapping.js`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `static`
- Size: 1690 bytes
- Source SHA-256: `497c4f341ccb06b2ddf368272cf37ffd341bb477643bfffbaf1162a52f7d7430`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(() => {
    "use strict";

    const form = document.querySelector("[data-mapping-form]");
    if (!form) return;

    const selects = Array.from(form.querySelectorAll("[data-mapping-select]"));
    const mappedCount = form.querySelector("[data-mapped-count]");

    function refreshMappingState() {
        const selectedValues = selects.map((select) => select.value).filter(Boolean);

        selects.forEach((select) => {
            Array.from(select.options).forEach((option) => {
                option.disabled = Boolean(
                    option.value &&
                    option.value !== select.value &&
                    selectedValues.includes(option.value)
                );
            });

            const row = select.closest("[data-mapping-row]");
            const isMapped = Boolean(select.value);
            row.classList.toggle("border-base-300", !isMapped);
            row.classList.toggle("border-primary", isMapped);
            row.classList.toggle("bg-base-100", !isMapped);
            row.classList.toggle("bg-primary/5", isMapped);
            row.querySelector("[data-mapped-icon]").classList.toggle("hidden", !isMapped);
            row.querySelector("[data-ignored-icon]").classList.toggle("hidden", isMapped);
            row.querySelector("[data-status-label]").textContent = isMapped ? "Asociată" : "Ignorată";
            row.querySelector("[data-mapping-status]").classList.toggle("text-success", isMapped);
        });

        if (mappedCount) mappedCount.textContent = String(new Set(selectedValues).size);
    }

    selects.forEach((select) => select.addEventListener("change", refreshMappingState));
    refreshMappingState();
})();
```
