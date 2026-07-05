# apps/diplome/static/diplome/template_editor.js

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/static/diplome/template_editor.js`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `static`
- Size: 75315 bytes
- Source SHA-256: `a170cb3fc8f8ac8bc23cb07601bbec000825b89891b775f41d5a23fef5ab6629`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(function () {
    "use strict";

    const root = document.getElementById("diploma-editor");
    if (!root || !window.DiplomaRenderer) return;
    const { mmToPx, pxToMm, pagePixelSize } = window.DiplomaRenderer;

    const layoutNode = document.getElementById("diploma-layout-data");
    const assetsNode = document.getElementById("diploma-media-assets-data");
    const canvas = document.getElementById("diploma-canvas");
    const stage = document.getElementById("editor-stage");
    const shell = document.getElementById("editor-canvas-shell");
    const viewport = document.getElementById("editor-canvas-viewport");
    const layersNode = document.getElementById("editor-layers");
    const propertiesNode = document.getElementById("editor-properties");
    const emptyPropertiesNode = document.getElementById("editor-empty-properties");
    const multiPropertiesNode = document.getElementById("editor-multi-properties");
    const topRuler = document.getElementById("editor-ruler-top");
    const leftRuler = document.getElementById("editor-ruler-left");
    const guideX = canvas.querySelector(".editor-guide-x");
    const guideY = canvas.querySelector(".editor-guide-y");
    const saveForm = document.getElementById("editor-save-form");
    const discardForm = document.getElementById("editor-discard-form");
    const mediaPicker = document.getElementById("editor-media-picker");
    const mediaPickerGrid = document.getElementById("editor-media-picker-grid");
    const mediaPickerEmpty = document.getElementById("editor-media-picker-empty");
    const mediaPickerFeedback = document.getElementById("editor-media-picker-feedback");
    const mediaPickerSelection = document.getElementById("editor-media-picker-selection");
    const mediaUploadForm = document.getElementById("editor-media-upload-form");
    const mediaUploadError = document.getElementById("editor-media-upload-error");
    const mediaPreviewNode = document.getElementById("editor-media-current-preview");
    const iconPreviewNode = document.getElementById("editor-icon-current-preview");
    const customGuidesNode = document.getElementById("editor-custom-guides");
    const guidePositionNode = document.getElementById("editor-guide-position");
    const inspectorTabs = Array.from(root.querySelectorAll("[data-inspector-tab]"));
    const inspectorPanels = Array.from(root.querySelectorAll("[data-inspector-panel]"));
    const confirmDialog = document.getElementById("editor-confirm-dialog");
    const confirmTitle = document.getElementById("editor-confirm-title");
    const confirmMessage = document.getElementById("editor-confirm-message");
    const confirmAccept = confirmDialog.querySelector("[data-confirm-accept]");
    const confirmCancel = document.getElementById("editor-confirm-cancel");
    const mediaAssets = assetsNode ? JSON.parse(assetsNode.textContent) : [];
    const mediaAssetsById = new Map(mediaAssets.map((asset) => [asset.id, asset]));
    const FITTABLE_TYPES = new Set(["text", "variable", "list", "image", "icon"]);
    const MIN_ZOOM = 0.1;
    const MAX_ZOOM = 2.5;
    const ZOOM_STEP = 0.1;
    const RULER_SIZE_PX = 27;
    let isDraftTemplate = root.dataset.isDraftTemplate === "true";

    const state = {
        layout: JSON.parse(layoutNode.textContent),
        selectedId: null,
        selectedIds: [],
        zoom: 0.75,
        zoomMode: "fit",
        gridVisible: true,
        guidesVisible: true,
        dirty: false,
        saving: false,
        leaving: false,
        revision: 0,
        history: [],
        historyIndex: 0,
        savedSnapshot: "",
    };
    state.layout.guides ??= { vertical: [], horizontal: [] };
    const pickerState = {
        mode: null,
        selectedAssetId: null,
        returnFocus: null,
    };
    state.layout.elements.forEach((element) => {
        if (["text", "variable", "list"].includes(element.type)) {
            element.style.lineHeight ??= 1.18;
            element.style.letterSpacing ??= 0;
            element.style.textTransform ??= "none";
        }
    });
    state.selectedId = state.layout.elements.find((item) => item.id === "full_name")?.id
        || state.layout.elements[0]?.id
        || null;
    state.selectedIds = state.selectedId ? [state.selectedId] : [];
    state.savedSnapshot = JSON.stringify(state.layout);
    state.history = [state.savedSnapshot];

    const VARIABLE_LABELS = {
        full_name: "Nume complet",
        date_of_birth: "Data nașterii",
        place_of_birth: "Locul nașterii",
        certificate_number: "Număr certificat",
    };

    const assetSelect = propertiesNode.querySelector('[data-prop="assetId"]');

    function assetKindLabel(asset) {
        return asset.kind === "svg" ? "SVG" : "Raster";
    }

    function assetDetails(asset) {
        const dimensions = asset.width && asset.height
            ? `${asset.width} × ${asset.height} px`
            : "Dimensiuni nespecificate";
        const size = Number.isFinite(asset.sizeBytes)
            ? `${Math.max(1, Math.round(asset.sizeBytes / 1024))} KB`
            : "";
        return [assetKindLabel(asset), dimensions, size].filter(Boolean).join(" · ");
    }

    function selectedElement() {
        return state.layout.elements.find((element) => element.id === state.selectedId) || null;
    }

    function selectedElements() {
        const ids = new Set(state.selectedIds);
        return state.layout.elements.filter((element) => ids.has(element.id));
    }

    function setSelection(ids) {
        const existing = new Set(state.layout.elements.map((element) => element.id));
        state.selectedIds = [...new Set(ids)].filter((id) => existing.has(id));
        state.selectedId = state.selectedIds.length === 1 ? state.selectedIds[0] : null;
    }

    function snap(value) {
        return Math.round(value / state.layout.page.grid_mm) * state.layout.page.grid_mm;
    }

    function clamp(value, minimum, maximum) {
        return Math.min(Math.max(value, minimum), maximum);
    }

    function setInspectorTab(tabName, { focus = false } = {}) {
        const activeTab = inspectorTabs.find((tab) => tab.dataset.inspectorTab === tabName);
        const activePanel = inspectorPanels.find((panel) => panel.dataset.inspectorPanel === tabName);
        if (!activeTab || !activePanel) return;

        inspectorTabs.forEach((tab) => {
            const isActive = tab === activeTab;
            tab.classList.toggle("is-active", isActive);
            tab.setAttribute("aria-selected", String(isActive));
            tab.tabIndex = isActive ? 0 : -1;
        });
        inspectorPanels.forEach((panel) => {
            panel.hidden = panel !== activePanel;
        });
        if (focus) activeTab.focus();
    }

    function viewportContentSize() {
        const style = window.getComputedStyle(viewport);
        const horizontalPadding = Number.parseFloat(style.paddingLeft)
            + Number.parseFloat(style.paddingRight);
        const verticalPadding = Number.parseFloat(style.paddingTop)
            + Number.parseFloat(style.paddingBottom);
        return {
            width: Math.max(1, viewport.clientWidth - horizontalPadding),
            height: Math.max(1, viewport.clientHeight - verticalPadding),
        };
    }

    function fittedPageZoom() {
        const pageSize = pagePixelSize(state.layout);
        const available = viewportContentSize();
        return clamp(Math.min(
            (available.width - RULER_SIZE_PX) / pageSize.width,
            (available.height - RULER_SIZE_PX) / pageSize.height,
            1
        ), MIN_ZOOM, MAX_ZOOM);
    }

    function syncZoomControl() {
        const control = root.querySelector('[data-action="zoom"]');
        const customOption = control.querySelector("[data-zoom-custom]");
        if (state.zoomMode === "fit") {
            customOption.hidden = true;
            control.value = "fit";
            return;
        }

        const matchingOption = Array.from(control.options).find((option) => (
            option !== customOption
            && Number.isFinite(Number.parseFloat(option.value))
            && Math.abs(Number.parseFloat(option.value) - state.zoom) < 0.001
        ));
        if (matchingOption) {
            customOption.hidden = true;
            control.value = matchingOption.value;
            return;
        }

        customOption.value = state.zoom.toFixed(2);
        customOption.textContent = `${Math.round(state.zoom * 100)}%`;
        customOption.hidden = false;
        control.value = customOption.value;
    }

    function setZoom(nextZoom, anchor = {}) {
        const previousZoom = state.zoom;
        const viewportRect = viewport.getBoundingClientRect();
        const stageRect = stage.getBoundingClientRect();
        const clientX = anchor.clientX ?? viewportRect.left + viewportRect.width / 2;
        const clientY = anchor.clientY ?? viewportRect.top + viewportRect.height / 2;
        const pageX = (clientX - stageRect.left) / previousZoom;
        const pageY = (clientY - stageRect.top) / previousZoom;

        state.zoomMode = "manual";
        state.zoom = clamp(Math.round(nextZoom * 100) / 100, MIN_ZOOM, MAX_ZOOM);
        renderCanvas();
        renderStatus();
        window.requestAnimationFrame(() => {
            const updatedStageRect = stage.getBoundingClientRect();
            viewport.scrollLeft += updatedStageRect.left + pageX * state.zoom - clientX;
            viewport.scrollTop += updatedStageRect.top + pageY * state.zoom - clientY;
        });
    }

    function changeZoom(direction, anchor = {}) {
        setZoom(state.zoom + direction * ZOOM_STEP, anchor);
    }

    function fitPage() {
        state.zoomMode = "fit";
        state.zoom = fittedPageZoom();
        renderCanvas();
        renderStatus();
        window.requestAnimationFrame(() => viewport.scrollTo({ left: 0, top: 0 }));
    }

    function refreshFittedZoom() {
        if (state.zoomMode !== "fit") return;
        const nextZoom = fittedPageZoom();
        if (Math.abs(nextZoom - state.zoom) < 0.005) return;
        state.zoom = nextZoom;
        renderCanvas();
        renderStatus();
    }

    function uniqueId(prefix) {
        return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`;
    }

    function typography(size = 24, bold = false) {
        return {
            fontFamily: "Lora",
            fontSize: size,
            bold,
            italic: false,
            underline: false,
            color: "#164194",
            align: "center",
            lineHeight: 1.18,
            letterSpacing: 0,
            textTransform: "none",
        };
    }

    function baseElement(type, label, width_mm, height_mm) {
        const page = state.layout.page;
        return {
            id: uniqueId("el"),
            type,
            label,
            x_mm: snap(Math.max(0, (page.width_mm - width_mm) / 2)),
            y_mm: snap(Math.max(0, (page.height_mm - height_mm) / 2)),
            width_mm,
            height_mm,
            rotation: 0,
            zIndex: Math.min(1000, Math.max(1, ...state.layout.elements.map((item) => item.zIndex + 1))),
            locked: false,
            visible: true,
        };
    }

    function layoutSnapshot() {
        return JSON.stringify(state.layout);
    }

    function renderHistoryControls() {
        root.querySelector('[data-action="undo"]').disabled = state.historyIndex <= 0;
        root.querySelector('[data-action="redo"]').disabled = state.historyIndex >= state.history.length - 1;
    }

    function recordHistory() {
        const snapshot = layoutSnapshot();
        if (snapshot === state.history[state.historyIndex]) return;
        state.history.splice(state.historyIndex + 1);
        state.history.push(snapshot);
        if (state.history.length > 100) state.history.shift();
        state.historyIndex = state.history.length - 1;
    }

    function updateDirtyStatus() {
        state.dirty = layoutSnapshot() !== state.savedSnapshot;
        setSaveStatus(
            state.dirty ? "dirty" : "saved",
            state.dirty ? "Modificări nesalvate" : "Modificări salvate",
        );
    }

    function markDirty() {
        recordHistory();
        state.revision += 1;
        updateDirtyStatus();
        renderHistoryControls();
    }

    function restoreHistory(offset) {
        const targetIndex = state.historyIndex + offset;
        if (targetIndex < 0 || targetIndex >= state.history.length) return;
        state.historyIndex = targetIndex;
        state.layout = JSON.parse(state.history[state.historyIndex]);
        setSelection(state.selectedIds);
        state.revision += 1;
        updateDirtyStatus();
        renderAll();
    }

    function setSaveStatus(mode, label) {
        const node = root.querySelector('[data-status="save"]');
        node.classList.remove("is-dirty", "is-saving", "is-error");
        if (mode !== "saved") node.classList.add(`is-${mode}`);
        node.querySelector("strong").textContent = label;
    }

    function renderRulers() {
        const page = state.layout.page;
        const pageSize = pagePixelSize(state.layout);
        topRuler.replaceChildren();
        leftRuler.replaceChildren();
        topRuler.style.width = `${pageSize.width * state.zoom}px`;
        leftRuler.style.height = `${pageSize.height * state.zoom}px`;
        topRuler.style.backgroundSize = `${mmToPx(page.grid_mm) * state.zoom}px 100%`;
        leftRuler.style.backgroundSize = `100% ${mmToPx(page.grid_mm) * state.zoom}px`;
        for (let value = 0; value <= page.width_mm; value += page.major_grid_mm) {
            const label = document.createElement("span");
            label.className = "editor-ruler-label";
            label.style.left = `${mmToPx(value) * state.zoom}px`;
            label.textContent = String(value);
            topRuler.appendChild(label);
        }
        for (let value = 0; value <= page.height_mm; value += page.major_grid_mm) {
            const label = document.createElement("span");
            label.className = "editor-ruler-label";
            label.style.top = `${mmToPx(value) * state.zoom}px`;
            label.textContent = String(value);
            leftRuler.appendChild(label);
        }
    }

    function renderCustomGuides() {
        canvas.querySelectorAll(".editor-guide-custom").forEach((node) => node.remove());
        const appendGuide = (orientation, position) => {
            const guide = document.createElement("div");
            guide.className = `editor-guide editor-guide-custom ${orientation === "vertical" ? "editor-guide-x" : "editor-guide-y"}`;
            guide.dataset.guideOrientation = orientation;
            guide.dataset.guidePosition = String(position);
            guide.hidden = !state.guidesVisible;
            if (orientation === "vertical") guide.style.left = `${mmToPx(position)}px`;
            else guide.style.top = `${mmToPx(position)}px`;
            canvas.appendChild(guide);
        };
        state.layout.guides.vertical.forEach((position) => appendGuide("vertical", position));
        state.layout.guides.horizontal.forEach((position) => appendGuide("horizontal", position));
    }

    function renderGuideControls() {
        customGuidesNode.replaceChildren();
        const addChip = (orientation, position) => {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = `${orientation === "vertical" ? "V" : "O"} ${position} mm ×`;
            button.title = "Elimină ghidajul";
            button.addEventListener("click", () => {
                state.layout.guides[orientation] = state.layout.guides[orientation]
                    .filter((value) => value !== position);
                markDirty();
                renderCanvas();
                renderGuideControls();
            });
            customGuidesNode.appendChild(button);
        };
        state.layout.guides.vertical.forEach((position) => addChip("vertical", position));
        state.layout.guides.horizontal.forEach((position) => addChip("horizontal", position));
    }

    function addCustomGuide(orientation) {
        const limit = orientation === "vertical"
            ? state.layout.page.width_mm
            : state.layout.page.height_mm;
        const position = clamp(Number.parseInt(guidePositionNode.value, 10) || 0, 0, limit);
        if (!state.layout.guides[orientation].includes(position)) {
            state.layout.guides[orientation].push(position);
            state.layout.guides[orientation].sort((left, right) => left - right);
            markDirty();
        }
        state.guidesVisible = true;
        const toggle = root.querySelector('[data-action="toggle-guides"]');
        toggle.classList.add("is-active");
        toggle.setAttribute("aria-pressed", "true");
        renderCanvas();
        renderGuideControls();
    }

    function renderCanvas() {
        const page = state.layout.page;
        const pageSize = pagePixelSize(state.layout);
        if (state.zoomMode === "fit") state.zoom = fittedPageZoom();
        window.DiplomaRenderer.render(canvas, state.layout, {
            editable: true,
            selectedId: state.selectedId,
            selectedIds: state.selectedIds,
            assets: mediaAssetsById,
        });
        renderCustomGuides();
        canvas.classList.toggle("has-grid", state.gridVisible);
        stage.style.transform = `scale(${state.zoom})`;
        stage.style.width = `${pageSize.width}px`;
        stage.style.height = `${pageSize.height}px`;
        shell.style.width = `${pageSize.width * state.zoom + 27}px`;
        shell.style.height = `${pageSize.height * state.zoom + 27}px`;
        renderRulers();
    }

    function fittedMediaSize(element) {
        if (element.type === "icon" && !element.assetId) {
            const size = Math.min(element.width_mm, element.height_mm);
            return { width_mm: size, height_mm: size };
        }
        const asset = mediaAssetsById.get(element.assetId);
        if (!asset?.width || !asset?.height) return null;
        if (element.type === "image" && element.style.fit !== "contain") return null;
        const ratio = asset.width / asset.height;
        if (element.width_mm / element.height_mm > ratio) {
            return {
                width_mm: Math.max(1, Math.ceil(element.height_mm * ratio)),
                height_mm: element.height_mm,
            };
        }
        return {
            width_mm: element.width_mm,
            height_mm: Math.max(1, Math.ceil(element.width_mm / ratio)),
        };
    }

    function measuredContentSize(element) {
        const elementNode = canvas.querySelector(`[data-element-id="${CSS.escape(element.id)}"]`);
        const contentNode = elementNode?.firstElementChild;
        if (!contentNode) return null;
        const originalStyle = contentNode.getAttribute("style");
        contentNode.style.width = "max-content";
        contentNode.style.height = "auto";
        contentNode.style.flex = "none";
        contentNode.style.maxWidth = "none";
        contentNode.style.maxHeight = "none";
        contentNode.style.overflow = "visible";
        const maxWidth = mmToPx(state.layout.page.width_mm - element.x_mm);
        let width = Math.min(contentNode.scrollWidth + 2, maxWidth);
        if (contentNode.scrollWidth > maxWidth) contentNode.style.width = `${maxWidth}px`;
        const height = contentNode.scrollHeight + 2;
        if (originalStyle === null) contentNode.removeAttribute("style");
        else contentNode.setAttribute("style", originalStyle);
        return {
            width_mm: Math.max(1, Math.ceil(pxToMm(width))),
            height_mm: Math.max(1, Math.ceil(pxToMm(height))),
        };
    }

    function fitElementToContent(element) {
        if (!element || element.locked || !FITTABLE_TYPES.has(element.type)) return false;
        const size = ["text", "variable", "list"].includes(element.type)
            ? measuredContentSize(element)
            : fittedMediaSize(element);
        if (!size) return false;
        const width = clamp(size.width_mm, 1, state.layout.page.width_mm - element.x_mm);
        const height = clamp(size.height_mm, 1, state.layout.page.height_mm - element.y_mm);
        if (width === element.width_mm && height === element.height_mm) return false;
        element.width_mm = width;
        element.height_mm = height;
        return true;
    }

    function fitSelectedToContent() {
        const element = selectedElement();
        if (!fitElementToContent(element)) return;
        markDirty();
        renderAll();
    }

    function iconButton(label, text, action) {
        const button = document.createElement("button");
        button.type = "button";
        button.title = label;
        button.setAttribute("aria-label", label);
        button.textContent = text;
        button.addEventListener("click", (event) => {
            event.stopPropagation();
            action();
        });
        return button;
    }

    function replaceMediaAssets(assets) {
        mediaAssets.splice(0, mediaAssets.length, ...assets);
        mediaAssetsById.clear();
        mediaAssets.forEach((asset) => mediaAssetsById.set(asset.id, asset));
    }

    function renderAssetSelect(element) {
        assetSelect.replaceChildren();
        mediaAssets.forEach((asset) => {
            const option = document.createElement("option");
            option.value = asset.id;
            option.textContent = asset.name;
            assetSelect.appendChild(option);
        });
        if (element.assetId && !mediaAssetsById.has(element.assetId)) {
            const missingOption = document.createElement("option");
            missingOption.value = element.assetId;
            missingOption.textContent = "Fișier media indisponibil";
            assetSelect.prepend(missingOption);
        }
        if (!assetSelect.options.length) {
            const emptyOption = document.createElement("option");
            emptyOption.value = "";
            emptyOption.textContent = "Niciun fișier disponibil";
            emptyOption.disabled = true;
            assetSelect.appendChild(emptyOption);
        }
        assetSelect.value = element.assetId || "";
    }

    function renderMediaPreview(element, targetNode = mediaPreviewNode) {
        targetNode.replaceChildren();
        const asset = mediaAssetsById.get(element.assetId);
        if (!asset) {
            const unavailable = document.createElement("span");
            unavailable.className = "editor-media-current-unavailable";
            unavailable.textContent = element.type === "icon"
                ? "Se folosește iconul inclus"
                : "Fișier media indisponibil";
            targetNode.appendChild(unavailable);
            return;
        }
        const image = document.createElement("img");
        image.src = asset.url;
        image.alt = element.alt || asset.name;
        const details = document.createElement("span");
        const name = document.createElement("strong");
        const metadata = document.createElement("small");
        name.textContent = asset.name;
        metadata.textContent = assetDetails(asset);
        details.append(name, metadata);
        targetNode.append(image, details);
    }

    function setPickerFeedback(message = "", mode = "status") {
        mediaPickerFeedback.hidden = !message;
        mediaPickerFeedback.textContent = message;
        mediaPickerFeedback.classList.toggle("is-error", mode === "error");
    }

    function renderMediaPicker() {
        mediaPickerGrid.replaceChildren();
        mediaPickerEmpty.hidden = mediaAssets.length > 0;
        mediaAssets.forEach((asset) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "editor-media-card";
            button.dataset.assetId = asset.id;
            button.setAttribute("role", "option");
            const selected = pickerState.selectedAssetId === asset.id;
            button.classList.toggle("is-selected", selected);
            button.setAttribute("aria-selected", String(selected));

            const preview = document.createElement("span");
            preview.className = "editor-media-card-preview";
            const image = document.createElement("img");
            image.src = asset.url;
            image.alt = "";
            image.loading = "lazy";
            preview.appendChild(image);

            const copy = document.createElement("span");
            copy.className = "editor-media-card-copy";
            const name = document.createElement("strong");
            const metadata = document.createElement("small");
            name.textContent = asset.name;
            metadata.textContent = assetDetails(asset);
            copy.append(name, metadata);
            button.append(preview, copy);
            button.addEventListener("click", () => {
                pickerState.selectedAssetId = asset.id;
                renderMediaPicker();
                mediaPickerGrid.querySelector(`[data-asset-id="${asset.id}"]`)?.focus();
            });
            mediaPickerGrid.appendChild(button);
        });

        const selectedAsset = mediaAssetsById.get(pickerState.selectedAssetId);
        mediaPickerSelection.textContent = selectedAsset
            ? `Selectat: ${selectedAsset.name}`
            : "Niciun fișier selectat";
        root.querySelector('[data-action="apply-media-asset"]').disabled = !selectedAsset;
    }

    function openMediaPicker(mode, trigger = document.activeElement) {
        const element = selectedElement();
        pickerState.mode = mode;
        pickerState.returnFocus = trigger;
        pickerState.selectedAssetId = ["replace", "replace-background", "replace-icon"].includes(mode) && mediaAssetsById.has(element?.assetId)
            ? element.assetId
            : null;
        const descriptions = {
            "create-image": "Alege fișierul pentru imaginea nouă.",
            "create-background": "Alege fișierul care va acoperi fundalul paginii.",
            replace: "Alege fișierul care va înlocui selecția curentă.",
            "replace-background": "Alege fișierul care va înlocui fundalul curent.",
            "replace-icon": "Alege sau încarcă grafica folosită de icon.",
        };
        document.getElementById("editor-media-picker-description").textContent = descriptions[mode];
        setPickerFeedback();
        mediaUploadError.hidden = true;
        mediaUploadError.textContent = "";
        renderMediaPicker();
        mediaPicker.hidden = false;
        window.requestAnimationFrame(() => {
            const selectedCard = mediaPickerGrid.querySelector(".is-selected");
            (selectedCard || mediaPickerGrid.querySelector("button") || mediaUploadForm.elements.file).focus();
        });
    }

    function closeMediaPicker() {
        if (mediaPicker.hidden) return;
        mediaPicker.hidden = true;
        const returnFocus = pickerState.returnFocus;
        pickerState.mode = null;
        pickerState.selectedAssetId = null;
        if (returnFocus instanceof HTMLElement) returnFocus.focus();
    }

    async function fetchMediaAssets() {
        const response = await fetch(root.dataset.mediaAssetsApiUrl, {
            headers: { "Accept": "application/json" },
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok || !Array.isArray(payload.assets)) {
            throw new Error("Biblioteca media nu a putut fi reîmprospătată.");
        }
        replaceMediaAssets(payload.assets);
    }

    async function refreshMediaAssets() {
        const refreshButton = root.querySelector('[data-action="refresh-media-assets"]');
        refreshButton.disabled = true;
        setPickerFeedback("Se reîmprospătează biblioteca…");
        try {
            await fetchMediaAssets();
            if (!mediaAssetsById.has(pickerState.selectedAssetId)) {
                pickerState.selectedAssetId = null;
            }
            setPickerFeedback("Biblioteca media a fost actualizată.");
            renderMediaPicker();
            renderProperties();
            renderCanvas();
        } catch (error) {
            setPickerFeedback(error.message, "error");
        } finally {
            refreshButton.disabled = false;
        }
    }

    function applyMediaAsset() {
        const asset = mediaAssetsById.get(pickerState.selectedAssetId);
        if (!asset) return;
        if (pickerState.mode === "create-image") {
            addElement({
                ...baseElement("image", "Imagine", 58, 37),
                style: { fit: "contain", opacity: 1 },
                assetId: asset.id,
                alt: asset.name,
            }, { fitContent: true });
        } else if (pickerState.mode === "create-background") {
            if (state.layout.elements.some((element) => element.type === "background")) {
                setPickerFeedback("Template-ul poate avea un singur fundal.", "error");
                return;
            }
            const element = baseElement(
                "background",
                "Fundal",
                state.layout.page.width_mm,
                state.layout.page.height_mm,
            );
            Object.assign(element, {
                x_mm: 0,
                y_mm: 0,
                zIndex: 0,
                locked: true,
                style: { fit: "cover", opacity: 1 },
                assetId: asset.id,
                alt: "",
            });
            addElement(element);
        } else if (["replace", "replace-background", "replace-icon"].includes(pickerState.mode)) {
            const element = selectedElement();
            const backgroundWorkflow = pickerState.mode === "replace-background" && element?.type === "background";
            const iconWorkflow = pickerState.mode === "replace-icon" && element?.type === "icon";
            if (!element || !["image", "background", "icon"].includes(element.type)
                || (element.locked && !backgroundWorkflow)
                || (pickerState.mode === "replace-icon" && !iconWorkflow)) return;
            if (element.assetId !== asset.id) {
                element.assetId = asset.id;
                if (!element.alt) element.alt = asset.name;
                markDirty();
                renderAll();
            }
        }
        closeMediaPicker();
    }

    async function removeIconAsset() {
        const element = selectedElement();
        if (!element || element.type !== "icon" || element.locked || !element.assetId) return;
        const confirmed = await requestConfirmation({
            title: "Revii la iconul inclus?",
            message: "Grafica personalizată va fi scoasă din element. Fișierul rămâne în biblioteca media.",
            acceptLabel: "Revino",
        });
        if (!confirmed) return;
        delete element.assetId;
        delete element.alt;
        markDirty();
        renderAll();
    }

    let confirmationResolver = null;

    function closeConfirmation(result) {
        if (!confirmationResolver) return;
        const resolve = confirmationResolver;
        confirmationResolver = null;
        if (confirmDialog.open) confirmDialog.close();
        resolve(result);
    }

    function requestConfirmation({
        title,
        message,
        acceptLabel = "Șterge",
        cancelLabel = "Renunță",
    }) {
        if (confirmationResolver) closeConfirmation(false);
        confirmTitle.textContent = title;
        confirmMessage.textContent = message;
        confirmAccept.textContent = acceptLabel;
        confirmCancel.textContent = cancelLabel;
        confirmDialog.showModal();
        return new Promise((resolve) => {
            confirmationResolver = resolve;
            window.requestAnimationFrame(() => confirmAccept.focus());
        });
    }

    async function removeSelectedMediaElement() {
        const element = selectedElement();
        if (!element || !["image", "background"].includes(element.type)) return;
        await deleteElements([element.id], {
            allowLockedBackground: element.type === "background",
            confirmDelete: true,
        });
    }

    async function deleteElements(
        ids = state.selectedIds,
        { allowLockedBackground = false, confirmDelete = false } = {},
    ) {
        const idSet = new Set(ids);
        const targets = state.layout.elements.filter((element) => idSet.has(element.id));
        const deletable = targets.filter(
            (element) => !element.locked || (allowLockedBackground && element.type === "background"),
        );
        if (!deletable.length) return;
        if (confirmDelete || deletable.some((element) => element.type === "background")) {
            const hasBackground = deletable.some((element) => element.type === "background");
            const confirmed = await requestConfirmation({
                title: hasBackground ? "Elimini fundalul?" : "Elimini elementul media?",
                message: "Elementul va fi eliminat din template. Fișierul original rămâne în biblioteca media.",
            });
            if (!confirmed) return;
        }
        const firstIndex = Math.min(...deletable.map((element) => state.layout.elements.indexOf(element)));
        const deletedIds = new Set(deletable.map((element) => element.id));
        state.layout.elements = state.layout.elements.filter((element) => !deletedIds.has(element.id));
        const next = state.layout.elements[Math.min(firstIndex, state.layout.elements.length - 1)];
        setSelection(next ? [next.id] : []);
        markDirty();
        renderAll();
    }

    function duplicateElements(ids = state.selectedIds) {
        const idSet = new Set(ids);
        const originals = state.layout.elements.filter(
            (element) => idSet.has(element.id) && !element.locked && element.type !== "background",
        );
        if (!originals.length) return;
        let nextZ = Math.max(0, ...state.layout.elements.map((element) => element.zIndex));
        const copies = originals.map((element) => {
            const copy = JSON.parse(JSON.stringify(element));
            copy.id = uniqueId(element.type);
            copy.label = `${element.label} copie`.slice(0, 120);
            copy.x_mm = clamp(element.x_mm + 5, 0, state.layout.page.width_mm - element.width_mm);
            copy.y_mm = clamp(element.y_mm + 5, 0, state.layout.page.height_mm - element.height_mm);
            nextZ = Math.min(1000, nextZ + 1);
            copy.zIndex = nextZ;
            return copy;
        });
        state.layout.elements.push(...copies);
        setSelection(copies.map((element) => element.id));
        markDirty();
        renderAll();
    }

    function renderLayers() {
        layersNode.replaceChildren();
        [...state.layout.elements]
            .sort((left, right) => right.zIndex - left.zIndex)
            .forEach((element) => {
                const row = document.createElement("div");
                row.className = "editor-layer";
                row.dataset.elementId = element.id;
                row.classList.toggle("is-selected", state.selectedIds.includes(element.id));
                row.tabIndex = 0;

                const drag = document.createElement("span");
                drag.className = "editor-layer-drag";
                drag.textContent = "⠿";
                const name = document.createElement("span");
                name.className = "editor-layer-name";
                name.textContent = element.label;
                name.title = element.label;
                row.append(drag, name);
                row.appendChild(iconButton(
                    element.visible ? "Ascunde stratul" : "Afișează stratul",
                    element.visible ? "◉" : "○",
                    () => {
                        element.visible = !element.visible;
                        markDirty();
                        renderAll();
                    },
                ));
                row.appendChild(iconButton(
                    element.locked ? "Deblochează stratul" : "Blochează stratul",
                    element.locked ? "▣" : "□",
                    () => {
                        element.locked = !element.locked;
                        markDirty();
                        renderAll();
                    },
                ));
                row.appendChild(iconButton("Duplică stratul", "⧉", () => duplicateElements([element.id])));
                row.appendChild(iconButton(
                    "Șterge stratul",
                    "×",
                    () => deleteElements(
                        [element.id],
                        { allowLockedBackground: element.type === "background" },
                    ),
                ));
                row.addEventListener("click", (event) => selectElement(element.id, event));
                row.addEventListener("keydown", (event) => {
                    if (event.key === "Enter" || event.key === " ") selectElement(element.id, event);
                });
                layersNode.appendChild(row);
            });
    }

    function setFieldValue(selector, value) {
        const node = propertiesNode.querySelector(selector);
        if (!node) return;
        if (node.type === "checkbox") node.checked = Boolean(value);
        else node.value = value ?? "";
    }

    function renderProperties() {
        const element = selectedElement();
        propertiesNode.hidden = !element;
        const multiple = state.selectedIds.length > 1;
        emptyPropertiesNode.hidden = Boolean(element) || multiple;
        multiPropertiesNode.hidden = !multiple;
        multiPropertiesNode.querySelector("[data-multi-count]").textContent = `${state.selectedIds.length} elemente selectate`;
        document.getElementById("property-lock-indicator").textContent = element?.locked ? "▣" : "○";
        if (!element) return;

        ["x_mm", "y_mm", "width_mm", "height_mm", "rotation", "zIndex", "label", "text", "placeholder", "variable", "alt", "iconName"]
            .forEach((key) => setFieldValue(`[data-prop="${key}"]`, element[key]));

        const hasTypography = ["text", "variable", "list"].includes(element.type);
        propertiesNode.querySelector('[data-section="typography"]').hidden = !hasTypography;
        if (hasTypography) {
            ["fontFamily", "fontSize", "color", "align", "lineHeight", "letterSpacing", "textTransform"].forEach((key) => {
                setFieldValue(`[data-style="${key}"]`, element.style[key]);
            });
            propertiesNode.querySelectorAll("[data-style-toggle]").forEach((button) => {
                button.setAttribute("aria-pressed", String(Boolean(element.style[button.dataset.styleToggle])));
            });
        }
        const hasList = element.type === "list";
        propertiesNode.querySelector('[data-section="list"]').hidden = !hasList;
        if (hasList) {
            ["listType", "indent_mm"].forEach((key) => {
                setFieldValue(`[data-style="${key}"]`, element.style[key]);
            });
            propertiesNode.querySelector("[data-list-items]").value = element.items.join("\n");
        }
        const hasMedia = element.type === "image" || element.type === "background";
        propertiesNode.querySelector('[data-section="media"]').hidden = !hasMedia;
        if (hasMedia) {
            renderAssetSelect(element);
            renderMediaPreview(element);
            ["fit", "opacity"].forEach((key) => {
                setFieldValue(`[data-style="${key}"]`, element.style[key]);
            });
        }
        const hasIcon = element.type === "icon";
        propertiesNode.querySelector('[data-section="icon"]').hidden = !hasIcon;
        if (hasIcon) {
            renderMediaPreview(element, iconPreviewNode);
            ["color", "opacity"].forEach((key) => {
                setFieldValue(`[data-icon-style="${key}"]`, element.style[key]);
            });
            propertiesNode.querySelector('[data-action="remove-icon-asset"]').disabled = !element.assetId;
        }
        const hasTable = element.type === "table";
        propertiesNode.querySelector('[data-section="table"]').hidden = !hasTable;
        if (hasTable) {
            propertiesNode.querySelector("[data-table-columns]").value = element.columns.join("\n");
            propertiesNode.querySelector("[data-table-rows]").value = element.rows
                .map((row) => row.join(" | "))
                .join("\n");
            ["fontFamily", "fontSize", "bold", "color", "align", "borderColor", "headerBackground"]
                .forEach((key) => setFieldValue(`[data-table-style="${key}"]`, element.style[key]));
        }
        propertiesNode.querySelector('[data-content-field="text"]').hidden = element.type !== "text";
        propertiesNode.querySelector('[data-content-field="placeholder"]').hidden = element.type !== "variable";
        propertiesNode.querySelector('[data-content-field="variable"]').hidden = element.type !== "variable";
        propertiesNode.querySelectorAll("input, select, textarea, button").forEach((control) => {
            control.disabled = element.locked;
        });
        if (element.type === "icon") {
            propertiesNode.querySelector('[data-action="remove-icon-asset"]').disabled = element.locked || !element.assetId;
        }
        if (element.type === "background") {
            ["x_mm", "y_mm", "width_mm", "height_mm", "rotation", "zIndex"].forEach((key) => {
                propertiesNode.querySelector(`[data-prop="${key}"]`).disabled = true;
            });
            [
                '[data-prop="assetId"]', '[data-prop="alt"]', '[data-style="fit"]',
                '[data-style="opacity"]', '[data-action="open-media-picker"]',
                '[data-action="remove-media-element"]',
            ].forEach((selector) => {
                propertiesNode.querySelector(selector).disabled = false;
            });
        }
    }

    function renderAlignmentState() {
        const unlockedCount = selectedElements().filter(
            (element) => !element.locked && element.type !== "background"
        ).length;
        root.querySelectorAll("[data-align]").forEach((button) => {
            button.disabled = unlockedCount < 1;
        });
        root.querySelectorAll("[data-distribute]").forEach((button) => {
            button.disabled = unlockedCount < 3;
        });
        const element = selectedElement();
        root.querySelector('[data-action="fit-content"]').disabled = !(
            element && !element.locked && FITTABLE_TYPES.has(element.type)
        );
    }

    function renderStatus() {
        root.querySelector('[data-status="grid"]').textContent = `${state.layout.page.grid_mm} mm / ${state.layout.page.major_grid_mm} mm`;
        root.querySelector('[data-status="zoom"]').textContent = `${Math.round(state.zoom * 100)}%`;
        root.querySelector('[data-status="page"]').textContent = `${state.layout.page.size} ${state.layout.page.orientation}`;
        syncZoomControl();
    }

    function renderAll() {
        renderCanvas();
        renderLayers();
        renderProperties();
        renderAlignmentState();
        renderStatus();
        renderHistoryControls();
        renderGuideControls();
    }

    function selectElement(elementId, event = {}) {
        if (event.shiftKey || event.ctrlKey || event.metaKey) {
            const ids = new Set(state.selectedIds);
            if (ids.has(elementId)) ids.delete(elementId);
            else ids.add(elementId);
            setSelection([...ids]);
        } else {
            setSelection([elementId]);
        }
        renderAll();
    }

    function addElement(element, { fitContent = false } = {}) {
        state.layout.elements.push(element);
        setSelection([element.id]);
        renderCanvas();
        if (fitContent && fitElementToContent(element)) {
            element.x_mm = snap(Math.max(0, (state.layout.page.width_mm - element.width_mm) / 2));
            element.y_mm = snap(Math.max(0, (state.layout.page.height_mm - element.height_mm) / 2));
        }
        markDirty();
        renderAll();
    }

    function addText() {
        addElement({
            ...baseElement("text", "Text nou", 85, 13),
            style: typography(24),
            text: "Text nou",
        }, { fitContent: true });
    }

    function addList() {
        addElement({
            ...baseElement("list", "Listă", 120, 40),
            style: {
                ...typography(14),
                fontFamily: "Inter",
                color: "#111827",
                align: "left",
                lineHeight: 1.2,
                listType: "bullet",
                indent_mm: 5,
            },
            items: ["Primul punct", "Al doilea punct"],
        }, { fitContent: true });
    }

    function addVariable(variable) {
        const label = VARIABLE_LABELS[variable];
        addElement({
            ...baseElement("variable", label, 90, 15),
            style: typography(variable === "full_name" ? 32 : 20, variable === "full_name"),
            variable,
            placeholder: label,
        }, { fitContent: true });
    }

    function addImage(trigger) {
        openMediaPicker("create-image", trigger);
    }

    function addBackground(trigger) {
        const background = state.layout.elements.find((element) => element.type === "background");
        if (background) {
            setSelection([background.id]);
            renderAll();
            openMediaPicker("replace-background", trigger);
            return;
        }
        openMediaPicker("create-background", trigger);
    }

    function addIcon() {
        addElement({
            ...baseElement("icon", "Icon", 13, 13),
            style: { color: "#164194", opacity: 1 },
            iconName: "award",
        }, { fitContent: true });
    }

    function addTable() {
        addElement({
            ...baseElement("table", "Tabel", 143, 29),
            style: {
                fontFamily: "Inter",
                fontSize: 14,
                bold: false,
                color: "#304253",
                align: "center",
                borderColor: "#164194",
                headerBackground: "#edf3f9",
            },
            columns: ["Coloana 1", "Coloana 2", "Coloana 3"],
            rows: [["Valoare", "Valoare", "Valoare"]],
        });
    }

    function moveLayer(direction) {
        const element = selectedElement();
        if (!element || element.type === "background") return;
        const sorted = state.layout.elements
            .filter((item) => item.type !== "background")
            .sort((left, right) => left.zIndex - right.zIndex);
        const index = sorted.findIndex((item) => item.id === element.id);
        const targetIndex = index + direction;
        if (targetIndex < 0 || targetIndex >= sorted.length) return;
        const target = sorted[targetIndex];
        [element.zIndex, target.zIndex] = [target.zIndex, element.zIndex];
        markDirty();
        renderAll();
    }

    function alignSelected(kind) {
        const elements = selectedElements().filter(
            (element) => !element.locked && element.type !== "background"
        );
        if (!elements.length) return;
        const alignToPage = elements.length === 1;
        const left = alignToPage
            ? 0
            : Math.min(...elements.map((element) => element.x_mm));
        const right = alignToPage
            ? state.layout.page.width_mm
            : Math.max(...elements.map((element) => element.x_mm + element.width_mm));
        const top = alignToPage
            ? 0
            : Math.min(...elements.map((element) => element.y_mm));
        const bottom = alignToPage
            ? state.layout.page.height_mm
            : Math.max(...elements.map((element) => element.y_mm + element.height_mm));
        elements.forEach((element) => {
            if (kind === "left") element.x_mm = left;
            if (kind === "center") element.x_mm = snap((left + right - element.width_mm) / 2);
            if (kind === "right") element.x_mm = right - element.width_mm;
            if (kind === "top") element.y_mm = top;
            if (kind === "middle") element.y_mm = snap((top + bottom - element.height_mm) / 2);
            if (kind === "bottom") element.y_mm = bottom - element.height_mm;
            element.x_mm = clamp(element.x_mm, 0, state.layout.page.width_mm - element.width_mm);
            element.y_mm = clamp(element.y_mm, 0, state.layout.page.height_mm - element.height_mm);
        });
        markDirty();
        renderAll();
    }

    function distributeSelected(axis) {
        const elements = selectedElements().filter(
            (element) => !element.locked && element.type !== "background"
        );
        if (elements.length < 3) return;
        const horizontal = axis === "horizontal";
        elements.sort((left, right) => horizontal ? left.x_mm - right.x_mm : left.y_mm - right.y_mm);
        const positionKey = horizontal ? "x_mm" : "y_mm";
        const sizeKey = horizontal ? "width_mm" : "height_mm";
        const first = elements[0][positionKey];
        const end = elements.at(-1)[positionKey] + elements.at(-1)[sizeKey];
        const occupied = elements.reduce((sum, element) => sum + element[sizeKey], 0);
        const gap = (end - first - occupied) / (elements.length - 1);
        let cursor = first;
        elements.forEach((element) => {
            if (element.type !== "background") element[positionKey] = snap(cursor);
            cursor += element[sizeKey] + gap;
        });
        markDirty();
        renderAll();
    }

    function hideGuides() {
        guideX.hidden = true;
        guideY.hidden = true;
    }

    function snapBoundsToPage(bounds) {
        if (!state.guidesVisible) {
            hideGuides();
            return { dx: 0, dy: 0 };
        }
        const tolerance = 1;
        const page = state.layout.page;
        const findSnap = (values, targets) => {
            let best = null;
            values.forEach((value) => targets.forEach((target) => {
                const distance = Math.abs(target - value);
                if (distance <= tolerance && (!best || distance < best.distance)) {
                    best = { adjustment: target - value, target, distance };
                }
            }));
            return best;
        };
        const xSnap = findSnap(
            [bounds.left, (bounds.left + bounds.right) / 2, bounds.right],
            [0, page.width_mm / 2, page.width_mm, ...state.layout.guides.vertical],
        );
        const ySnap = findSnap(
            [bounds.top, (bounds.top + bounds.bottom) / 2, bounds.bottom],
            [0, page.height_mm / 2, page.height_mm, ...state.layout.guides.horizontal],
        );
        guideX.hidden = !xSnap;
        guideY.hidden = !ySnap;
        if (xSnap) guideX.style.left = `${mmToPx(xSnap.target)}px`;
        if (ySnap) guideY.style.top = `${mmToPx(ySnap.target)}px`;
        return { dx: xSnap?.adjustment || 0, dy: ySnap?.adjustment || 0 };
    }

    function beginPointerInteraction(event) {
        const node = event.target.closest(".diploma-element");
        if (!node) {
            setSelection([]);
            renderAll();
            return;
        }
        const element = state.layout.elements.find((item) => item.id === node.dataset.elementId);
        if (!element) return;
        if (event.shiftKey || event.ctrlKey || event.metaKey) {
            selectElement(element.id, event);
            return;
        }
        if (!state.selectedIds.includes(element.id)) setSelection([element.id]);
        renderAll();
        if (element.locked || element.type === "background" || event.button !== 0) return;
        event.preventDefault();

        const resizing = state.selectedIds.length === 1 && Boolean(event.target.closest("[data-resize-handle]"));
        const moving = selectedElements().filter((item) => !item.locked);
        if (!moving.length) return;
        const startElements = moving.map((item) => ({
            element: item,
            x_mm: item.x_mm,
            y_mm: item.y_mm,
            width_mm: item.width_mm,
            height_mm: item.height_mm,
        }));
        const start = {
            clientX: event.clientX,
            clientY: event.clientY,
            x_mm: element.x_mm,
            y_mm: element.y_mm,
            width_mm: element.width_mm,
            height_mm: element.height_mm,
        };

        function onMove(moveEvent) {
            const dx_mm = pxToMm((moveEvent.clientX - start.clientX) / state.zoom);
            const dy_mm = pxToMm((moveEvent.clientY - start.clientY) / state.zoom);
            if (resizing) {
                element.width_mm = clamp(snap(start.width_mm + dx_mm), 1, state.layout.page.width_mm - element.x_mm);
                element.height_mm = clamp(snap(start.height_mm + dy_mm), 1, state.layout.page.height_mm - element.y_mm);
                const adjustment = snapBoundsToPage({
                    left: element.x_mm,
                    right: element.x_mm + element.width_mm,
                    top: element.y_mm,
                    bottom: element.y_mm + element.height_mm,
                });
                element.width_mm = clamp(snap(element.width_mm + adjustment.dx), 1, state.layout.page.width_mm - element.x_mm);
                element.height_mm = clamp(snap(element.height_mm + adjustment.dy), 1, state.layout.page.height_mm - element.y_mm);
            } else {
                const left = Math.min(...startElements.map((item) => item.x_mm));
                const right = Math.max(...startElements.map((item) => item.x_mm + item.width_mm));
                const top = Math.min(...startElements.map((item) => item.y_mm));
                const bottom = Math.max(...startElements.map((item) => item.y_mm + item.height_mm));
                let moveX = clamp(snap(dx_mm), -left, state.layout.page.width_mm - right);
                let moveY = clamp(snap(dy_mm), -top, state.layout.page.height_mm - bottom);
                const adjustment = snapBoundsToPage({
                    left: left + moveX,
                    right: right + moveX,
                    top: top + moveY,
                    bottom: bottom + moveY,
                });
                moveX = clamp(snap(moveX + adjustment.dx), -left, state.layout.page.width_mm - right);
                moveY = clamp(snap(moveY + adjustment.dy), -top, state.layout.page.height_mm - bottom);
                startElements.forEach((item) => {
                    item.element.x_mm = item.x_mm + moveX;
                    item.element.y_mm = item.y_mm + moveY;
                });
            }
            renderCanvas();
            renderProperties();
        }

        function onUp() {
            document.removeEventListener("pointermove", onMove);
            document.removeEventListener("pointerup", onUp);
            hideGuides();
            markDirty();
            renderAll();
        }

        document.addEventListener("pointermove", onMove);
        document.addEventListener("pointerup", onUp, { once: true });
    }

    function updateProperty(control) {
        const element = selectedElement();
        const key = control.dataset.prop;
        const backgroundMediaChange = element?.type === "background" && ["assetId", "alt"].includes(key);
        if (!element || (element.locked && !backgroundMediaChange)) return;
        let value = control.value;
        if (key === "assetId" && !mediaAssetsById.has(value)) return;
        if (["x_mm", "y_mm", "width_mm", "height_mm", "rotation", "zIndex"].includes(key)) {
            value = Number.parseInt(value, 10);
            if (!Number.isFinite(value)) return;
            if (["x_mm", "y_mm", "width_mm", "height_mm"].includes(key)) value = snap(value);
        }
        if (key === "width_mm") value = clamp(value, 1, state.layout.page.width_mm - element.x_mm);
        if (key === "height_mm") value = clamp(value, 1, state.layout.page.height_mm - element.y_mm);
        if (key === "x_mm") value = clamp(value, 0, state.layout.page.width_mm - element.width_mm);
        if (key === "y_mm") value = clamp(value, 0, state.layout.page.height_mm - element.height_mm);
        if (key === "rotation") value = clamp(value, -180, 180);
        if (key === "zIndex") value = clamp(value, element.type === "background" ? 0 : 1, 1000);
        element[key] = value;
        if (key === "assetId" && !element.alt) {
            element.alt = mediaAssetsById.get(value)?.name || "";
        }
        markDirty();
        renderCanvas();
        renderLayers();
    }

    function updateStyle(control) {
        const element = selectedElement();
        const key = control.dataset.style;
        const backgroundStyleChange = element?.type === "background" && ["fit", "opacity"].includes(key);
        if (!element || (element.locked && !backgroundStyleChange)) return;
        let value = control.value;
        if (key === "fontSize") value = clamp(Number.parseInt(value, 10) || 8, 8, 200);
        if (key === "opacity") value = clamp(Number.parseFloat(value) || 0, 0, 1);
        if (key === "lineHeight") value = clamp(Number.parseFloat(value) || 0.8, 0.8, 3);
        if (key === "letterSpacing") value = clamp(Number.parseFloat(value) || 0, -5, 20);
        if (key === "indent_mm") value = clamp(Number.parseFloat(value) || 0, 0, 50);
        element.style[key] = value;
        markDirty();
        renderCanvas();
    }

    function updateIconStyle(control) {
        const element = selectedElement();
        if (!element || element.type !== "icon" || element.locked) return;
        const key = control.dataset.iconStyle;
        let value = control.value;
        if (key === "opacity") value = clamp(Number.parseFloat(value) || 0, 0, 1);
        element.style[key] = value;
        markDirty();
        renderCanvas();
    }

    function updateTableStyle(control) {
        const element = selectedElement();
        if (!element || element.type !== "table" || element.locked) return;
        const key = control.dataset.tableStyle;
        let value = control.type === "checkbox" ? control.checked : control.value;
        if (key === "fontSize") value = clamp(Number.parseInt(value, 10) || 8, 8, 72);
        element.style[key] = value;
        markDirty();
        renderCanvas();
    }

    function updateTableColumns(control) {
        const element = selectedElement();
        if (!element || element.type !== "table" || element.locked) return;
        const columns = control.value.split(/\r?\n/)
            .map((value) => value.trim())
            .filter(Boolean)
            .slice(0, 8);
        if (!columns.length) return;
        element.columns = columns;
        element.rows = element.rows.map((row) => [
            ...row.slice(0, columns.length),
            ...Array(Math.max(0, columns.length - row.length)).fill(""),
        ]);
        markDirty();
        renderCanvas();
    }

    function updateTableRows(control) {
        const element = selectedElement();
        if (!element || element.type !== "table" || element.locked) return;
        element.rows = control.value.split(/\r?\n/)
            .filter((line) => line.trim())
            .slice(0, 20)
            .map((line) => {
                const cells = line.split("|").map((value) => value.trim());
                return [
                    ...cells.slice(0, element.columns.length),
                    ...Array(Math.max(0, element.columns.length - cells.length)).fill(""),
                ];
            });
        markDirty();
        renderCanvas();
    }

    async function saveLayout() {
        if (state.saving) return false;
        state.saving = true;
        setSaveStatus("saving", "Se salvează…");
        const savedRevision = state.revision;
        const submittedSnapshot = layoutSnapshot();
        const formData = new FormData(saveForm);
        formData.append("layout_json", JSON.stringify(state.layout));
        try {
            const response = await fetch(root.dataset.saveUrl, {
                method: "POST",
                body: formData,
                headers: { "X-Requested-With": "XMLHttpRequest" },
            });
            const payload = await response.json();
            if (!response.ok || !payload.success) {
                const message = payload.errors?.layout_json?.[0]?.message || "Template-ul nu a putut fi salvat.";
                throw new Error(message);
            }
            isDraftTemplate = Boolean(payload.isDraft);
            state.savedSnapshot = submittedSnapshot;
            if (state.revision !== savedRevision) {
                updateDirtyStatus();
                setSaveStatus("dirty", "Există modificări noi nesalvate");
                return false;
            }
            updateDirtyStatus();
            return true;
        } catch (error) {
            setSaveStatus("error", error.message || "Eroare la salvare");
            return false;
        } finally {
            state.saving = false;
        }
    }

    async function openPreview(event) {
        event.preventDefault();
        const previewLink = event.currentTarget;
        if (state.dirty && !(await saveLayout())) return;
        window.location.href = previewLink.href;
    }

    async function confirmDiscardChanges() {
        if (!state.dirty) return true;
        return requestConfirmation({
            title: "Modificări nesalvate",
            message: "Ai modificări nesalvate. Dacă ieși acum, acestea vor fi pierdute.",
            acceptLabel: "Ieși fără salvare",
            cancelLabel: "Rămâi în editor",
        });
    }

    async function discardDraftTemplate() {
        if (!isDraftTemplate) return true;
        try {
            const response = await fetch(discardForm.action, {
                method: "POST",
                body: new FormData(discardForm),
                headers: {
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
            });
            const payload = await response.json().catch(() => ({}));
            if (!response.ok || !payload.success) {
                throw new Error("Template-ul provizoriu nu a putut fi eliminat.");
            }
            isDraftTemplate = false;
            return true;
        } catch (error) {
            setSaveStatus("error", error.message || "Template-ul provizoriu nu a putut fi eliminat.");
            return false;
        }
    }

    async function prepareToLeaveEditor() {
        if (state.leaving) return false;
        state.leaving = true;
        if (!(await confirmDiscardChanges())) {
            state.leaving = false;
            return false;
        }
        if (!(await discardDraftTemplate())) {
            state.leaving = false;
            return false;
        }
        state.dirty = false;
        return true;
    }

    async function closeEditor() {
        if (!(await prepareToLeaveEditor())) return;
        window.location.assign(root.dataset.templateListUrl);
    }

    function shouldInterceptNavigation(event, link) {
        if ((!state.dirty && !isDraftTemplate) || !link || event.defaultPrevented || event.button !== 0) return false;
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return false;
        if (link.hasAttribute("download") || (link.target && link.target !== "_self")) return false;
        if (link.dataset.action === "preview") return false;

        const destination = new URL(link.href, window.location.href);
        if (!["http:", "https:"].includes(destination.protocol)) return false;
        const current = new URL(window.location.href);
        if (
            destination.origin === current.origin
            && destination.pathname === current.pathname
            && destination.search === current.search
        ) return false;
        return true;
    }

    async function handleDocumentNavigation(event) {
        const link = event.target.closest?.("a[href]");
        if (!shouldInterceptNavigation(event, link)) return;
        event.preventDefault();
        event.stopPropagation();
        if (!(await prepareToLeaveEditor())) return;
        window.location.assign(link.href);
    }

    root.addEventListener("click", (event) => {
        const alignNode = event.target.closest("[data-align]");
        if (alignNode) {
            alignSelected(alignNode.dataset.align);
            return;
        }
        const distributeNode = event.target.closest("[data-distribute]");
        if (distributeNode) {
            distributeSelected(distributeNode.dataset.distribute);
            return;
        }
        const actionNode = event.target.closest("[data-action]");
        if (!actionNode) return;
        const action = actionNode.dataset.action;
        if (action === "save") saveLayout();
        if (action === "close-editor") closeEditor();
        if (action === "undo") restoreHistory(-1);
        if (action === "redo") restoreHistory(1);
        if (action === "zoom-out") changeZoom(-1);
        if (action === "zoom-in") changeZoom(1);
        if (action === "fit-page") fitPage();
        if (action === "toggle-grid") {
            state.gridVisible = !state.gridVisible;
            actionNode.classList.toggle("is-active", state.gridVisible);
            actionNode.setAttribute("aria-pressed", String(state.gridVisible));
            renderCanvas();
        }
        if (action === "toggle-guides") {
            state.guidesVisible = !state.guidesVisible;
            actionNode.classList.toggle("is-active", state.guidesVisible);
            actionNode.setAttribute("aria-pressed", String(state.guidesVisible));
            if (!state.guidesVisible) hideGuides();
            renderCanvas();
        }
        if (action === "fit-content") fitSelectedToContent();
        if (action === "add-guide-x") addCustomGuide("vertical");
        if (action === "add-guide-y") addCustomGuide("horizontal");
        if (action === "add-text") addText();
        if (action === "add-list") addList();
        if (action === "add-image") addImage(actionNode);
        if (action === "add-background") addBackground(actionNode);
        if (action === "add-icon") addIcon();
        if (action === "add-table") addTable();
        if (action === "layer-up") moveLayer(1);
        if (action === "layer-down") moveLayer(-1);
        if (action === "open-media-picker") {
            openMediaPicker(selectedElement()?.type === "background" ? "replace-background" : "replace", actionNode);
        }
        if (action === "open-icon-media-picker") openMediaPicker("replace-icon", actionNode);
        if (action === "close-media-picker") closeMediaPicker();
        if (action === "apply-media-asset") applyMediaAsset();
        if (action === "refresh-media-assets") refreshMediaAssets();
        if (action === "remove-media-element") removeSelectedMediaElement();
        if (action === "remove-icon-asset") removeIconAsset();
    });

    root.querySelector('[data-action="zoom"]').addEventListener("change", (event) => {
        if (event.target.value === "fit") {
            fitPage();
            return;
        }
        setZoom(Number.parseFloat(event.target.value));
    });

    viewport.addEventListener("wheel", (event) => {
        if (!event.ctrlKey && !event.metaKey) return;
        event.preventDefault();
        changeZoom(event.deltaY < 0 ? 1 : -1, {
            clientX: event.clientX,
            clientY: event.clientY,
        });
    }, { passive: false });

    inspectorTabs.forEach((tab, index) => {
        tab.addEventListener("click", () => setInspectorTab(tab.dataset.inspectorTab));
        tab.addEventListener("keydown", (event) => {
            let nextIndex = null;
            if (event.key === "ArrowLeft") nextIndex = (index - 1 + inspectorTabs.length) % inspectorTabs.length;
            if (event.key === "ArrowRight") nextIndex = (index + 1) % inspectorTabs.length;
            if (event.key === "Home") nextIndex = 0;
            if (event.key === "End") nextIndex = inspectorTabs.length - 1;
            if (nextIndex === null) return;
            event.preventDefault();
            setInspectorTab(inspectorTabs[nextIndex].dataset.inspectorTab, { focus: true });
        });
    });

    root.querySelector('[data-action="preview"]').addEventListener("click", openPreview);

    root.querySelectorAll("[data-add-variable]").forEach((button) => {
        button.addEventListener("click", () => {
            addVariable(button.dataset.addVariable);
            button.closest("details")?.removeAttribute("open");
        });
    });

    propertiesNode.addEventListener("input", (event) => {
        if (event.target.tagName === "SELECT") return;
        if (event.target.matches("[data-prop]")) updateProperty(event.target);
        if (event.target.matches("[data-style]")) updateStyle(event.target);
        if (event.target.matches("[data-icon-style]")) updateIconStyle(event.target);
        if (event.target.matches("[data-table-style]")) updateTableStyle(event.target);
        if (event.target.matches("[data-table-columns]")) updateTableColumns(event.target);
        if (event.target.matches("[data-table-rows]")) updateTableRows(event.target);
        if (event.target.matches("[data-list-items]")) {
            const element = selectedElement();
            if (!element || element.type !== "list" || element.locked) return;
            element.items = event.target.value.split(/\r?\n/).slice(0, 20);
            markDirty();
            renderCanvas();
        }
    });
    propertiesNode.addEventListener("change", (event) => {
        if (event.target.matches("[data-prop]")) {
            updateProperty(event.target);
            renderProperties();
        }
        if (event.target.matches("[data-style]")) {
            updateStyle(event.target);
            renderProperties();
        }
        if (event.target.matches("[data-icon-style]")) {
            updateIconStyle(event.target);
            renderProperties();
        }
        if (event.target.matches("[data-table-style]")) {
            updateTableStyle(event.target);
            renderProperties();
        }
    });
    propertiesNode.querySelectorAll("[data-style-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const element = selectedElement();
            if (!element || element.locked) return;
            const key = button.dataset.styleToggle;
            element.style[key] = !element.style[key];
            markDirty();
            renderAll();
        });
    });

    mediaUploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = mediaUploadForm.querySelector('[type="submit"]');
        submitButton.disabled = true;
        mediaUploadError.hidden = true;
        mediaUploadError.textContent = "";
        try {
            const response = await fetch(root.dataset.mediaAssetsUploadUrl, {
                method: "POST",
                body: new FormData(mediaUploadForm),
                headers: { "Accept": "application/json" },
            });
            const payload = await response.json().catch(() => ({}));
            if (!response.ok || !payload.success || !payload.asset) {
                const messages = Object.values(payload.errors || {})
                    .flat()
                    .map((error) => typeof error === "string" ? error : error.message)
                    .filter(Boolean);
                throw new Error(messages.join(" ") || "Fișierul nu a putut fi încărcat.");
            }

            const uploadedAsset = payload.asset;
            const existingIndex = mediaAssets.findIndex((asset) => asset.id === uploadedAsset.id);
            if (existingIndex >= 0) mediaAssets.splice(existingIndex, 1, uploadedAsset);
            else mediaAssets.unshift(uploadedAsset);
            mediaAssetsById.set(uploadedAsset.id, uploadedAsset);
            try {
                await fetchMediaAssets();
            } catch (_error) {
                // The upload response is sufficient to keep the new asset usable.
            }
            pickerState.selectedAssetId = uploadedAsset.id;
            mediaUploadForm.reset();
            setPickerFeedback(`„${uploadedAsset.name}” a fost încărcat și selectat.`);
            renderMediaPicker();
            renderProperties();
            renderCanvas();
        } catch (error) {
            mediaUploadError.textContent = error.message || "Fișierul nu a putut fi încărcat.";
            mediaUploadError.hidden = false;
        } finally {
            submitButton.disabled = false;
        }
    });

    confirmAccept.addEventListener("click", () => closeConfirmation(true));
    confirmDialog.querySelectorAll("[data-confirm-cancel]").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            closeConfirmation(false);
        });
    });
    confirmDialog.addEventListener("cancel", (event) => {
        event.preventDefault();
        closeConfirmation(false);
    });

    document.addEventListener("click", handleDocumentNavigation, true);
    canvas.addEventListener("pointerdown", beginPointerInteraction);
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !mediaPicker.hidden) closeMediaPicker();
        const typing = event.target.closest("input, textarea, select, [contenteditable='true']");
        if (!typing && (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "z") {
            event.preventDefault();
            restoreHistory(event.shiftKey ? 1 : -1);
            return;
        }
        if (!typing && (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "y") {
            event.preventDefault();
            restoreHistory(1);
            return;
        }
        if (!["Delete", "Backspace"].includes(event.key)) return;
        if (typing) return;
        if (!state.selectedIds.length) return;
        event.preventDefault();
        deleteElements();
    });
    let bypassHistoryGuard = false;
    window.history.pushState({ diplomaEditorGuard: true }, "", window.location.href);
    window.addEventListener("popstate", async () => {
        if (bypassHistoryGuard) return;
        if (await prepareToLeaveEditor()) {
            bypassHistoryGuard = true;
            window.history.back();
            return;
        }
        window.history.pushState({ diplomaEditorGuard: true }, "", window.location.href);
    });

    if ("ResizeObserver" in window) {
        const viewportObserver = new ResizeObserver(refreshFittedZoom);
        viewportObserver.observe(viewport);
    } else {
        window.addEventListener("resize", refreshFittedZoom);
    }

    renderAll();
})();
```
