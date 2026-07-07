(() => {
    const form = document.getElementById('word-converter-form');
    if (!form) {
        return;
    }

    const elements = {
        wordFile: document.getElementById('id_word_file'),
        scheduleFile: document.getElementById('id_schedule_file'),
        wordFileError: document.getElementById('word-file-error'),
        scheduleFileError: document.getElementById('schedule-file-error'),
        error: document.getElementById('word-converter-error'),
        success: document.getElementById('word-converter-success'),
        preview: document.getElementById('word-match-preview'),
        summary: document.getElementById('word-match-summary'),
        tableBody: document.getElementById('word-match-table-body'),
        previewButton: document.getElementById('word-preview-button'),
        generateButton: document.getElementById('word-generate-button'),
        loading: document.getElementById('word-converter-loading'),
        loadingText: document.getElementById('word-converter-loading-text'),
    };
    const state = { wordFileB64: '', scheduleOptions: [], rows: [] };
    let busy = false;

    function csrfToken() {
        return form.querySelector('[name="csrfmiddlewaretoken"]')?.value || '';
    }

    function setHidden(element, hidden) {
        element.classList.toggle('hidden', hidden);
        if (element === elements.loading) {
            element.classList.toggle('flex', !hidden);
        }
    }

    function showMessage(element, message) {
        element.textContent = message;
        setHidden(element, false);
    }

    function clearMessages() {
        elements.error.textContent = '';
        elements.success.textContent = '';
        setHidden(elements.error, true);
        setHidden(elements.success, true);
    }

    function setBusy(value, message) {
        busy = value;
        elements.previewButton.disabled = value;
        elements.generateButton.disabled = value;
        if (message) {
            elements.loadingText.textContent = message;
        }
        setHidden(elements.loading, !value);
    }

    function setFieldError(control, errorElement, message) {
        errorElement.textContent = message;
        setHidden(errorElement, !message);
        control.classList.toggle('file-input-error', Boolean(message));
        control.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function resetPreview() {
        state.wordFileB64 = '';
        state.scheduleOptions = [];
        state.rows = [];
        elements.tableBody.replaceChildren();
        setHidden(elements.preview, true);
        clearMessages();
    }

    function compactOptionLabel(title, maximumLength = 42) {
        return title.length > maximumLength
            ? `${title.slice(0, maximumLength - 1).trimEnd()}…`
            : title;
    }

    function selectedOption(row) {
        return state.scheduleOptions.find((option) => option.row_index === row.selected_row_index);
    }

    function appendDates(container, dates, emptyText) {
        container.replaceChildren();
        const values = (dates || []).filter(Boolean);
        if (!values.length) {
            const empty = document.createElement('span');
            empty.className = 'text-muted';
            empty.textContent = emptyText;
            container.appendChild(empty);
            return;
        }
        values.forEach((value) => {
            const line = document.createElement('div');
            line.className = 'whitespace-nowrap';
            line.textContent = value;
            container.appendChild(line);
        });
    }

    function updateSummary() {
        const selected = state.rows.filter((row) => row.selected_row_index !== null).length;
        elements.summary.textContent = `${selected} rânduri vor fi completate. ${state.rows.length - selected} rânduri vor rămâne neschimbate.`;
    }

    function updateRow(row, tableRow, statusCell, datesCell, select) {
        const option = selectedOption(row);
        const selected = Boolean(option);
        statusCell.textContent = selected ? 'Selectat' : 'Neschimbat';
        statusCell.className = selected ? 'font-semibold text-success' : 'text-muted';
        select.title = option ? option.title : 'Lasă rândul neschimbat';
        tableRow.classList.toggle('bg-warning/10', !selected);
        appendDates(datesCell, option?.dates, selected ? 'Fără perioade' : 'Neschimbat');
        updateSummary();
    }

    function renderPreview(payload) {
        state.wordFileB64 = payload.word_file_b64;
        state.scheduleOptions = payload.schedule_options || [];
        state.rows = payload.rows || [];
        elements.tableBody.replaceChildren();

        state.rows.forEach((row) => {
            const tableRow = document.createElement('tr');
            const titleCell = document.createElement('th');
            titleCell.scope = 'row';
            titleCell.className = 'ops-word-match-course break-words whitespace-normal font-medium';
            titleCell.textContent = row.word_title;

            const statusCell = document.createElement('td');
            statusCell.className = 'align-top';
            const selectCell = document.createElement('td');
            selectCell.className = 'min-w-0 align-middle';
            const selectClip = document.createElement('div');
            selectClip.className = 'ops-word-select-clip w-full min-w-0 max-w-full';
            const select = document.createElement('select');
            select.className = 'select select-sm w-full min-w-0 max-w-full bg-base-100';
            select.setAttribute('aria-label', `Selectează programul pentru ${row.word_title}`);
            const unchanged = document.createElement('option');
            unchanged.value = '';
            unchanged.textContent = 'Lasă rândul neschimbat';
            select.appendChild(unchanged);
            state.scheduleOptions.forEach((option) => {
                const optionElement = document.createElement('option');
                optionElement.value = String(option.row_index);
                optionElement.textContent = compactOptionLabel(option.title);
                optionElement.title = option.title;
                optionElement.selected = option.row_index === row.selected_row_index;
                select.appendChild(optionElement);
            });
            selectClip.appendChild(select);
            selectCell.appendChild(selectClip);

            const candidateCell = document.createElement('td');
            const candidateList = document.createElement('div');
            candidateList.className = 'grid min-w-0 gap-1.5';
            (row.candidates || []).forEach((candidate) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'btn btn-outline btn-primary btn-xs h-auto min-h-7 w-full min-w-0 max-w-full justify-between gap-2 overflow-hidden whitespace-normal py-1 text-left';
                button.dataset.rowIndex = String(candidate.row_index);
                const candidateTitle = document.createElement('span');
                candidateTitle.className = 'min-w-0 flex-1 break-words text-left';
                candidateTitle.textContent = candidate.title;
                button.appendChild(candidateTitle);
                const score = document.createElement('span');
                score.className = 'badge badge-sm badge-neutral shrink-0';
                score.textContent = String(candidate.score);
                button.appendChild(score);
                button.addEventListener('click', () => {
                    select.value = button.dataset.rowIndex;
                    select.dispatchEvent(new Event('change'));
                });
                candidateList.appendChild(button);
            });
            if (!candidateList.childElementCount) {
                candidateList.textContent = 'Nu există sugestii';
                candidateList.classList.add('text-muted');
            }
            candidateCell.appendChild(candidateList);

            const datesCell = document.createElement('td');
            datesCell.className = 'ops-word-match-periods break-words';
            tableRow.append(titleCell, statusCell, selectCell, candidateCell, datesCell);
            select.addEventListener('change', () => {
                row.selected_row_index = select.value === '' ? null : Number(select.value);
                updateRow(row, tableRow, statusCell, datesCell, select);
            });
            elements.tableBody.appendChild(tableRow);
            updateRow(row, tableRow, statusCell, datesCell, select);
        });

        setHidden(elements.preview, false);
        elements.preview.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    async function jsonResponse(response) {
        const contentType = response.headers.get('Content-Type') || '';
        if (!contentType.includes('application/json')) {
            throw new Error('Serverul a returnat un răspuns neașteptat.');
        }
        return response.json();
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (busy) {
            return;
        }
        clearMessages();
        setFieldError(elements.wordFile, elements.wordFileError, '');
        setFieldError(elements.scheduleFile, elements.scheduleFileError, '');
        if (!elements.wordFile.files.length) {
            setFieldError(elements.wordFile, elements.wordFileError, 'Selectați un document DOCX.');
            showMessage(elements.error, 'Documentul Word este obligatoriu.');
            return;
        }
        if (!elements.scheduleFile.files.length) {
            setFieldError(elements.scheduleFile, elements.scheduleFileError, 'Selectați un program CSV sau XLSX.');
            showMessage(elements.error, 'Programul generat este obligatoriu.');
            return;
        }

        setBusy(true, 'Se analizează documentele…');
        try {
            const response = await fetch(form.dataset.previewUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken() },
                body: new FormData(form),
            });
            const payload = await jsonResponse(response);
            if (!response.ok || !payload.success) {
                throw new Error(payload.error || 'Previzualizarea nu a putut fi creată.');
            }
            renderPreview(payload);
        } catch (error) {
            showMessage(elements.error, error.message || 'Previzualizarea nu a putut fi creată.');
        } finally {
            setBusy(false);
        }
    });

    elements.generateButton.addEventListener('click', async () => {
        if (busy || !state.wordFileB64) {
            return;
        }
        clearMessages();
        setBusy(true, 'Se generează documentul Word…');
        try {
            const matches = state.rows
                .filter((row) => row.selected_row_index !== null)
                .map((row) => ({
                    word_row_index: row.word_row_index,
                    schedule_row_index: row.selected_row_index,
                }));
            const response = await fetch(form.dataset.generateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken(),
                },
                body: JSON.stringify({
                    word_file_b64: state.wordFileB64,
                    schedule_options: state.scheduleOptions,
                    matches,
                }),
            });
            if (!response.ok) {
                const payload = await jsonResponse(response);
                throw new Error(payload.error || 'Documentul Word nu a putut fi generat.');
            }
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = form.dataset.downloadFilename;
            document.body.appendChild(link);
            link.click();
            link.remove();
            URL.revokeObjectURL(url);
            const matched = response.headers.get('X-Matched-Course-Rows') || '0';
            const skipped = response.headers.get('X-Skipped-Course-Rows') || '0';
            showMessage(elements.success, `Documentul a fost generat. Rânduri completate: ${matched}. Rânduri neschimbate: ${skipped}.`);
        } catch (error) {
            showMessage(elements.error, error.message || 'Documentul Word nu a putut fi generat.');
        } finally {
            setBusy(false);
        }
    });

    elements.wordFile.addEventListener('change', () => {
        resetPreview();
    });
    elements.scheduleFile.addEventListener('change', () => {
        resetPreview();
    });
})();
