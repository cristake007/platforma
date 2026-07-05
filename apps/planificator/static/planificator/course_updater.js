(() => {
    const form = document.getElementById('course-updater-form');
    if (!form) {
        return;
    }

    const fileInput = document.getElementById('id_input_file');
    const fileSelect = document.getElementById('course-file-select');
    const fileName = document.getElementById('course-file-name');
    const fileError = document.getElementById('course-file-error');
    const previewButton = document.getElementById('course-preview-button');
    const errorAlert = document.getElementById('course-updater-error');
    const successAlert = document.getElementById('course-updater-success');
    const previewContainer = document.getElementById('course-preview-container');
    const previewCount = document.getElementById('course-preview-count');
    const table = document.getElementById('course-preview-table');
    const tableBody = document.getElementById('course-preview-table-body');
    const tableScroll = document.getElementById('course-preview-table-scroll');
    const topScroll = document.getElementById('course-preview-top-scroll');
    const topScrollInner = document.getElementById('course-preview-top-scroll-inner');
    const baseUrlInput = document.getElementById('wp-base-url');
    const usernameInput = document.getElementById('wp-username');
    const passwordInput = document.getElementById('wp-app-password');
    const connectButton = document.getElementById('wp-connect-button');
    const disconnectButton = document.getElementById('wp-disconnect-button');
    const connectionStatus = document.getElementById('wp-connection-status');

    let connected = false;
    let previewRows = [];
    let busy = false;

    function setHidden(element, hidden) {
        element.classList.toggle('hidden', hidden);
    }

    function clearMessages() {
        errorAlert.textContent = '';
        successAlert.textContent = '';
        setHidden(errorAlert, true);
        setHidden(successAlert, true);
    }

    function showError(message) {
        errorAlert.textContent = message;
        setHidden(errorAlert, false);
    }

    function showSuccess(message) {
        successAlert.textContent = message;
        setHidden(successAlert, false);
    }

    function setFileError(message) {
        fileError.textContent = message;
        setHidden(fileError, !message);
        fileInput.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function csrfToken() {
        return form.querySelector('[name="csrfmiddlewaretoken"]')?.value || '';
    }

    function credentials() {
        return {
            wp_base_url: baseUrlInput.value.trim(),
            wp_username: usernameInput.value.trim(),
            wp_app_password: passwordInput.value.trim(),
        };
    }

    async function jsonRequest(url, payload) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken(),
            },
            body: JSON.stringify(payload),
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Cererea nu a putut fi finalizată.');
        }
        return data;
    }

    function setConnectionState(isConnected, message = '') {
        connected = isConnected;
        connectButton.disabled = false;
        setHidden(connectButton, isConnected);
        setHidden(disconnectButton, !isConnected);
        connectionStatus.textContent = message || (isConnected ? 'Conectat' : 'Neconectat');
        connectionStatus.removeAttribute('title');
        connectionStatus.className = isConnected
            ? 'badge badge-outline badge-sm whitespace-nowrap border-success/40 bg-success/5 text-success'
            : 'badge badge-outline badge-sm whitespace-nowrap';
        if (previewRows.length) {
            renderRows();
        }
    }

    function setConnectionError(message) {
        connected = false;
        connectButton.disabled = false;
        setHidden(connectButton, false);
        setHidden(disconnectButton, true);
        connectionStatus.textContent = 'Conectarea a eșuat';
        connectionStatus.title = message || 'Conectarea a eșuat';
        connectionStatus.className = 'badge badge-outline badge-sm whitespace-nowrap border-error/40 bg-error/5 text-error';
        if (previewRows.length) {
            renderRows();
        }
    }

    function appendDateList(container, values, variant = 'neutral') {
        container.replaceChildren();
        if (!values?.length) {
            const empty = document.createElement('span');
            empty.className = 'text-xs text-muted';
            empty.textContent = '—';
            container.appendChild(empty);
            return;
        }
        const list = document.createElement('div');
        list.className = 'grid grid-cols-2 items-start gap-x-1 gap-y-0.5';
        values.forEach((value) => {
            const item = document.createElement('span');
            item.className = variant === 'primary'
                ? 'whitespace-nowrap rounded-field bg-primary/10 px-1 py-0 text-[11px] font-medium leading-4 text-primary'
                : 'whitespace-nowrap rounded-field bg-base-200 px-1 py-0 text-[11px] leading-4 text-base-content';
            item.textContent = value;
            list.appendChild(item);
        });
        container.appendChild(list);
    }

    function wpRequired() {
        const text = document.createElement('span');
        text.className = 'text-xs leading-5 text-muted';
        text.textContent = 'Necesită conexiune WordPress.';
        return text;
    }

    function actionButton(action, label, icon, style = 'outline') {
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset.action = action;
        button.className = style === 'primary'
            ? 'btn btn-primary btn-xs'
            : 'btn btn-outline btn-xs';
        if (icon) {
            const iconElement = document.createElement('i');
            iconElement.className = `bi ${icon}`;
            iconElement.setAttribute('aria-hidden', 'true');
            button.appendChild(iconElement);
        }
        button.append(label);
        return button;
    }

    function renderCourseCell(cell, row) {
        const title = document.createElement('p');
        title.className = 'font-semibold leading-5 text-base-content';
        title.textContent = row.title || 'Curs fără titlu';
        cell.appendChild(title);
        if (row.slug) {
            const slug = document.createElement('code');
            slug.className = 'mt-1 block text-[11px] text-muted';
            slug.textContent = row.slug;
            cell.appendChild(slug);
        }
        const postId = document.createElement('span');
        postId.className = 'mt-1 block text-[11px] text-muted';
        postId.textContent = `Post ID: ${row.post_id || '—'}`;
        cell.appendChild(postId);
        if (row.permalink) {
            const link = document.createElement('a');
            link.className = 'link link-primary mt-1 block truncate text-xs';
            link.textContent = row.permalink;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            try {
                const parsed = new URL(row.permalink);
                if (['http:', 'https:'].includes(parsed.protocol)) {
                    link.href = parsed.href;
                }
            } catch (_error) {
                link.removeAttribute('href');
            }
            cell.appendChild(link);
        }
    }

    function renderStatus(cell, row) {
        const status = document.createElement('span');
        const hasError = Boolean(row.error) || String(row.status || '').startsWith('error:');
        const succeeded = ['success', 'no changes', 'date preluate'].includes(row.status);
        status.className = hasError
            ? 'badge badge-outline badge-sm h-auto min-h-5 whitespace-normal border-error/40 bg-error/5 py-1 text-left text-error'
            : succeeded
                ? 'badge badge-outline badge-sm h-auto min-h-5 whitespace-normal border-success/40 bg-success/5 py-1 text-left text-success'
                : 'badge badge-outline badge-sm h-auto min-h-5 whitespace-normal py-1 text-left';
        status.textContent = row.error ? `eroare: ${row.error}` : (row.status || 'pregătit');
        cell.appendChild(status);
    }

    function renderRows() {
        tableBody.replaceChildren();
        previewRows.forEach((row, index) => {
            const tr = document.createElement('tr');
            tr.dataset.index = String(index);

            const courseCell = document.createElement('td');
            renderCourseCell(courseCell, row);

            const excelDatesCell = document.createElement('td');
            appendDateList(excelDatesCell, row.excel_dates, 'primary');

            const currentDatesCell = document.createElement('td');
            if (connected && row.current_dates_loaded) {
                appendDateList(currentDatesCell, row.existing_valid_dates);
            } else {
                currentDatesCell.appendChild(wpRequired());
            }

            const finalDatesCell = document.createElement('td');
            appendDateList(finalDatesCell, row.final_dates, 'primary');
            const details = document.createElement('details');
            details.className = 'mt-1 text-xs';
            const summary = document.createElement('summary');
            summary.className = 'cursor-pointer text-primary';
            summary.textContent = 'Payload';
            const payload = document.createElement('pre');
            payload.className = 'mt-1 max-h-40 overflow-auto rounded-field bg-base-200 p-2 text-[10px] leading-4';
            payload.textContent = JSON.stringify(row.payload, null, 2);
            details.append(summary, payload);
            finalDatesCell.appendChild(details);

            const statusCell = document.createElement('td');
            renderStatus(statusCell, row);

            const actionCell = document.createElement('td');
            if (!connected) {
                actionCell.appendChild(wpRequired());
            } else {
                const actions = document.createElement('div');
                actions.className = 'flex flex-wrap gap-1.5';
                const fetchDates = actionButton('fetch', 'Preia datele', 'bi-download');
                fetchDates.disabled = !(row.slug || row.permalink);
                const update = actionButton('update', 'Actualizează', 'bi-pencil', 'primary');
                update.disabled = !row.can_update || row.status === 'success' || row.status === 'no changes';
                actions.append(fetchDates, update);
                actionCell.appendChild(actions);
            }

            tr.append(
                courseCell,
                excelDatesCell,
                currentDatesCell,
                finalDatesCell,
                statusCell,
                actionCell,
            );
            tableBody.appendChild(tr);
        });
        previewCount.textContent = `${previewRows.length} ${previewRows.length === 1 ? 'rând' : 'rânduri'}`;
        setHidden(previewContainer, false);
        requestAnimationFrame(updateTopScrollWidth);
    }

    function updateTopScrollWidth() {
        topScrollInner.style.width = `${table.scrollWidth}px`;
    }

    let syncingScroll = false;
    topScroll.addEventListener('scroll', () => {
        if (syncingScroll) return;
        syncingScroll = true;
        tableScroll.scrollLeft = topScroll.scrollLeft;
        syncingScroll = false;
    });
    tableScroll.addEventListener('scroll', () => {
        if (syncingScroll) return;
        syncingScroll = true;
        topScroll.scrollLeft = tableScroll.scrollLeft;
        syncingScroll = false;
    });
    window.addEventListener('resize', updateTopScrollWidth);

    fileSelect.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => {
        const selected = fileInput.files[0];
        fileName.textContent = selected?.name || 'Niciun fișier selectat';
        fileName.classList.toggle('text-muted', !selected);
        setFileError('');
        clearMessages();
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (busy) return;
        if (!fileInput.files.length) {
            setFileError('Selectează un fișier CSV sau XLSX.');
            return;
        }
        busy = true;
        previewButton.disabled = true;
        clearMessages();
        setFileError('');
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Previzualizarea nu a putut fi construită.');
            }
            previewRows = data.rows || [];
            renderRows();
            showSuccess('Previzualizarea a fost construită. Verifică fiecare rând înainte de actualizare.');
        } catch (error) {
            showError(error.message);
        } finally {
            busy = false;
            previewButton.disabled = false;
        }
    });

    connectButton.addEventListener('click', async () => {
        connectButton.disabled = true;
        clearMessages();
        connectionStatus.textContent = 'Se conectează…';
        connectionStatus.className = 'badge badge-ghost badge-sm whitespace-nowrap';
        try {
            const data = await jsonRequest(form.dataset.connectUrl, credentials());
            const name = data.user?.name ? `Conectat ca ${data.user.name}` : 'Conectat';
            setConnectionState(true, name);
            showSuccess('Conexiunea WordPress a fost verificată.');
        } catch (error) {
            setConnectionError(error.message);
            showError(error.message);
        }
    });

    disconnectButton.addEventListener('click', () => {
        passwordInput.value = '';
        clearMessages();
        setConnectionState(false, 'Deconectat');
    });

    [baseUrlInput, usernameInput, passwordInput].forEach((input) => {
        input.addEventListener('input', () => {
            if (connected) {
                setConnectionState(false, 'Date modificate. Reconectează.');
            }
        });
    });

    tableBody.addEventListener('click', async (event) => {
        const button = event.target.closest('button[data-action]');
        if (!button || button.disabled) return;
        const tr = button.closest('tr[data-index]');
        const row = previewRows[Number(tr.dataset.index)];
        if (!row) return;

        button.disabled = true;
        clearMessages();
        const common = {
            ...credentials(),
            post_id: row.post_id,
            permalink: row.permalink,
            slug: row.slug,
        };
        try {
            if (button.dataset.action === 'fetch') {
                row.status = 'se preiau datele…';
                renderRows();
                const data = await jsonRequest(form.dataset.fetchDatesUrl, {
                    ...common,
                    excel_dates: row.excel_dates || [],
                });
                row.post_id = data.post_id;
                row.existing_valid_dates = data.existing_valid_dates || [];
                row.final_dates = data.final_dates || [];
                row.payload = data.payload || row.payload;
                row.can_update = Boolean(data.can_update);
                row.current_dates_loaded = true;
                row.status = 'date preluate';
            } else if (button.dataset.action === 'update') {
                row.status = 'se actualizează…';
                renderRows();
                const data = await jsonRequest(form.dataset.updateUrl, {
                    ...common,
                    final_dates: row.final_dates || [],
                });
                row.post_id = data.post_id;
                row.final_dates = data.final_dates || row.final_dates;
                row.status = data.status || 'success';
                showSuccess(data.updated ? `Cursul "${row.title}" a fost actualizat.` : `Cursul "${row.title}" nu necesită modificări.`);
            }
            row.error = null;
        } catch (error) {
            row.status = `error: ${error.message}`;
            row.error = null;
            showError(error.message);
        } finally {
            renderRows();
        }
    });

    setConnectionState(false);
})();
