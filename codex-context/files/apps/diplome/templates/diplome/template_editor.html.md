# apps/diplome/templates/diplome/template_editor.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/templates/diplome/template_editor.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 24754 bytes
- Source SHA-256: `bc6d3444fd9fe4eca400136fa3478948cd9641453620af3462408fac1fbb61a7`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Editor {{ diploma_template.name }} | Platforma TUVTK{% endblock %}
{% block sidebar_start_collapsed %}true{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'diplome/template_editor.css' %}">
{% endblock %}

{% block content %}
<section
    id="diploma-editor"
    class="diploma-editor"
    data-save-url="{% url 'diplome:template_editor' diploma_template.pk %}"
    data-preview-url="{% url 'diplome:template_preview' diploma_template.pk %}"
    data-template-list-url="{% url 'diplome:template_list' %}"
    data-is-draft-template="{{ is_draft_template|yesno:'true,false' }}"
    data-media-assets-api-url="{{ media_assets_api_url }}"
    data-media-assets-upload-url="{{ media_assets_upload_url }}"
>
    <header class="editor-heading">
        <div class="editor-heading-actions">
            <button type="button" class="btn btn-primary btn-sm" data-action="save">Salvează</button>
            <a href="{% url 'diplome:template_preview' diploma_template.pk %}" class="btn btn-outline btn-primary btn-sm" data-action="preview">Previzualizează</a>
            <button type="button" class="btn btn-outline btn-error btn-sm" data-action="close-editor">Închide</button>
        </div>
    </header>

    <form id="editor-save-form" class="hidden">{% csrf_token %}</form>
    <form id="editor-discard-form" method="post" action="{% url 'diplome:template_delete' diploma_template.pk %}" class="hidden">{% csrf_token %}</form>

    <dialog id="editor-confirm-dialog" class="modal" aria-labelledby="editor-confirm-title">
        <div class="modal-box max-w-md">
            <h2 id="editor-confirm-title" class="text-lg font-bold">Confirmă acțiunea</h2>
            <p id="editor-confirm-message" class="mt-3 text-sm text-base-content/75"></p>
            <div class="modal-action">
                <button type="button" id="editor-confirm-cancel" class="btn btn-ghost" data-confirm-cancel>Renunță</button>
                <button type="button" class="btn btn-error" data-confirm-accept>Șterge</button>
            </div>
        </div>
        <form method="dialog" class="modal-backdrop"><button data-confirm-cancel>Închide</button></form>
    </dialog>

    <div
        id="editor-media-picker"
        class="editor-media-picker"
        role="dialog"
        aria-modal="true"
        aria-labelledby="editor-media-picker-title"
        hidden
    >
        <button type="button" class="editor-media-picker-backdrop" data-action="close-media-picker" aria-label="Închide selectorul media" tabindex="-1"></button>
        <div class="editor-media-picker-panel">
            <header class="editor-media-picker-header">
                <div>
                    <h2 id="editor-media-picker-title">Alege un fișier media</h2>
                    <p id="editor-media-picker-description">Selectează un fișier din biblioteca ta.</p>
                </div>
                <button type="button" class="editor-media-picker-close" data-action="close-media-picker" aria-label="Închide">×</button>
            </header>
            <div class="editor-media-picker-body">
                <section class="editor-media-library" aria-label="Fișiere media disponibile">
                    <div class="editor-media-library-toolbar">
                        <strong>Biblioteca mea</strong>
                        <button type="button" class="editor-media-secondary-action" data-action="refresh-media-assets">Reîmprospătează</button>
                    </div>
                    <p id="editor-media-picker-feedback" class="editor-media-feedback" role="status" hidden></p>
                    <div id="editor-media-picker-grid" class="editor-media-picker-grid" role="listbox" aria-label="Fișiere media"></div>
                    <div id="editor-media-picker-empty" class="editor-media-picker-empty" hidden>
                        <strong>Biblioteca media este goală.</strong>
                        <span>Încarcă un fișier fără să părăsești editorul.</span>
                    </div>
                </section>
                <aside class="editor-media-upload" aria-label="Încarcă un fișier media">
                    <h3>Încarcă un fișier nou</h3>
                    <p>SVG, PNG, JPG sau WEBP.</p>
                    <form id="editor-media-upload-form" enctype="multipart/form-data">
                        {% csrf_token %}
                        <label class="editor-field">Nume în bibliotecă
                            <input type="text" name="name" maxlength="160" placeholder="Opțional">
                        </label>
                        <label class="editor-field">Fișier
                            <input type="file" name="file" required accept=".svg,.png,.jpg,.jpeg,.webp,image/svg+xml,image/png,image/jpeg,image/webp">
                        </label>
                        <p id="editor-media-upload-error" class="editor-media-upload-error" role="alert" hidden></p>
                        <button type="submit" class="btn btn-primary btn-sm w-full">Încarcă</button>
                    </form>
                </aside>
            </div>
            <footer class="editor-media-picker-footer">
                <span id="editor-media-picker-selection">Niciun fișier selectat</span>
                <div>
                    <button type="button" class="btn btn-ghost btn-sm" data-action="close-media-picker">Renunță</button>
                    <button type="button" class="btn btn-primary btn-sm" data-action="apply-media-asset" disabled>Folosește fișierul</button>
                </div>
            </footer>
        </div>
    </div>

    <div class="editor-toolbar" role="toolbar" aria-label="Instrumente editor">
        <button type="button" class="editor-tool" data-action="undo" title="Anulează ultima modificare" disabled>↶ <span>Undo</span></button>
        <button type="button" class="editor-tool" data-action="redo" title="Reface ultima modificare" disabled>↷ <span>Redo</span></button>
        <span class="editor-toolbar-divider"></span>
        <div class="editor-zoom-controls" role="group" aria-label="Zoom canvas">
            <button type="button" class="editor-tool editor-zoom-button" data-action="zoom-out" aria-label="Micșorează zoomul" title="Micșorează zoomul">−</button>
            <label class="editor-tool-field">Zoom
                <select data-action="zoom" aria-label="Nivel zoom" title="Poți folosi și Ctrl + rotița mouse-ului">
                    <option value="fit" selected>Încadrează pagina</option>
                    <option value="0.25">25%</option>
                    <option value="0.5">50%</option>
                    <option value="0.75">75%</option>
                    <option value="1">100%</option>
                    <option value="1.25">125%</option>
                    <option value="1.5">150%</option>
                    <option value="2">200%</option>
                    <option value="" data-zoom-custom hidden></option>
                </select>
            </label>
            <button type="button" class="editor-tool editor-zoom-button" data-action="zoom-in" aria-label="Mărește zoomul" title="Mărește zoomul">+</button>
            <button type="button" class="editor-tool" data-action="fit-page" title="Încadrează pagina în spațiul disponibil">Încadrează</button>
        </div>
        <button type="button" class="editor-tool is-active" data-action="toggle-grid" aria-pressed="true">▦ <span>Grid</span></button>
        <button type="button" class="editor-tool is-active" data-action="toggle-guides" aria-pressed="true">┼ <span>Ghidaje</span></button>
        <button type="button" class="editor-tool" data-action="fit-content" title="Potrivește caseta la conținut" disabled>↙↗ <span>Potrivește</span></button>
    </div>

    <div class="editor-workspace">
        <aside class="editor-panel editor-layers-panel" aria-label="Straturi">
            <div class="editor-panel-title"><h2>Straturi</h2><span aria-hidden="true">▤</span></div>
            <div id="editor-layers" class="editor-layers"></div>
            <div class="editor-align-actions" role="toolbar" aria-label="Aliniere selecție">
                <button type="button" data-align="left" title="Aliniază la stânga">⊢</button>
                <button type="button" data-align="center" title="Centrează orizontal">↔</button>
                <button type="button" data-align="right" title="Aliniază la dreapta">⊣</button>
                <button type="button" data-align="top" title="Aliniază sus">⊤</button>
                <button type="button" data-align="middle" title="Centrează vertical">↕</button>
                <button type="button" data-align="bottom" title="Aliniază jos">⊥</button>
                <button type="button" data-distribute="horizontal" title="Distribuie orizontal">⋯</button>
                <button type="button" data-distribute="vertical" title="Distribuie vertical">⋮</button>
            </div>
            <div class="editor-guide-controls">
                <div class="editor-guide-input-row">
                    <label>Poziție (mm)<input type="number" id="editor-guide-position" min="0" step="1" value="10"></label>
                    <button type="button" data-action="add-guide-x" title="Adaugă ghid vertical">+ V</button>
                    <button type="button" data-action="add-guide-y" title="Adaugă ghid orizontal">+ O</button>
                </div>
                <small>Elementele se fixează automat pe ghidaje când sunt mutate.</small>
                <div id="editor-custom-guides" class="editor-custom-guides"></div>
            </div>
            <div class="editor-layer-actions">
                <button type="button" data-action="layer-up">↑ Mută în sus</button>
                <button type="button" data-action="layer-down">↓ Mută în jos</button>
            </div>
        </aside>

        <main class="editor-canvas-viewport" id="editor-canvas-viewport">
            <div class="editor-canvas-shell" id="editor-canvas-shell">
                <div class="editor-ruler-corner"></div>
                <div class="editor-ruler editor-ruler-top" id="editor-ruler-top"></div>
                <div class="editor-ruler editor-ruler-left" id="editor-ruler-left"></div>
                <div class="editor-stage" id="editor-stage">
                    <div class="diploma-canvas has-grid" id="diploma-canvas" tabindex="0" aria-label="Canvas template diplomă">
                        <div class="editor-guide editor-guide-x" hidden></div>
                        <div class="editor-guide editor-guide-y" hidden></div>
                    </div>
                </div>
            </div>
        </main>

        <aside class="editor-panel editor-inspector-panel" aria-label="Inspector template">
            <div class="editor-inspector-tabs" role="tablist" aria-label="Panouri inspector">
                <button type="button" id="editor-tab-elements" class="editor-inspector-tab is-active" role="tab" aria-selected="true" aria-controls="editor-panel-elements" data-inspector-tab="elements">Elemente</button>
                <button type="button" id="editor-tab-properties" class="editor-inspector-tab" role="tab" aria-selected="false" aria-controls="editor-panel-properties" data-inspector-tab="properties" tabindex="-1">Proprietăți</button>
            </div>

            <div id="editor-panel-elements" class="editor-inspector-pane editor-inspector-pane-elements" role="tabpanel" aria-labelledby="editor-tab-elements" data-inspector-panel="elements">
                <div class="editor-panel-title"><h2>Adaugă element</h2><span aria-hidden="true">＋</span></div>
                <div class="editor-element-library">
                    <div class="editor-element-actions">
                        <button type="button" class="editor-element-action" data-action="add-text"><span class="editor-element-icon" aria-hidden="true">A</span><span><strong>Text</strong><small>Bloc de text liber</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-list"><span class="editor-element-icon" aria-hidden="true">•</span><span><strong>Listă</strong><small>Listă cu marcatori</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-image"><span class="editor-element-icon" aria-hidden="true">▧</span><span><strong>Imagine</strong><small>Fișier din bibliotecă</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-background"><span class="editor-element-icon" aria-hidden="true">▣</span><span><strong>Fundal</strong><small>Imagine pe întreaga pagină</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-icon"><span class="editor-element-icon" aria-hidden="true">☆</span><span><strong>Icon</strong><small>Simbol sau grafică</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-table"><span class="editor-element-icon" aria-hidden="true">▦</span><span><strong>Tabel</strong><small>Rânduri și coloane</small></span></button>
                    </div>
                    <section class="editor-variable-library" aria-labelledby="editor-variable-library-title">
                        <h3 id="editor-variable-library-title">Variabile participant</h3>
                        <div>
                            <button type="button" data-add-variable="full_name">Nume complet</button>
                            <button type="button" data-add-variable="date_of_birth">Data nașterii</button>
                            <button type="button" data-add-variable="place_of_birth">Locul nașterii</button>
                            <button type="button" data-add-variable="certificate_number">Număr certificat</button>
                        </div>
                    </section>
                </div>
            </div>

            <div id="editor-panel-properties" class="editor-inspector-pane editor-inspector-pane-properties" role="tabpanel" aria-labelledby="editor-tab-properties" data-inspector-panel="properties" hidden>
                <div class="editor-panel-title"><h2>Element selectat</h2><span id="property-lock-indicator" aria-hidden="true">○</span></div>
                <div id="editor-empty-properties" class="editor-empty-properties">Selectează un element pentru a-i edita proprietățile.</div>
                <div id="editor-multi-properties" class="editor-empty-properties" hidden>
                    <strong data-multi-count>0 elemente selectate</strong>
                    <span>Folosește instrumentele de aliniere din panoul Straturi sau trage selecția pentru a muta elementele deblocate împreună.</span>
                </div>
                <div id="editor-properties" class="editor-properties" hidden>
                <section>
                    <h3>Poziție și dimensiune</h3>
                    <div class="editor-field-grid">
                        <label>X (mm)<input type="number" data-prop="x_mm" step="1"></label>
                        <label>Y (mm)<input type="number" data-prop="y_mm" step="1"></label>
                        <label>Lățime (mm)<input type="number" data-prop="width_mm" min="1" step="1"></label>
                        <label>Înălțime (mm)<input type="number" data-prop="height_mm" min="1" step="1"></label>
                        <label>Rotire<input type="number" data-prop="rotation" min="-180" max="180"></label>
                        <label>Ordine strat<input type="number" data-prop="zIndex" min="0" max="1000"></label>
                    </div>
                </section>
                <section data-section="typography">
                    <h3>Tipografie</h3>
                    <label class="editor-field">Familie font
                        <select data-style="fontFamily">
                            <option>Lora</option><option>Inter</option><option>Georgia</option><option>Arial</option><option>Times New Roman</option>
                        </select>
                    </label>
                    <div class="editor-field-grid">
                        <label>Dimensiune<input type="number" data-style="fontSize" min="8" max="200"></label>
                        <label>Culoare<input type="color" data-style="color"></label>
                    </div>
                    <div class="editor-toggle-row">
                        <button type="button" data-style-toggle="bold" aria-pressed="false"><strong>B</strong></button>
                        <button type="button" data-style-toggle="italic" aria-pressed="false"><em>I</em></button>
                        <button type="button" data-style-toggle="underline" aria-pressed="false"><u>U</u></button>
                    </div>
                    <label class="editor-field">Aliniere
                        <select data-style="align"><option value="left">Stânga</option><option value="center">Centru</option><option value="right">Dreapta</option></select>
                    </label>
                    <div class="editor-field-grid">
                        <label>Înălțime rând<input type="number" data-style="lineHeight" min="0.8" max="3" step="0.01"></label>
                        <label>Spațiere litere (px)<input type="number" data-style="letterSpacing" min="-5" max="20" step="0.1"></label>
                    </div>
                    <label class="editor-field">Transformare text
                        <select data-style="textTransform"><option value="none">Niciuna</option><option value="uppercase">MAJUSCULE</option><option value="lowercase">minuscule</option></select>
                    </label>
                </section>
                <section data-section="list" hidden>
                    <h3>Listă</h3>
                    <label class="editor-field">Elemente (unul pe rând)<textarea data-list-items rows="6" maxlength="4019"></textarea></label>
                    <div class="editor-field-grid">
                        <label>Tip
                            <select data-style="listType"><option value="bullet">Marcatori</option><option value="number">Numerotată</option></select>
                        </label>
                        <label>Indentare (mm)<input type="number" data-style="indent_mm" min="0" max="50" step="1"></label>
                    </div>
                </section>
                <section data-section="media" hidden>
                    <h3>Fișier media</h3>
                    <div id="editor-media-current-preview" class="editor-media-current-preview"></div>
                    <label class="editor-field">Fișier din bibliotecă
                        <select data-prop="assetId"></select>
                    </label>
                    <div class="editor-media-property-actions">
                        <button type="button" data-action="open-media-picker">Alege sau înlocuiește</button>
                        <button type="button" class="is-danger" data-action="remove-media-element">Elimină din template</button>
                    </div>
                    <div class="editor-field-grid">
                        <label>Încadrare
                            <select data-style="fit"><option value="contain">Conține</option><option value="cover">Acoperă</option><option value="stretch">Întinde</option></select>
                        </label>
                        <label>Opacitate<input type="number" data-style="opacity" min="0" max="1" step="0.05"></label>
                    </div>
                    <label class="editor-field">Text alternativ<input type="text" data-prop="alt" maxlength="160"></label>
                    <a href="{% url 'media_library:index' %}" class="mt-2 inline-flex text-xs font-semibold text-primary hover:underline">Deschide biblioteca media</a>
                </section>
                <section data-section="icon" hidden>
                    <h3>Icon</h3>
                    <div id="editor-icon-current-preview" class="editor-media-current-preview"></div>
                    <label class="editor-field">Icon inclus
                        <select data-prop="iconName">
                            <option value="award">Medalie</option>
                            <option value="patch-check">Validare</option>
                            <option value="star">Stea</option>
                        </select>
                    </label>
                    <div class="editor-field-grid">
                        <label>Culoare<input type="color" data-icon-style="color"></label>
                        <label>Opacitate<input type="number" data-icon-style="opacity" min="0" max="1" step="0.05"></label>
                    </div>
                    <div class="editor-media-property-actions">
                        <button type="button" data-action="open-icon-media-picker">Alege sau încarcă grafică</button>
                        <button type="button" class="is-danger" data-action="remove-icon-asset">Revino la iconul inclus</button>
                    </div>
                </section>
                <section data-section="table" hidden>
                    <h3>Tabel</h3>
                    <label class="editor-field">Coloane (una pe rând)<textarea data-table-columns rows="4" maxlength="967"></textarea></label>
                    <label class="editor-field">Rânduri (celule separate prin |)<textarea data-table-rows rows="6" maxlength="25619"></textarea></label>
                    <div class="editor-field-grid">
                        <label>Font
                            <select data-table-style="fontFamily"><option>Inter</option><option>Lora</option><option>Georgia</option><option>Arial</option><option>Times New Roman</option></select>
                        </label>
                        <label>Dimensiune<input type="number" data-table-style="fontSize" min="8" max="72"></label>
                        <label>Culoare text<input type="color" data-table-style="color"></label>
                        <label>Culoare bordură<input type="color" data-table-style="borderColor"></label>
                        <label>Fundal antet<input type="color" data-table-style="headerBackground"></label>
                        <label>Aliniere
                            <select data-table-style="align"><option value="left">Stânga</option><option value="center">Centru</option><option value="right">Dreapta</option></select>
                        </label>
                    </div>
                    <label class="editor-checkbox-field"><input type="checkbox" data-table-style="bold"> Text îngroșat</label>
                </section>
                <section>
                    <h3>Conținut</h3>
                    <label class="editor-field">Etichetă<input type="text" data-prop="label" maxlength="120"></label>
                    <label class="editor-field" data-content-field="text">Text<textarea data-prop="text" rows="3" maxlength="500"></textarea></label>
                    <label class="editor-field" data-content-field="placeholder">Placeholder<input type="text" data-prop="placeholder" maxlength="500"></label>
                    <label class="editor-field" data-content-field="variable">Variabilă
                        <select data-prop="variable">
                            <option value="full_name">Nume complet</option>
                            <option value="date_of_birth">Data nașterii</option>
                            <option value="place_of_birth">Locul nașterii</option>
                            <option value="certificate_number">Număr certificat</option>
                        </select>
                    </label>
                </section>
                </div>
            </div>
        </aside>
    </div>

    <footer class="editor-statusbar">
        <span>▦ Grid <strong data-status="grid">1 mm / 10 mm</strong></span>
        <span>Zoom <strong data-status="zoom">75%</strong></span>
        <span>▤ <strong data-status="page">A4 landscape</strong></span>
        <span class="editor-save-status" data-status="save"><i></i><strong>Modificări salvate</strong></span>
    </footer>

    {{ layout|json_script:"diploma-layout-data" }}
    {{ media_assets|json_script:"diploma-media-assets-data" }}
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/template_renderer.js' %}" defer></script>
<script src="{% static 'diplome/template_editor.js' %}" defer></script>
{% endblock %}
```
