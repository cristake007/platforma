# apps/diplome/static/diplome/template_editor.css

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/static/diplome/template_editor.css`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `static`
- Size: 27577 bytes
- Source SHA-256: `b4015518a7f7bf289be744e93088a815f758caada9056a29efa3d00a26d6eff3`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```css
.diploma-editor {
    --editor-border: var(--tuvtk-border-default);
    --editor-muted: var(--tuvtk-panel-muted-bg);
    --editor-workspace: #eef2f6;
    --editor-selected: var(--tuvtk-brand-primary);
    display: grid;
    min-height: 0;
    height: 100%;
    overflow: hidden;
    border: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    grid-template-rows: auto auto minmax(0, 1fr) auto;
}

body:has(.diploma-editor) .drawer-content > main {
    overflow: hidden;
}

body:has(.diploma-editor) .drawer-content > main > div {
    height: 100%;
    max-width: none;
}

@media (min-width: 1024px) {
    body:has(.diploma-editor) .drawer-content > main > div {
        padding: 0;
    }

    body:has(.diploma-editor) .diploma-editor {
        border-block: 0;
        border-right: 0;
    }
}

.editor-heading,
.preview-heading {
    display: flex;
    min-width: 0;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1rem;
    border-bottom: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    padding: 0.9rem 1rem;
}

.editor-heading h1,
.preview-heading h1 {
    margin-top: 0.25rem;
    color: var(--tuvtk-heading-text);
    font-size: 1.4rem;
    font-weight: 750;
    line-height: 1.2;
}

.editor-heading p,
.preview-heading p {
    margin-top: 0.25rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.78rem;
}

.editor-heading-actions {
    display: flex;
    flex: none;
    flex-wrap: wrap;
    justify-content: flex-end;
    margin-left: auto;
    gap: 0.5rem;
}

.editor-toolbar {
    position: relative;
    z-index: 20;
    display: flex;
    min-height: 3.2rem;
    align-items: center;
    gap: 0.35rem;
    overflow: visible;
    border-bottom: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    padding: 0.45rem 0.65rem;
    scrollbar-width: thin;
}

.editor-tool,
.editor-tool-field {
    display: inline-flex;
    min-height: 2.1rem;
    flex: none;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.35rem 0.55rem;
    color: var(--tuvtk-body-text);
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1;
}

button.editor-tool {
    cursor: pointer;
}

