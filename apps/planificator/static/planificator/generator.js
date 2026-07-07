(() => {
    const initGeneratorWorkflow = (root = document) => {
        const workflow = root.querySelector?.("#generator-workflow") || document.getElementById("generator-workflow");
        if (!workflow || workflow.dataset.generatorInitialized === "true") return;
        workflow.dataset.generatorInitialized = "true";

        const slider = workflow.querySelector("#id_randomness");
        const yearInput = workflow.querySelector("#id_year");
        const monthInputs = Array.from(workflow.querySelectorAll('input[name="months"]'));
        const fileInput = workflow.querySelector("#id_input_file");
        const uploadDropzone = workflow.querySelector("#ops-upload-dropzone");
        const holidayStore = workflow.querySelector("#id_holidays");
        const holidayInput = workflow.querySelector("#ops-holiday-date");
        const holidayList = workflow.querySelector("#ops-holiday-list");
        const holidayLive = workflow.querySelector("#ops-holiday-live");
        const generatorForm = workflow.querySelector("#generator-form");
        const sourceGenerationInput = workflow.querySelector("#id_source_generation_id");
        const uploadPrompt = workflow.querySelector("#ops-upload-prompt");
        const uploadState = workflow.querySelector("#ops-upload-state");
        const uploadStatus = workflow.querySelector("#ops-upload-status");
        const replaceUpload = workflow.querySelector("#ops-replace-upload");
        const clearUpload = workflow.querySelector("#ops-clear-upload");
        const clearProcessedUpload = workflow.querySelector("#ops-clear-processed-upload");
        const uploadWarning = workflow.querySelector("#ops-upload-warning");
        const uploadWarningText = workflow.querySelector("#ops-upload-warning-text");

        const setText = (id, value) => {
            const element = workflow.querySelector(`#${id}`);
            if (element) element.textContent = String(value);
        };
        const holidayItems = () => holidayStore ? holidayStore.value.split(/[\n,]+/).map((item) => item.trim()).filter(Boolean) : [];
        const writeHolidays = (items) => {
            if (holidayStore) holidayStore.value = items.join("\n");
            setText("ops-holiday-count", items.length);
        };
        const setWorkflowStep = (currentStep) => {
            workflow.querySelectorAll("[data-generator-step]").forEach((step) => {
                const stepNumber = Number(step.dataset.generatorStep);
                step.classList.toggle("step-primary", stepNumber < currentStep);
                step.classList.toggle("step-secondary", stepNumber === currentStep);
            });
            workflow.querySelectorAll("[data-generator-card]").forEach((card) => {
                const stepNumber = Number(card.dataset.generatorCard);
                card.classList.toggle("generator-card-complete", stepNumber < currentStep);
            });
            workflow.dataset.currentStep = String(currentStep);
        };
        const showUploadWarning = (message) => {
            if (uploadWarningText) uploadWarningText.textContent = message;
            uploadWarning?.classList.remove("hidden");
        };
        const hideUploadWarning = () => uploadWarning?.classList.add("hidden");
        const markSettingsDirty = () => {
            if (Number(workflow.dataset.currentStep || 1) > 2) setWorkflowStep(2);
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
            const submit = workflow.querySelector("#ops-preview-submit");
            if (submit) submit.disabled = selected === 0;
            const toggle = workflow.querySelector("#ops-toggle-months");
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
        workflow.querySelector("#ops-toggle-months")?.addEventListener("click", () => {
            const selectAll = monthInputs.some((input) => !input.checked);
            monthInputs.forEach((input) => { input.checked = selectAll; });
            syncMonths();
            markSettingsDirty();
        });
        workflow.querySelector("#ops-add-holiday")?.addEventListener("click", () => {
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

        setWorkflowStep(Number(workflow.dataset.currentStep || 1));
        syncSlider();
        syncMonths();
        renderHolidays();
    };

    document.addEventListener("DOMContentLoaded", () => initGeneratorWorkflow());
    document.body.addEventListener("htmx:afterSwap", (event) => {
        if (event.detail?.target?.id === "generator-workflow") {
            initGeneratorWorkflow(event.detail.target);
        }
    });
})();
