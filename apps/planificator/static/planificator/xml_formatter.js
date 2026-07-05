(() => {
    const form = document.getElementById('xml-export-form');
    if (!form) {
        return;
    }

    const fileInput = document.getElementById('id_input_file');
    const fileSelect = document.getElementById('xml-file-select');
    const fileName = document.getElementById('xml-file-name');
    const fileError = document.getElementById('xml-file-error');
    const postIdInput = document.getElementById('id_start_post_id');
    const postIdError = document.getElementById('xml-post-id-error');
    const errorAlert = document.getElementById('xml-export-error');
    const successAlert = document.getElementById('xml-export-success');
    const generateButton = document.getElementById('xml-generate-button');
    const loading = document.getElementById('xml-export-loading');
    let busy = false;

    function setHidden(element, hidden) {
        element.classList.toggle('hidden', hidden);
        if (element === loading) {
            element.classList.toggle('flex', !hidden);
        }
    }

    function clearMessages() {
        errorAlert.textContent = '';
        successAlert.textContent = '';
        setHidden(errorAlert, true);
        setHidden(successAlert, true);
    }

    function setFieldError(message) {
        fileError.textContent = message;
        setHidden(fileError, !message);
        fileInput.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function setPostIdError(message) {
        postIdError.textContent = message;
        setHidden(postIdError, !message);
        postIdInput.classList.toggle('input-error', Boolean(message));
        postIdInput.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function responseFilename(response) {
        const disposition = response.headers.get('Content-Disposition') || '';
        const match = disposition.match(/filename="?([^";]+)"?/i);
        return match?.[1] || form.dataset.downloadFilename;
    }

    function downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
    }

    fileSelect.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        const selected = fileInput.files[0];
        fileName.textContent = selected?.name || 'Niciun fișier selectat';
        fileName.classList.toggle('text-muted', !selected);
        setFieldError('');
        clearMessages();
    });

    postIdInput.addEventListener('input', () => setPostIdError(''));

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (busy) {
            return;
        }
        if (!fileInput.files.length) {
            setFieldError('Selectează un fișier CSV sau XLSX.');
            return;
        }
        const postId = Number(postIdInput.value);
        if (!Number.isInteger(postId) || postId < 1 || postId > 2147483647) {
            setPostIdError('Introdu un Post ID întreg între 1 și 2147483647.');
            return;
        }

        busy = true;
        generateButton.disabled = true;
        clearMessages();
        setFieldError('');
        setPostIdError('');
        setHidden(loading, false);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
            });
            if (!response.ok) {
                const payload = await response.json().catch(() => ({}));
                throw new Error(payload.error || 'Fișierul XML nu a putut fi generat.');
            }
            downloadBlob(await response.blob(), responseFilename(response));
            successAlert.textContent = 'Fișierul XML a fost generat.';
            setHidden(successAlert, false);
            form.reset();
            fileName.textContent = 'Niciun fișier selectat';
            fileName.classList.add('text-muted');
        } catch (error) {
            errorAlert.textContent = error.message;
            setHidden(errorAlert, false);
        } finally {
            busy = false;
            generateButton.disabled = false;
            setHidden(loading, true);
        }
    });
})();
