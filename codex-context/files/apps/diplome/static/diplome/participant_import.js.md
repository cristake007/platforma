# apps/diplome/static/diplome/participant_import.js

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/static/diplome/participant_import.js`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `static`
- Size: 1401 bytes
- Source SHA-256: `b881f3f43c46b7d62cb7720abf4521358035ec29f2c291102cce593e727f1f6b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(() => {
    const form = document.querySelector("[data-participant-import-form]");
    const toast = document.querySelector("[data-participant-import-toast]");
    const toastMessage = toast?.querySelector("[data-participant-import-toast-message]");
    const listName = form?.querySelector("#id_list_name");
    const sourceFile = form?.querySelector("#id_source_file");
    let hideTimer;

    if (!form || !toast || !toastMessage || !listName || !sourceFile) {
        return;
    }

    const showError = (message, field) => {
        window.clearTimeout(hideTimer);
        toastMessage.textContent = message;
        toast.classList.remove("hidden");
        field.setAttribute("aria-invalid", "true");
        field.focus();
        hideTimer = window.setTimeout(() => toast.classList.add("hidden"), 5000);
    };

    listName.addEventListener("input", () => listName.removeAttribute("aria-invalid"));
    sourceFile.addEventListener("change", () => sourceFile.removeAttribute("aria-invalid"));

    form.addEventListener("submit", (event) => {
        if (!listName.value.trim()) {
            event.preventDefault();
            showError("Numele listei este obligatoriu.", listName);
            return;
        }
        if (!sourceFile.files.length) {
            event.preventDefault();
            showError("Selectează un fișier CSV sau XLSX.", sourceFile);
        }
    });
})();
```