.editor-tool:hover:not(:disabled),
.editor-tool.is-active {
    border-color: var(--tuvtk-brand-primary);
    background: var(--tuvtk-control-hover-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-tool:disabled {
    cursor: not-allowed;
    opacity: 0.42;
}

.editor-tool-field select {
    border: 0;
    background: transparent;
    color: inherit;
    font: inherit;
    outline: none;
}

.editor-zoom-controls {
    display: inline-flex;
    flex: none;
    align-items: stretch;
    gap: 0.25rem;
}

.editor-zoom-button {
    width: 2.1rem;
    padding-inline: 0;
    font-size: 1rem;
}

.editor-toolbar-divider {
    width: 1px;
    height: 1.75rem;
    flex: none;
    margin-inline: 0.2rem;
    background: var(--editor-border);
}

.editor-workspace {
    display: grid;
    min-width: 0;
    min-height: 0;
    grid-template-columns: 16rem minmax(28rem, 1fr) 18rem;
}

.editor-panel {
    position: relative;
    z-index: 10;
    display: flex;
    min-width: 0;
    min-height: 0;
    flex-direction: column;
    background: var(--tuvtk-panel-bg);
}

.editor-layers-panel {
    border-right: 1px solid var(--editor-border);
}

.editor-inspector-panel {
    border-left: 1px solid var(--editor-border);
}

.editor-inspector-tabs {
    display: grid;
    min-height: 2.8rem;
    flex: none;
    border-bottom: 1px solid var(--editor-border);
    background: var(--editor-muted);
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.editor-inspector-tab {
    position: relative;
    cursor: pointer;
    padding: 0.65rem 0.5rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.72rem;
    font-weight: 700;
}

.editor-inspector-tab + .editor-inspector-tab {
    border-left: 1px solid var(--editor-border);
}

.editor-inspector-tab:hover,
.editor-inspector-tab:focus-visible {
    background: var(--tuvtk-control-hover-bg);
    color: var(--tuvtk-brand-primary);
    outline: none;
}

.editor-inspector-tab.is-active {
    background: var(--tuvtk-panel-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-inspector-tab.is-active::after {
    position: absolute;
    right: 0.65rem;
    bottom: -1px;
    left: 0.65rem;
    height: 2px;
    background: var(--editor-selected);
    content: "";
}

.editor-inspector-pane {
    display: flex;
    min-width: 0;
    min-height: 0;
    flex: 1;
    flex-direction: column;
}

.editor-inspector-pane[hidden] {
    display: none;
}

.editor-inspector-pane-properties .editor-properties {
    flex: 1;
}

.editor-inspector-pane-elements {
    overflow-y: auto;
}

.editor-element-library {
    display: grid;
    gap: 1rem;
    padding: 0.65rem;
}

.editor-element-actions {
    display: grid;
    gap: 0.35rem;
}

.editor-element-action {
    display: grid;
    min-width: 0;
    cursor: pointer;
    align-items: center;
    gap: 0.6rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.5rem;
    text-align: left;
    grid-template-columns: 2rem minmax(0, 1fr);
}

.editor-element-action:hover,
.editor-element-action:focus-visible {
    border-color: var(--editor-selected);
    background: var(--tuvtk-control-hover-bg);
    outline: none;
}

.editor-element-action > span:last-child {
    display: grid;
    min-width: 0;
    gap: 0.1rem;
}

.editor-element-action strong {
    color: var(--tuvtk-heading-text);
    font-size: 0.72rem;
}

.editor-element-action small {
    overflow: hidden;
    color: var(--tuvtk-muted-text);
    font-size: 0.62rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-element-icon {
    display: grid;
    width: 2rem;
    height: 2rem;
    place-items: center;
    border: 1px solid var(--editor-border);
    background: var(--editor-muted);
    color: var(--tuvtk-brand-primary);
    font-size: 0.85rem;
    font-weight: 750;
}

.editor-variable-library {
    border-top: 1px solid var(--editor-border);
    padding-top: 0.75rem;
}

.editor-variable-library h3 {
    margin-bottom: 0.5rem;
    color: var(--tuvtk-heading-text);
    font-size: 0.68rem;
    font-weight: 750;
}

.editor-variable-library > div {
    display: grid;
    gap: 0.3rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.editor-variable-library button {
    min-height: 2rem;
    cursor: pointer;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    padding: 0.35rem;
    color: var(--tuvtk-body-text);
    font-size: 0.62rem;
    line-height: 1.2;
}

.editor-variable-library button:hover,
.editor-variable-library button:focus-visible {
    border-color: var(--editor-selected);
    color: var(--tuvtk-brand-primary);
    outline: none;
}

.editor-panel-title {
    display: flex;
    min-height: 2.8rem;
    flex: none;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--editor-border);
    padding: 0.65rem 0.75rem;
}

.editor-panel-title h2 {
    font-size: 0.8rem;
    font-weight: 750;
}

.editor-layers {
    min-height: 0;
    flex: 1;
    overflow-y: auto;
}

.editor-layer {
    display: grid;
    min-height: 2.75rem;
    cursor: pointer;
    align-items: center;
    gap: 0.3rem;
    border-bottom: 1px solid var(--editor-border);
    padding: 0.45rem 0.45rem;
    grid-template-columns: 1.1rem minmax(0, 1fr) repeat(4, 1.6rem);
}

.editor-layer:hover {
    background: var(--tuvtk-control-hover-bg);
}

.editor-layer.is-selected {
    background: var(--tuvtk-primary-tint-bg);
    box-shadow: inset 3px 0 var(--editor-selected);
}

.editor-layer-drag {
    color: var(--tuvtk-muted-text);
    font-size: 0.75rem;
    letter-spacing: -0.1em;
}

.editor-layer-name {
    overflow: hidden;
    color: var(--tuvtk-body-text);
    font-size: 0.76rem;
    font-weight: 600;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-layer button {
    display: grid;
    width: 1.6rem;
    height: 1.6rem;
    cursor: pointer;
    place-items: center;
    border-radius: var(--radius-field);
    color: var(--tuvtk-muted-text);
    font-size: 0.75rem;
}

.editor-layer button:hover {
    background: var(--tuvtk-panel-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-layer-actions {
    display: grid;
    flex: none;
    gap: 0.35rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.55rem;
}

.editor-align-actions {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.25rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.45rem;
}

.editor-align-actions button {
    min-height: 1.8rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    font-size: 0.8rem;
}

.editor-align-actions button:disabled {
    cursor: not-allowed;
    opacity: 0.35;
}

.editor-guide-controls {
    display: grid;
    gap: 0.35rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.5rem;
}

.editor-guide-input-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 2.4rem 2.4rem;
    gap: 0.3rem;
}

.editor-guide-input-row label {
    display: grid;
    gap: 0.2rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.65rem;
}

.editor-guide-input-row input,
.editor-guide-input-row button,
.editor-custom-guides button {
    min-width: 0;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.3rem 0.4rem;
    font-size: 0.7rem;
}

.editor-guide-controls small {
    color: var(--tuvtk-muted-text);
    font-size: 0.62rem;
    line-height: 1.25;
}

.editor-custom-guides {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
}

.editor-custom-guides button {
    color: var(--tuvtk-brand-primary);
}

.editor-layer-actions button {
    min-height: 2rem;
    cursor: pointer;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    color: var(--tuvtk-body-text);
    font-size: 0.7rem;
    font-weight: 600;
    text-align: left;
    padding-inline: 0.65rem;
}

.editor-layer-actions button:hover {
    border-color: var(--tuvtk-brand-primary);
    color: var(--tuvtk-brand-primary);
}

.editor-canvas-viewport {
    min-width: 0;
    min-height: 0;
    overflow: scroll;
    overscroll-behavior: contain;
    background: var(--editor-workspace);
    padding: 1rem;
    scrollbar-color: var(--scrollbar-thumb) var(--editor-muted);
    scrollbar-gutter: stable;
    scrollbar-width: auto;
}

.editor-canvas-viewport::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

.editor-canvas-viewport::-webkit-scrollbar-track,
.editor-canvas-viewport::-webkit-scrollbar-corner {
    background: var(--editor-muted);
}

.editor-canvas-viewport::-webkit-scrollbar-thumb {
    border: 3px solid var(--editor-muted);
    border-radius: 9999px;
    background: var(--scrollbar-thumb);
}

.editor-canvas-shell {
    position: relative;
    margin: 0 auto;
}

.editor-ruler-corner {
    position: absolute;
    z-index: 6;
    top: 0;
    left: 0;
    width: 1.7rem;
    height: 1.7rem;
    border-right: 1px solid var(--editor-border);
    border-bottom: 1px solid var(--editor-border);
    background: var(--editor-muted);
}

.editor-ruler {
    position: absolute;
    z-index: 5;
    overflow: hidden;
    background-color: var(--editor-muted);
    color: var(--tuvtk-muted-text);
    font-size: 0.58rem;
    pointer-events: none;
}

.editor-ruler-top {
    top: 0;
    left: 1.7rem;
    height: 1.7rem;
    border-bottom: 1px solid var(--editor-border);
    background-image: linear-gradient(90deg, transparent calc(100% - 1px), #aebbc6 0);
}

.editor-ruler-left {
    top: 1.7rem;
    left: 0;
    width: 1.7rem;
    border-right: 1px solid var(--editor-border);
    background-image: linear-gradient(180deg, transparent calc(100% - 1px), #aebbc6 0);
}

.editor-ruler-label {
    position: absolute;
    line-height: 1;
}

.editor-ruler-top .editor-ruler-label {
    top: 0.15rem;
    transform: translateX(2px);
}

.editor-ruler-left .editor-ruler-label {
    left: 0.12rem;
    transform: translateY(2px);
}

.editor-stage {
    position: absolute;
    top: 1.7rem;
    left: 1.7rem;
    transform-origin: top left;
}

.diploma-canvas {
    position: relative;
    overflow: hidden;
    background-color: #ffffff;
    box-shadow: 0 4px 14px rgb(23 33 43 / 0.18);
    outline: 1px solid #b8c4cf;
    touch-action: none;
}

.diploma-canvas.has-grid {
    background-image:
        linear-gradient(to right, rgb(22 65 148 / 0.16) 1px, transparent 1px),
        linear-gradient(to bottom, rgb(22 65 148 / 0.16) 1px, transparent 1px),
        linear-gradient(to right, rgb(22 65 148 / 0.055) 1px, transparent 1px),
        linear-gradient(to bottom, rgb(22 65 148 / 0.055) 1px, transparent 1px);
    background-size:
        var(--major-grid-size) var(--major-grid-size),
        var(--major-grid-size) var(--major-grid-size),
        var(--minor-grid-size) var(--minor-grid-size),
        var(--minor-grid-size) var(--minor-grid-size);
}

.diploma-element {
    position: absolute;
    display: flex;
    overflow: hidden;
    align-items: center;
    box-sizing: border-box;
    cursor: move;
    user-select: none;
    transform-origin: center;
}

.diploma-element.is-hidden {
    display: none;
}

.diploma-element.is-locked {
    cursor: not-allowed;
}

.diploma-element.is-selected {
    overflow: visible;
    outline: 2px solid var(--editor-selected);
    outline-offset: 1px;
}

.diploma-element-content {
    width: 100%;
    max-height: 100%;
    overflow: hidden;
    line-height: 1.18;
    white-space: pre-wrap;
}

.diploma-list {
    width: 100%;
    max-height: 100%;
    margin: 0;
    overflow: hidden;
    box-sizing: border-box;
}

.diploma-list li {
    padding-inline-start: 0.25em;
}

.diploma-element-table {
    align-items: stretch;
}

.diploma-element-table table {
    width: 100%;
    height: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.diploma-element-table th,
.diploma-element-table td {
    overflow: hidden;
    border: 1px solid var(--element-border, #164194);
    padding: 0.25rem;
    text-overflow: ellipsis;
}

.diploma-element-table th {
    background: var(--element-header, #edf3f9);
}

.diploma-placeholder {
    display: grid;
    width: 100%;
    height: 100%;
    place-items: center;
    border: 1px dashed var(--tuvtk-border-hover);
    background: var(--tuvtk-panel-muted-bg);
    color: var(--tuvtk-muted-text);
    font-family: Inter, "Segoe UI", sans-serif;
    font-size: 0.8rem;
}

.diploma-media {
    display: block;
    width: 100%;
    height: 100%;
    pointer-events: none;
    user-select: none;
}

.diploma-icon {
    display: grid;
    width: 100%;
    height: 100%;
    place-items: center;
    line-height: 1;
}

.diploma-icon-svg {
    display: block;
    width: 100%;
    height: 100%;
    overflow: visible;
}

.editor-resize-handle {
    position: absolute;
    right: -6px;
    bottom: -6px;
    width: 11px;
    height: 11px;
    cursor: nwse-resize;
    border: 2px solid #ffffff;
    background: var(--editor-selected);
    box-shadow: 0 0 0 1px var(--editor-selected);
}

.editor-guide {
    position: absolute;
    z-index: 2000;
    background: var(--tuvtk-brand-secondary);
    pointer-events: none;
}

.editor-guide-x {
    top: 0;
    bottom: 0;
    left: 50%;
    width: 1px;
}

.editor-guide-y {
    right: 0;
    left: 0;
    top: 50%;
    height: 1px;
}

.editor-guide-custom {
    z-index: 1999;
    background: repeating-linear-gradient(
        to bottom,
        var(--tuvtk-brand-secondary) 0 5px,
        transparent 5px 9px
    );
}

.editor-guide-custom.editor-guide-y {
    background: repeating-linear-gradient(
        to right,
        var(--tuvtk-brand-secondary) 0 5px,
        transparent 5px 9px
    );
}

.editor-checkbox-field {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 0.5rem;
    font-size: 0.72rem;
}

.editor-properties {
    min-height: 0;
    overflow-y: auto;
    padding: 0 0.75rem 1rem;
}

.editor-properties section {
    border-bottom: 1px solid var(--editor-border);
    padding-block: 0.8rem;
}

.editor-properties h3 {
    margin-bottom: 0.65rem;
    color: var(--tuvtk-heading-text);
    font-size: 0.72rem;
    font-weight: 750;
}

.editor-field-grid {
    display: grid;
    gap: 0.5rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.editor-field,
.editor-field-grid label {
    display: grid;
    min-width: 0;
    gap: 0.25rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.66rem;
    font-weight: 600;
}

.editor-field + .editor-field,
.editor-field-grid + .editor-field,
.editor-field + .editor-field-grid {
    margin-top: 0.55rem;
}

.editor-field input,
.editor-field select,
.editor-field textarea,
.editor-field-grid input,
.editor-field-grid select {
    width: 100%;
    min-height: 2rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.35rem 0.45rem;
    color: var(--tuvtk-body-text);
    font-size: 0.72rem;
    font-weight: 500;
}

.editor-field textarea {
    min-height: 4.5rem;
    resize: vertical;
}

.editor-toggle-row {
    display: flex;
    gap: 0.35rem;
    margin-top: 0.55rem;
}

.editor-toggle-row button {
    display: grid;
    width: 2rem;
    height: 2rem;
    cursor: pointer;
    place-items: center;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    color: var(--tuvtk-body-text);
}

.editor-toggle-row button[aria-pressed="true"] {
    border-color: var(--tuvtk-brand-primary);
    background: var(--tuvtk-brand-primary);
    color: #ffffff;
}

.editor-empty-properties {
    padding: 1rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.75rem;
    line-height: 1.5;
}

.editor-media-current-preview {
    display: grid;
    min-height: 3.5rem;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.6rem;
    border: 1px solid var(--editor-border);
    background: var(--editor-muted);
    padding: 0.4rem;
    grid-template-columns: 3rem minmax(0, 1fr);
}

.editor-media-current-preview img {
    width: 3rem;
    height: 2.7rem;
    background: #ffffff;
    object-fit: contain;
}

.editor-media-current-preview span:not(.editor-media-current-unavailable) {
    display: grid;
    min-width: 0;
    gap: 0.15rem;
}

.editor-media-current-preview strong,
.editor-media-current-preview small {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-media-current-preview strong {
    color: var(--tuvtk-heading-text);
    font-size: 0.7rem;
}

.editor-media-current-preview small,
.editor-media-current-unavailable {
    color: var(--tuvtk-muted-text);
    font-size: 0.62rem;
}

.editor-media-current-unavailable {
    grid-column: 1 / -1;
    padding: 0.5rem;
    text-align: center;
}

.editor-media-property-actions {
    display: grid;
    gap: 0.35rem;
    margin-block: 0.55rem;
    grid-template-columns: minmax(0, 1fr) auto;
}

.editor-media-property-actions button,
.editor-media-secondary-action {
    min-height: 1.9rem;
    cursor: pointer;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    padding-inline: 0.5rem;
    color: var(--tuvtk-body-text);
    font-size: 0.65rem;
    font-weight: 650;
}

.editor-media-property-actions button:hover:not(:disabled),
.editor-media-secondary-action:hover:not(:disabled) {
    border-color: var(--tuvtk-brand-primary);
    color: var(--tuvtk-brand-primary);
}

.editor-media-property-actions .is-danger {
    color: var(--color-error);
}

.editor-media-picker[hidden] {
    display: none;
}

.editor-media-picker {
    position: fixed;
    z-index: 1000;
    inset: 0;
    display: grid;
    place-items: center;
    padding: 1rem;
}

.editor-media-picker-backdrop {
    position: absolute;
    inset: 0;
    border: 0;
    background: rgb(23 33 43 / 0.55);
    cursor: default;
}

.editor-media-picker-panel {
    position: relative;
    display: grid;
    width: min(58rem, 100%);
    max-height: min(44rem, calc(100dvh - 2rem));
    overflow: hidden;
    border: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    box-shadow: 0 18px 55px rgb(23 33 43 / 0.28);
    grid-template-rows: auto minmax(0, 1fr) auto;
}

.editor-media-picker-header,
.editor-media-picker-footer,
.editor-media-library-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.editor-media-picker-header {
    border-bottom: 1px solid var(--editor-border);
    padding: 0.8rem 0.9rem;
}

.editor-media-picker-header h2 {
    color: var(--tuvtk-heading-text);
    font-size: 0.95rem;
    font-weight: 750;
}

.editor-media-picker-header p,
.editor-media-upload > p {
    margin-top: 0.15rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.68rem;
}

.editor-media-picker-close {
    display: grid;
    width: 2rem;
    height: 2rem;
    flex: none;
    cursor: pointer;
    place-items: center;
    border-radius: var(--radius-field);
    color: var(--tuvtk-muted-text);
    font-size: 1.3rem;
}

.editor-media-picker-close:hover {
    background: var(--tuvtk-control-hover-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-media-picker-body {
    display: grid;
    min-height: 0;
    grid-template-columns: minmax(0, 1fr) 16rem;
}

.editor-media-library {
    min-width: 0;
    min-height: 0;
    overflow-y: auto;
    padding: 0.8rem;
}

.editor-media-library-toolbar {
    margin-bottom: 0.65rem;
    color: var(--tuvtk-heading-text);
    font-size: 0.73rem;
}

.editor-media-feedback,
.editor-media-upload-error {
    margin-bottom: 0.65rem;
    border: 1px solid var(--tuvtk-border-default);
    background: var(--tuvtk-panel-muted-bg);
    padding: 0.45rem 0.55rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.67rem;
    line-height: 1.35;
}

.editor-media-feedback.is-error,
.editor-media-upload-error {
    border-color: var(--color-error);
    color: var(--color-error);
}

.editor-media-picker-grid {
    display: grid;
    gap: 0.55rem;
    grid-template-columns: repeat(auto-fill, minmax(9.5rem, 1fr));
}

.editor-media-card {
    display: grid;
    min-width: 0;
    cursor: pointer;
    overflow: hidden;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    text-align: left;
}

.editor-media-card:hover,
.editor-media-card:focus-visible,
.editor-media-card.is-selected {
    border-color: var(--editor-selected);
    outline: none;
    box-shadow: 0 0 0 2px rgb(22 65 148 / 0.14);
}

.editor-media-card.is-selected {
    background: var(--tuvtk-primary-tint-bg);
}

.editor-media-card-preview {
    display: grid;
    height: 6rem;
    place-items: center;
    border-bottom: 1px solid var(--editor-border);
    background: var(--editor-muted);
    padding: 0.35rem;
}

.editor-media-card-preview img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.editor-media-card-copy {
    display: grid;
    min-width: 0;
    gap: 0.15rem;
    padding: 0.45rem 0.5rem;
}

.editor-media-card-copy strong,
.editor-media-card-copy small {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-media-card-copy strong {
    color: var(--tuvtk-heading-text);
    font-size: 0.7rem;
}

.editor-media-card-copy small {
    color: var(--tuvtk-muted-text);
    font-size: 0.6rem;
}

.editor-media-picker-empty {
    display: grid;
    min-height: 12rem;
    place-content: center;
    gap: 0.3rem;
    border: 1px dashed var(--tuvtk-border-hover);
    color: var(--tuvtk-muted-text);
    font-size: 0.72rem;
    text-align: center;
}

.editor-media-picker-empty[hidden] {
    display: none;
}

.editor-media-picker-empty strong {
    color: var(--tuvtk-heading-text);
}

.editor-media-upload {
    overflow-y: auto;
    border-left: 1px solid var(--editor-border);
    background: var(--editor-muted);
    padding: 0.8rem;
}

.editor-media-upload h3 {
    color: var(--tuvtk-heading-text);
    font-size: 0.75rem;
    font-weight: 750;
}

.editor-media-upload form {
    margin-top: 0.75rem;
}

.editor-media-upload input[type="file"] {
    padding: 0.25rem;
    font-size: 0.62rem;
}

.editor-media-picker-footer {
    min-height: 3.25rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.6rem 0.9rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.68rem;
}

.editor-media-picker-footer > div {
    display: flex;
    gap: 0.45rem;
}

.editor-statusbar {
    position: sticky;
    z-index: 30;
    bottom: 0;
    display: grid;
    min-height: 2.8rem;
    align-items: center;
    border-top: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    color: var(--tuvtk-muted-text);
    font-size: 0.7rem;
    grid-template-columns: repeat(4, minmax(0, 1fr));
}

.editor-statusbar > span {
    display: flex;
    min-height: 1.8rem;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    border-right: 1px solid var(--editor-border);
}

.editor-statusbar > span:last-child {
    border-right: 0;
}

.editor-save-status i {
    width: 0.65rem;
    height: 0.65rem;
    border-radius: 50%;
    background: var(--color-success);
}

.editor-save-status.is-dirty i {
    background: var(--color-warning);
}

.editor-save-status.is-saving i {
    background: var(--color-info);
}

.editor-save-status.is-error i {
    background: var(--color-error);
}

.diploma-preview-page {
    overflow: hidden;
    border: 1px solid var(--tuvtk-border-default);
    background: var(--tuvtk-panel-bg);
}

.preview-workspace {
    min-height: calc(100dvh - 15rem);
    overflow: auto;
    background: #eef2f6;
    padding: 2rem;
}

.preview-canvas-frame {
    position: relative;
    margin: 0 auto;
    transform-origin: top left;
}

.preview-canvas .diploma-element {
    cursor: default;
}

@media (max-width: 1199px) {
    .editor-workspace {
        grid-template-columns: 10.5rem minmax(28rem, 1fr) 16rem;
    }
}

@media (max-width: 899px) {
    .diploma-editor {
        min-height: 0;
        overflow: hidden;
    }

    .editor-heading,
    .preview-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .editor-heading-actions {
        align-self: flex-end;
    }

    .editor-workspace {
        min-height: 0;
        grid-template-columns: 10rem minmax(42rem, 1fr) 16rem;
        overflow-x: auto;
    }

    .editor-statusbar {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .editor-statusbar > span:nth-child(2) {
        border-right: 0;
    }

    .editor-media-picker {
        align-items: start;
        padding: 0.5rem;
    }

    .editor-media-picker-panel {
        max-height: calc(100dvh - 1rem);
    }

    .editor-media-picker-body {
        overflow-y: auto;
        grid-template-columns: 1fr;
    }

    .editor-media-library,
    .editor-media-upload {
        overflow: visible;
    }

    .editor-media-upload {
        border-top: 1px solid var(--editor-border);
        border-left: 0;
    }

    .editor-media-picker-footer {
        align-items: flex-start;
        flex-direction: column;
    }

    .editor-media-picker-footer > div {
        width: 100%;
        justify-content: flex-end;
    }
}
```
