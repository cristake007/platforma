# apps/diplome/static/diplome/template_renderer.js

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/static/diplome/template_renderer.js`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `static`
- Size: 9571 bytes
- Source SHA-256: `35183f1835f7bcedcb15b0007a537f04267566e435b9cd27fce14824cfd087a5`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```javascript
(function () {
    "use strict";

    const PX_PER_MM = 96 / 25.4;

    const FONT_STACKS = {
        Inter: 'InterVariable, Inter, "Segoe UI", sans-serif',
        Lora: 'Lora, Georgia, "Times New Roman", serif',
        Georgia: 'Georgia, "Times New Roman", serif',
        Arial: 'Arial, sans-serif',
        "Times New Roman": '"Times New Roman", serif',
    };
    const SVG_NS = "http://www.w3.org/2000/svg";

    function mmToPx(value) {
        return value * PX_PER_MM;
    }

    function pxToMm(value) {
        return value / PX_PER_MM;
    }

    function pagePixelSize(layout) {
        return {
            width: mmToPx(layout.page.width_mm),
            height: mmToPx(layout.page.height_mm),
        };
    }

    function textNode(className, value) {
        const node = document.createElement("div");
        node.className = className;
        node.textContent = value;
        return node;
    }

    function svgIcon(iconName) {
        const svg = document.createElementNS(SVG_NS, "svg");
        svg.classList.add("diploma-icon-svg");
        svg.setAttribute("viewBox", "0 0 24 24");
        svg.setAttribute("aria-hidden", "true");
        svg.setAttribute("fill", "none");
        svg.setAttribute("stroke", "currentColor");
        svg.setAttribute("stroke-width", "1.8");
        svg.setAttribute("stroke-linecap", "round");
        svg.setAttribute("stroke-linejoin", "round");
        const paths = {
            award: [
                ["circle", { cx: "12", cy: "8", r: "5" }],
                ["path", { d: "M8.7 12.7 7.5 22l4.5-2.7 4.5 2.7-1.2-9.3" }],
            ],
            "patch-check": [
                ["rect", { x: "3.5", y: "3.5", width: "17", height: "17", rx: "2" }],
                ["path", { d: "m7.5 12 3 3 6-6" }],
            ],
            star: [["path", { d: "m12 2.8 2.8 5.7 6.3.9-4.6 4.5 1.1 6.3-5.6-3-5.6 3 1.1-6.3-4.6-4.5 6.3-.9Z" }]],
        };
        (paths[iconName] || paths.star).forEach(([tag, attributes]) => {
            const node = document.createElementNS(SVG_NS, tag);
            Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
            svg.appendChild(node);
        });
        return svg;
    }

    function applyTypography(node, style) {
        node.style.fontFamily = FONT_STACKS[style.fontFamily] || FONT_STACKS.Inter;
        node.style.fontSize = `${style.fontSize}px`;
        node.style.fontWeight = style.bold ? "700" : "400";
        node.style.fontStyle = style.italic ? "italic" : "normal";
        node.style.textDecoration = style.underline ? "underline" : "none";
        node.style.color = style.color;
        node.style.textAlign = style.align;
        node.style.lineHeight = String(style.lineHeight ?? 1.18);
        node.style.letterSpacing = `${style.letterSpacing ?? 0}px`;
        node.style.textTransform = style.textTransform || "none";
    }

    function renderList(element) {
        const list = document.createElement(element.style.listType === "number" ? "ol" : "ul");
        list.className = "diploma-list";
        element.items.forEach((item) => {
            const row = document.createElement("li");
            row.textContent = item;
            list.appendChild(row);
        });
        applyTypography(list, element.style);
        list.style.paddingInlineStart = `${mmToPx(element.style.indent_mm)}px`;
        return list;
    }

    function renderTable(element) {
        const table = document.createElement("table");
        table.setAttribute("aria-label", element.label);
        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        element.columns.forEach((column) => {
            const cell = document.createElement("th");
            cell.textContent = column;
            headerRow.appendChild(cell);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        const tbody = document.createElement("tbody");
        element.rows.forEach((row) => {
            const tableRow = document.createElement("tr");
            row.forEach((value) => {
                const cell = document.createElement("td");
                cell.textContent = value;
                tableRow.appendChild(cell);
            });
            tbody.appendChild(tableRow);
        });
        table.appendChild(tbody);
        table.style.fontFamily = FONT_STACKS[element.style.fontFamily] || FONT_STACKS.Inter;
        table.style.fontSize = `${element.style.fontSize}px`;
        table.style.fontWeight = element.style.bold ? "700" : "400";
        table.style.color = element.style.color;
        table.style.textAlign = element.style.align;
        return table;
    }

    function renderContent(element, sampleData, assets) {
        if (element.type === "text") {
            const node = textNode("diploma-element-content", element.text);
            applyTypography(node, element.style);
            return node;
        }
        if (element.type === "variable") {
            const value = sampleData?.[element.variable] || `{{ ${element.variable} }}`;
            const node = textNode("diploma-element-content", value);
            applyTypography(node, element.style);
            return node;
        }
        if (element.type === "list") return renderList(element);
        if (element.type === "table") {
            return renderTable(element);
        }
        if (element.type === "icon") {
            const asset = element.assetId ? assets?.get(element.assetId) : null;
            if (asset) {
                const image = document.createElement("img");
                image.className = "diploma-media";
                image.src = asset.url;
                image.alt = element.alt || "";
                image.draggable = false;
                image.style.objectFit = "contain";
                image.style.opacity = String(element.style.opacity);
                return image;
            }
            const node = document.createElement("div");
            node.className = "diploma-icon";
            node.style.color = element.style.color;
            node.style.opacity = String(element.style.opacity);
            node.appendChild(svgIcon(element.iconName));
            return node;
        }
        const asset = assets?.get(element.assetId);
        if (asset) {
            const image = document.createElement("img");
            image.className = "diploma-media";
            image.src = asset.url;
            image.alt = element.alt || "";
            image.draggable = false;
            image.style.objectFit = element.style.fit === "stretch" ? "fill" : element.style.fit;
            image.style.opacity = String(element.style.opacity);
            return image;
        }
        const node = textNode("diploma-placeholder", "Fișier media indisponibil");
        node.style.opacity = String(element.style.opacity);
        return node;
    }

    function renderElement(element, options) {
        const node = document.createElement("div");
        node.className = `diploma-element diploma-element-${element.type}`;
        node.dataset.elementId = element.id;
        node.style.left = `${mmToPx(element.x_mm)}px`;
        node.style.top = `${mmToPx(element.y_mm)}px`;
        node.style.width = `${mmToPx(element.width_mm)}px`;
        node.style.height = `${mmToPx(element.height_mm)}px`;
        node.style.zIndex = String(element.zIndex);
        node.style.transform = `rotate(${element.rotation}deg)`;
        node.setAttribute("role", options.editable ? "button" : "group");
        node.setAttribute("aria-label", element.label);
        if (!element.visible) node.classList.add("is-hidden");
        if (element.locked) node.classList.add("is-locked");
        const selectedIds = options.selectedIds || (options.selectedId ? [options.selectedId] : []);
        const selected = selectedIds.includes(element.id);
        if (options.editable && selected) {
            node.classList.add("is-selected");
            node.setAttribute("aria-pressed", "true");
        }
        if (element.type === "table") {
            node.style.setProperty("--element-border", element.style.borderColor);
            node.style.setProperty("--element-header", element.style.headerBackground);
        }
        node.appendChild(renderContent(element, options.sampleData, options.assets));
        if (options.editable && selected && selectedIds.length === 1 && !element.locked) {
            const handle = document.createElement("span");
            handle.className = "editor-resize-handle";
            handle.dataset.resizeHandle = "true";
            handle.setAttribute("aria-label", "Redimensionează elementul");
            node.appendChild(handle);
        }
        return node;
    }

    function render(canvas, layout, options = {}) {
        const guides = Array.from(canvas.querySelectorAll(".editor-guide"));
        canvas.replaceChildren(...guides);
        const pageSize = pagePixelSize(layout);
        canvas.style.width = `${pageSize.width}px`;
        canvas.style.height = `${pageSize.height}px`;
        canvas.style.setProperty("--minor-grid-size", `${mmToPx(layout.page.grid_mm)}px`);
        canvas.style.setProperty("--major-grid-size", `${mmToPx(layout.page.major_grid_mm)}px`);
        [...layout.elements]
            .sort((left, right) => left.zIndex - right.zIndex)
            .forEach((element) => canvas.appendChild(renderElement(element, options)));
    }

    window.DiplomaRenderer = { render, mmToPx, pxToMm, pagePixelSize };
})();
```
