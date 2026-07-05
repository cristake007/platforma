# apps/planificator/static/planificator/generator.js

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/planificator/static/planificator/generator.js`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `static`
- Size: 9082 bytes
- Source SHA-256: `763d55ef2de2ac2698c2dda2fc4ee6ab1c78b2f551bee78e89d9ffb4bba8ad66`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(() => {
    const slider = document.getElementById("id_randomness");
    const yearInput = document.getElementById("id_year");
    const monthInputs = Array.from(document.querySelectorAll('input[name="months"]'));
    const fileInput = document.getElementById("id_input_file");
    const uploadDropzone = document.getElementById("ops-upload-dropzone");
    const holidayStore = document.getElementById("id_holidays");
    const holidayInput = document.getElementById("ops-holiday-date");
    const holidayList = document.getElementById("ops-holiday-list");
    const holidayLive = document.getElementById("ops-holiday-live");
    const workflow = document.getElementById("generator-workflow");
    const generatorForm = document.getElementById("generator-form");
    const sourceGenerationInput = document.getElementById("id_source_generation_id");
    const uploadPrompt = document.getElementById("ops-upload-prompt");
    const uploadState = document.getElementById("ops-upload-state");
    const uploadStatus = document.getElementById("ops-upload-status");
    const replaceUpload = document.getElementById("ops-replace-upload");
    const clearUpload = document.getElementById("ops-clear-upload");
    const clearProcessedUpload = document.getElementById("ops-clear-processed-upload");
    const uploadWarning = document.getElementById("ops-upload-warning");
    const uploadWarningText = document.getElementById("ops-upload-warning-text");

    const setText = (id, value) => {
        const element = document.getElementById(id);
        if (element) element.textContent = String(value);
    };
    const holidayItems = () => holidayStore ? holidayStore.value.split(/[\n,]+/).map((item) => item.trim()).filter(Boolean) : [];
    const writeHolidays = (items) => {
        if (holidayStore) holidayStore.value = items.join("\n");
        setText("ops-holiday-count", items.length);
    };
    const setWorkflowStep = (currentStep) => {
        document.querySelectorAll("[data-generator-step]").forEach((step) => {
            const stepNumber = Number(step.dataset.generatorStep);
            step.classList.toggle("step-primary", stepNumber < currentStep);
            step.classList.toggle("step-secondary", stepNumber === currentStep);
        });
        document.querySelectorAll("[data-generator-card]").forEach((card) => {
            const stepNumber = Number(card.dataset.generatorCard);
            card.classList.toggle("generator-card-complete", stepNumber < currentStep);
        });
        if (workflow) workflow.dataset.currentStep = String(currentStep);
    };
    const showUploadWarning = (message) => {
        if (uploadWarningText) uploadWarningText.textContent = message;
        uploadWarning?.classList.remove("hidden");
    };
    const hideUploadWarning = () => uploadWarning?.classList.add("hidden");
    const markSettingsDirty = () => {
        if (Number(workflow?.dataset.currentStep || 1) > 2) setWorkflowStep(2);
    };
    const selectedHoliday = () => {
        if (!holidayInput?.value) {
            holidayInput?.classList.add("input-error");
            return "";
        }
        holidayInput.classList.remove("input-error");
        const [year, month, day] = holidayInput.value.split("-");
        return `${day}.${month}.${year}`;
    };
    const renderHolidays = () => {
        if (!holidayList) return;
        holidayList.replaceChildren();
        holidayItems().forEach((item, index) => {
            const chip = document.createElement("span");
            chip.className = "join";
            const text = document.createElement("span");
            text.textContent = item;
            text.className = "btn btn-outline btn-primary btn-xs join-item pointer-events-none font-normal";
            const remove = document.createElement("button");
            remove.type = "button";
            remove.textContent = "×";
            remove.className = "btn btn-outline btn-primary btn-square btn-xs join-item";
            remove.setAttribute("aria-label", `Șterge data ${item}`);
            remove.addEventListener("click", () => {
                const next = holidayItems().filter((_, itemIndex) => itemIndex !== index);
                writeHolidays(next);
                renderHolidays();
                markSettingsDirty();
                if (holidayLive) holidayLive.textContent = `Data ${item} a fost ștearsă.`;
            });
            chip.append(text, remove);
            holidayList.append(chip);
        });
        setText("ops-holiday-count", holidayItems().length);
    };
    const syncMonths = () => {
        const selected = monthInputs.filter((input) => input.checked).length;
        setText("ops-month-count", selected);
        setText("ops-month-count-summary", selected);
        const submit = document.getElementById("ops-preview-submit");
        if (submit) submit.disabled = selected === 0;
        const toggle = document.getElementById("ops-toggle-months");
        if (toggle) toggle.textContent = selected === monthInputs.length ? "Deselectează toate" : "Selectează toate";
    };
    const syncSlider = () => {
        if (!slider) return;
        setText("ops-randomness-value", slider.value);
        setText("ops-randomness-summary", slider.value);
    };

    slider?.addEventListener("input", () => {
        syncSlider();
        markSettingsDirty();
    });
    yearInput?.addEventListener("change", () => {
        setText("ops-year-display", yearInput.value);
        markSettingsDirty();
    });
    monthInputs.forEach((input) => input.addEventListener("change", () => {
        syncMonths();
        markSettingsDirty();
    }));
    document.getElementById("ops-toggle-months")?.addEventListener("click", () => {
        const selectAll = monthInputs.some((input) => !input.checked);
        monthInputs.forEach((input) => { input.checked = selectAll; });
        syncMonths();
        markSettingsDirty();
    });
    document.getElementById("ops-add-holiday")?.addEventListener("click", () => {
        const formatted = selectedHoliday();
        if (!formatted) {
            holidayInput?.focus();
            if (holidayLive) holidayLive.textContent = "Data selectată nu este validă.";
            return;
        }
        const items = holidayItems();
        if (!items.includes(formatted)) items.push(formatted);
        writeHolidays(items);
        renderHolidays();
        markSettingsDirty();
        if (holidayLive) holidayLive.textContent = `Data ${formatted} a fost adăugată.`;
    });
    fileInput?.addEventListener("change", () => {
        const file = fileInput.files?.[0];
        if (!file) return;
        if (sourceGenerationInput) sourceGenerationInput.value = "";
        hideUploadWarning();
        uploadDropzone?.classList.remove("border-secondary", "border-dashed", "bg-base-200");
        uploadPrompt?.classList.add("hidden");
        uploadState?.classList.remove("hidden");
        replaceUpload?.classList.add("hidden");
        clearProcessedUpload?.classList.add("hidden");
        clearUpload?.classList.remove("hidden");
        setText("ops-upload-file-name", file.name);
        if (uploadStatus) uploadStatus.textContent = "Pregătit pentru validare";
        setWorkflowStep(2);
    });
    generatorForm?.addEventListener("submit", (event) => {
        const hasNewUpload = Boolean(fileInput?.files?.length);
        const hasProcessedUpload = Boolean(sourceGenerationInput?.value.trim());
        if (hasNewUpload || hasProcessedUpload) {
            hideUploadWarning();
            return;
        }
        event.preventDefault();
        showUploadWarning("Selectează un fișier CSV sau XLSX pentru a continua.");
        setWorkflowStep(1);
        uploadWarning?.scrollIntoView({ behavior: "smooth", block: "center" });
        fileInput?.focus({ preventScroll: true });
    });
    ["dragenter", "dragover"].forEach((eventName) => {
        uploadDropzone?.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadDropzone.classList.add("border-secondary", "bg-base-200");
        });
    });
    ["dragleave", "drop"].forEach((eventName) => {
        uploadDropzone?.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadDropzone.classList.remove("border-secondary", "bg-base-200");
        });
    });
    uploadDropzone?.addEventListener("drop", (event) => {
        const files = event.dataTransfer?.files;
        if (!fileInput || !files?.length) return;
        fileInput.files = files;
        fileInput.dispatchEvent(new Event("change", { bubbles: true }));
    });
    clearUpload?.addEventListener("click", () => {
        if (fileInput) fileInput.value = "";
        uploadState?.classList.add("hidden");
        uploadPrompt?.classList.remove("hidden");
        uploadDropzone?.classList.add("border-dashed");
        hideUploadWarning();
        setWorkflowStep(1);
    });

    setWorkflowStep(Number(workflow?.dataset.currentStep || 1));
    syncSlider();
    syncMonths();
    renderHolidays();
})();
```
