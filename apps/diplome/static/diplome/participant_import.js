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
