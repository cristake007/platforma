# theme/static_src/src/styles.css

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `theme/static_src/src/styles.css`
- App: none
- Role: `theme`
- Size: 30335 bytes
- Source SHA-256: `5095c859a977a678b4be83527e6a4071c4516a439bfd4696a8d9c7aec8086a51`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```css
@import "tailwindcss";
@source "../../../apps/flota/**/*.{html,py,js}";
@plugin "daisyui" {
    themes: false;
}
@plugin "daisyui/theme" {
    name: "tuvtk";
    default: true;
    prefersdark: false;
    color-scheme: light;

    --tuvtk-brand-primary: #164194;
    --tuvtk-brand-secondary: #d41131;
    --tuvtk-brand-accent: #7c8f9e;
    --tuvtk-page-bg: #ffffff;
    --tuvtk-panel-bg: #ffffff;
    --tuvtk-panel-muted-bg: #f7f9fb;
    --tuvtk-heading-text: #17212b;
    --tuvtk-body-text: #304253;
    --tuvtk-muted-text: #5d6b79;
    --tuvtk-border-default: #cfd7df;
    --tuvtk-border-hover: #b8c4cf;
    --tuvtk-control-hover-bg: #edf3f9;
    --tuvtk-primary-tint-bg: #dbe6ef;
    --tuvtk-primary-tint-border: #c9d9e6;
    --tuvtk-text-on-brand: #ffffff;

    --color-base-100: var(--tuvtk-panel-bg);
    --color-base-200: var(--tuvtk-panel-muted-bg);
    --color-base-300: var(--tuvtk-border-default);
    --color-base-content: var(--tuvtk-body-text);
    --color-primary: var(--tuvtk-brand-primary);
    --color-primary-content: var(--tuvtk-text-on-brand);
    --color-secondary: var(--tuvtk-brand-secondary);
    --color-secondary-content: var(--tuvtk-text-on-brand);
    --color-accent: var(--tuvtk-brand-accent);
    --color-accent-content: var(--tuvtk-heading-text);
    --color-neutral: var(--tuvtk-heading-text);
    --color-neutral-content: var(--tuvtk-text-on-brand);
    --color-info: #165d8d;
    --color-info-content: #ffffff;
    --color-success: #2f6f4e;
    --color-success-content: #ffffff;
    --color-warning: #8a5a00;
    --color-warning-content: #ffffff;
    --color-error: #b4233c;
    --color-error-content: #ffffff;

    --radius-selector: 0.5rem;
    --radius-field: 0.25rem;
    --radius-box: 0.5rem;
    --size-selector: 0.25rem;
    --size-field: 0.25rem;
    --border: 1px;
    --depth: 1;
    --noise: 0;

    --sidebar-bg: #ffffff;
    --sidebar-border: #d5dee7;
    --sidebar-heading-bg: #f1f5f8;
    --sidebar-heading-text: #52697d;
    --sidebar-heading-border: #d5dee7;
    --sidebar-heading-accent: var(--tuvtk-brand-primary);
    --sidebar-item-text: var(--tuvtk-brand-primary);
    --sidebar-item-icon: var(--tuvtk-brand-primary);
    --sidebar-item-hover-bg: #edf3f9;
    --sidebar-item-hover-text: var(--tuvtk-brand-secondary);
    --sidebar-item-hover-icon: var(--tuvtk-brand-secondary);
    --sidebar-item-hover-indicator: var(--tuvtk-brand-secondary);
    --sidebar-item-hover-indicator-width: 3px;
    --sidebar-item-hover-shift: 3px;
    --sidebar-item-pressed-bg: #d7e3ef;
    --sidebar-item-pressed-text: #0f3268;
    --sidebar-item-pressed-icon: #0f3268;
    --sidebar-item-current-bg: #e1eaf4;
    --sidebar-item-current-text: #123b77;
    --sidebar-item-current-icon: var(--tuvtk-brand-primary);
    --sidebar-item-current-indicator: var(--tuvtk-brand-secondary);
    --sidebar-child-guide: #c8d4df;
    --sidebar-child-text: #405d73;
    --sidebar-child-hover-bg: #edf3f9;
    --sidebar-child-hover-text: #123b77;
    --sidebar-child-current-bg: #dce7f2;
    --sidebar-child-current-text: #123b77;
    --sidebar-footer-bg: #ffffff;
    --sidebar-footer-border: #d5dee7;
    --sidebar-footer-divider: rgb(255 255 255 / 0.1);
    --sidebar-footer-heading-text: #223241;
    --sidebar-footer-text: #6b7a88;
    --sidebar-tooltip-bg: var(--tuvtk-brand-primary);
    --sidebar-tooltip-text: #ffffff;
    --scrollbar-thumb: var(--tuvtk-brand-primary);
    --scrollbar-track: transparent;
}

@source "../../../core/**/*.{html,py,js}";
@source "../../../apps/dashboard/**/*.{html,py,js}";
@source "../../../apps/planificator/**/*.{html,py,js}";
@source "../../../apps/diplome/**/*.{html,py,js}";
@source "../../../apps/media_library/**/*.{html,py,js}";
@source "../../../apps/tasks/**/*.{html,py,js}";
@source "../../static/**/*.js";

@font-face {
    font-family: "InterVariable";
    font-style: normal;
    font-weight: 100 900;
    font-display: swap;
    src: url("../../fonts/inter/InterVariable.woff2") format("woff2");
}

@theme inline {
    --font-sans: "InterVariable", "Inter", "Segoe UI", sans-serif;
    --color-muted: var(--tuvtk-muted-text);
}

@layer base {
    html,
    body {
        font-family: var(--font-sans);
        font-optical-sizing: auto;
    }

    body {
        background: var(--color-base-100);
        color: var(--color-base-content);
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: var(--tuvtk-heading-text);
    }

    :focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }
}

@layer components {
    .dropdown-content {
        border-radius: 0.65rem;
        box-shadow: none;
    }

    .ops-shell {
        background: var(--color-base-100);
    }

    .ops-topbar {
        height: 4rem;
        border-bottom: 1px solid var(--color-primary);
        background: var(--color-base-100);
    }

    .ops-logo {
        width: 3.5rem;
        height: 3.5rem;
        flex: none;
        object-fit: contain;
    }

    .ops-header-chip {
        align-items: center;
        gap: 0.45rem;
        border: 1px solid var(--color-base-300);
        border-radius: 0.45rem;
        background: var(--color-base-100);
        padding: 0.45rem 0.65rem;
        color: var(--tuvtk-muted-text);
        font-size: 0.75rem;
        font-weight: 600;
    }

    .ops-sidebar-toggle {
        display: inline-flex;
        width: 2.75rem;
        height: 2.75rem;
        min-height: 2.75rem;
        flex: none;
        cursor: pointer;
        align-items: center;
        justify-content: center;
        border: 1px solid var(--color-base-300);
        border-radius: var(--radius-field);
        background: var(--color-base-100);
        color: var(--color-primary);
        transition: border-color 150ms ease, background-color 150ms ease, color 150ms ease;
    }

    .ops-sidebar-toggle:hover {
        border-color: var(--tuvtk-border-hover);
        background: var(--tuvtk-control-hover-bg);
        color: var(--color-secondary);
    }

    .ops-user-trigger {
        display: inline-flex;
        align-items: center;
        cursor: pointer;
        border: 1px solid var(--color-base-300);
        border-radius: 9999px;
        background: var(--color-base-100);
        padding: 0.3rem;
        color: var(--sidebar-item-text);
        list-style: none;
        transition: border-color 160ms ease, background-color 160ms ease, color 160ms ease;
    }

    .ops-user-trigger::-webkit-details-marker {
        display: none;
    }

    .ops-user-trigger:hover,
    .ops-user-trigger:focus-visible,
    .ops-user-flyout[open] > .ops-user-trigger {
        border-color: var(--tuvtk-border-hover);
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
    }

    .ops-avatar-frame {
        display: inline-grid;
        padding: 0.15rem;
        place-items: center;
        border: 1px solid var(--sidebar-border);
        border-radius: 9999px;
        background: var(--color-base-100);
        transition: border-color 160ms ease, transform 160ms ease;
    }

    .ops-user-trigger:hover .ops-avatar-frame,
    .ops-user-trigger:focus-visible .ops-avatar-frame,
    .ops-user-flyout[open] > .ops-user-trigger .ops-avatar-frame {
        border-color: var(--sidebar-item-hover-indicator);
        transform: scale(1.03);
    }

    .ops-avatar {
        display: grid;
        width: 2.4rem;
        height: 2.4rem;
        flex: none;
        place-items: center;
        overflow: hidden;
        border-radius: 9999px;
        background: var(--color-primary);
        color: var(--color-primary-content);
        font-size: 0.8125rem;
        font-weight: 800;
        letter-spacing: 0.04em;
    }

    .ops-avatar-status {
        position: absolute;
        right: -0.05rem;
        bottom: -0.05rem;
        width: 0.7rem;
        height: 0.7rem;
        border: 2px solid var(--color-base-100);
        border-radius: 9999px;
        background: var(--color-success);
    }

    .ops-title {
        color: var(--color-primary);
        letter-spacing: -0.025em;
    }

    .generator-step-card {
        overflow: hidden;
        border: 1px solid var(--tuvtk-border-hover);
        border-top: 4px solid var(--color-secondary);
        border-radius: 0;
        transition: opacity 180ms ease;
    }

    .card.generator-step-card {
        border-radius: 0 !important;
    }

    .generator-card-header {
        border-bottom: 1px solid var(--tuvtk-border-hover);
    }

    .generator-card-step .steps,
    .generator-card-step .step,
    .generator-card-step-copy {
        width: 100%;
        min-width: 0;
    }

    .generator-card-step .steps {
        overflow: visible;
    }

    .generator-card-step .step {
        min-height: 3.5rem;
        text-align: left;
    }

    .generator-card-step-copy {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        padding-block: 0.45rem;
    }

    .generator-card-step-copy .card-title {
        display: block;
        width: 100%;
        line-height: 1.25;
    }

    .generator-step-card.generator-card-complete {
        opacity: 0.64;
    }

    .ops-schedule-table thead th {
        position: sticky !important;
        top: 0 !important;
    }

    .ops-word-match-scroll {
        max-height: 36rem;
        overscroll-behavior-inline: contain;
        scrollbar-gutter: stable;
        scrollbar-width: auto;
    }

    .ops-word-match-scroll::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    .ops-word-match-scroll::-webkit-scrollbar-track {
        background: var(--scrollbar-track);
        border-top: 1px solid var(--tuvtk-border-default);
    }

    .ops-word-match-scroll::-webkit-scrollbar-thumb {
        border: 2px solid var(--scrollbar-track);
        border-radius: 9999px;
        background: var(--scrollbar-thumb);
    }

    .ops-word-match-table {
        width: 73.75rem;
        min-width: 73.75rem;
        table-layout: fixed;
    }

    .ops-word-match-table :where(th, td) {
        overflow-wrap: anywhere;
        white-space: normal;
        vertical-align: top;
    }

    .ops-course-updater-top-scroll {
        overflow-x: auto;
        overflow-y: hidden;
        height: 0.75rem;
        margin-bottom: 0.25rem;
        scrollbar-width: auto;
    }

    .ops-course-updater-top-scroll > div {
        height: 1px;
    }

    .ops-course-updater-scroll {
        max-height: 38rem;
        overflow: auto;
        overscroll-behavior-inline: contain;
        scrollbar-gutter: stable;
    }

    .ops-course-updater-table {
        width: 72.5rem;
        min-width: 72.5rem;
        table-layout: fixed;
    }

    .ops-course-updater-table thead th {
        position: sticky;
        top: 0;
        z-index: 10;
        background: var(--color-base-200);
    }

    .ops-course-updater-table :where(th, td) {
        overflow-wrap: anywhere;
        padding: 0.45rem 0.5rem;
        white-space: normal;
        vertical-align: top !important;
    }

    .ops-word-match-table thead th {
        position: sticky;
        top: 0;
        z-index: 5;
        background: var(--color-base-200);
    }

    .ops-word-match-course {
        text-align: center !important;
        vertical-align: middle !important;
    }

    .ops-word-match-periods {
        text-align: center !important;
        vertical-align: middle !important;
    }

    .ops-word-select-clip {
        overflow: hidden;
        border-radius: var(--radius-field);
    }

    .ops-word-match-table select {
        display: block;
        width: 100%;
        min-width: 0;
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    @media (max-width: 639px) {
        .ops-word-match-scroll {
            max-height: 26rem;
        }
    }

    .ops-schedule-course-column {
        position: sticky !important;
        left: 0 !important;
        width: var(--course-width) !important;
        min-width: var(--course-width) !important;
        max-width: var(--course-width) !important;
    }

    .ops-schedule-duration-column {
        position: sticky !important;
        left: var(--course-width) !important;
        width: var(--duration-width) !important;
        min-width: var(--duration-width) !important;
        max-width: var(--duration-width) !important;
    }

    .ops-schedule-investment-column {
        position: sticky !important;
        left: calc(var(--course-width) + var(--duration-width)) !important;
        width: var(--investment-width) !important;
        min-width: var(--investment-width) !important;
        max-width: var(--investment-width) !important;
    }

    .ops-sidebar {
        border-right: 1px solid var(--sidebar-border);
        background: var(--sidebar-bg);
        color: var(--sidebar-item-text);
    }

    .ops-sidebar-nav {
        scrollbar-width: thin;
        scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
    }

    .ops-sidebar-nav::-webkit-scrollbar,
    .ops-scrollbar::-webkit-scrollbar {
        width: 4px;
        height: 4px;
    }

    .ops-sidebar-nav::-webkit-scrollbar-track,
    .ops-scrollbar::-webkit-scrollbar-track {
        background: var(--scrollbar-track);
    }

    .ops-sidebar-nav::-webkit-scrollbar-thumb,
    .ops-scrollbar::-webkit-scrollbar-thumb {
        border-radius: 9999px;
        background: var(--scrollbar-thumb);
    }

    .ops-sidebar-heading {
        border-block: 1px solid var(--sidebar-heading-border);
        border-left: 3px solid var(--sidebar-heading-accent);
        background: var(--sidebar-heading-bg);
        padding-block: 0.48rem;
        color: var(--sidebar-heading-text);
    }

    .ops-sidebar-nav ul.menu {
        display: flex;
        width: 100%;
        flex-flow: column nowrap;
        align-items: stretch;
    }

    .ops-sidebar-nav ul.menu > li,
    .ops-sidebar-nav ul.menu > li > details {
        width: 100%;
    }

    .ops-sidebar-nav ul.menu > li > a,
    .ops-sidebar-nav ul.menu > li > details > summary {
        display: flex;
        width: 100%;
        min-height: 2.45rem;
        cursor: pointer;
        align-items: center;
        justify-content: flex-start;
        border-radius: 0;
        padding-inline: 1rem;
        color: var(--sidebar-item-text);
        text-align: left;
    }

    .ops-sidebar-nav ul.menu > li > details > summary::after {
        display: none;
    }

    .ops-sidebar-nav ul.menu > li > a:hover,
    .ops-sidebar-nav ul.menu > li > details > summary:hover {
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
        box-shadow: inset 3px 0 var(--sidebar-item-current-indicator);
    }

    .ops-sidebar-nav ul.menu > li > a.active {
        background: var(--sidebar-item-current-bg);
        color: var(--sidebar-item-current-text);
        box-shadow: inset 3px 0 var(--sidebar-item-current-indicator);
    }

    .ops-nav-icon {
        display: inline-flex;
        flex: none;
        align-items: center;
        justify-content: center;
    }

    .ops-nav-glyph,
    .ops-nav-chevron {
        width: 1rem;
        height: 1rem;
        flex: none;
        color: inherit;
    }

    .ops-nav-chevron {
        margin-left: auto;
        transition: transform 150ms ease;
    }

    details[open] > summary .ops-nav-chevron {
        transform: rotate(90deg);
    }

    .ops-sidebar-nav ul.ops-submenu {
        width: 100%;
        margin: 0;
        padding: 0.2rem 0 0.35rem;
    }

    .ops-sidebar-nav ul.ops-submenu::before {
        background: var(--sidebar-child-guide);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a {
        min-height: 2rem;
        padding-left: 3rem;
        color: var(--sidebar-child-text);
        font-size: 0.8125rem;
    }

    .ops-sidebar-nav ul.ops-submenu > li > a:hover {
        background: var(--sidebar-child-hover-bg);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a.active {
        background: var(--sidebar-child-current-bg);
        color: var(--sidebar-item-current-text);
    }

    .ops-sidebar-note {
        border: 1px solid var(--sidebar-footer-border);
        border-radius: 0.6rem;
        background: var(--sidebar-footer-bg);
    }

}

/* Sidebar rules share daisyUI's utility layer so its menu defaults cannot
   flatten the established expanded/collapsed navigation treatment. */
@layer utilities {
    .ops-user-flyout > .ops-user-menu {
        border-color: var(--sidebar-border);
        border-radius: 0;
        background: var(--sidebar-bg);
        box-shadow: none;
        color: var(--sidebar-child-text);
        opacity: 0;
        pointer-events: none;
        transform: translateY(-0.35rem) scale(0.98);
        transform-origin: right top;
        transition: opacity 160ms ease, transform 160ms ease;
        visibility: hidden;
    }

    .ops-user-flyout.is-flyout-active > .ops-user-menu {
        opacity: 1;
        pointer-events: auto;
        transform: translateY(0) scale(1);
        visibility: visible;
    }

    .ops-user-flyout.is-flyout-active.is-flyout-preparing > .ops-user-menu,
    .ops-user-flyout.is-flyout-active.is-flyout-closing > .ops-user-menu {
        opacity: 0;
        pointer-events: none;
        transform: translateY(-0.35rem) scale(0.98);
    }

    .ops-user-menu.menu > li > a,
    .ops-user-menu.menu > li > form > button {
        display: flex;
        width: 100%;
        min-height: 2.75rem;
        align-items: center;
        gap: 0.7rem;
        border-radius: 0;
        background: transparent;
        box-shadow: inset 0 0 var(--sidebar-item-hover-indicator);
        padding: 0.6rem 0.85rem;
        color: var(--sidebar-child-text);
        font-size: 0.875rem;
        text-align: left;
        transition: color 180ms ease, background-color 180ms ease, box-shadow 180ms ease;
    }

    .ops-user-menu.menu > li > form {
        display: block;
        width: 100%;
        margin: 0;
        border-radius: 0;
        background: transparent !important;
        padding: 0;
    }

    .ops-user-menu.menu > li > form:hover,
    .ops-user-menu.menu > li > form:focus-within {
        background: transparent !important;
    }

    .ops-user-menu.menu > li.ops-user-logout,
    .ops-user-menu.menu > li.ops-user-logout:hover,
    .ops-user-menu.menu > li.ops-user-logout:focus-within,
    .ops-user-menu.menu > li.ops-user-logout > form,
    .ops-user-menu.menu > li.ops-user-logout > form:hover,
    .ops-user-menu.menu > li.ops-user-logout > form:focus-within,
    .ops-user-menu.menu > li.ops-user-logout > form > button:hover,
    .ops-user-menu.menu > li.ops-user-logout > form > button:focus-visible {
        background: transparent !important;
        background-image: none !important;
    }

    .ops-user-menu.menu > li > a:hover,
    .ops-user-menu.menu > li > a:focus-visible,
    .ops-user-menu.menu > li > form > button:hover,
    .ops-user-menu.menu > li > form > button:focus-visible {
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
        box-shadow: inset var(--sidebar-item-hover-indicator-width) 0 var(--sidebar-item-hover-indicator);
    }

    .ops-user-menu-icon {
        display: grid;
        width: 1.25rem;
        height: 1.25rem;
        flex: none;
        place-items: center;
        color: var(--sidebar-item-icon);
        transition: color 180ms ease, transform 180ms ease;
    }

    .ops-user-menu-icon > svg {
        width: 100%;
        height: 100%;
    }

    .ops-user-menu-label {
        transition: transform 180ms ease;
    }

    .ops-user-menu.menu > li > a:hover .ops-user-menu-icon,
    .ops-user-menu.menu > li > a:focus-visible .ops-user-menu-icon,
    .ops-user-menu.menu > li > form > button:hover .ops-user-menu-icon,
    .ops-user-menu.menu > li > form > button:focus-visible .ops-user-menu-icon {
        color: var(--sidebar-item-hover-icon);
        transform: translateX(var(--sidebar-item-hover-shift));
    }

    .ops-user-menu.menu > li > a:hover .ops-user-menu-label,
    .ops-user-menu.menu > li > a:focus-visible .ops-user-menu-label,
    .ops-user-menu.menu > li > form > button:hover .ops-user-menu-label,
    .ops-user-menu.menu > li > form > button:focus-visible .ops-user-menu-label {
        transform: translateX(var(--sidebar-item-hover-shift));
    }

    .drawer-side .ops-sidebar,
    .ops-sidebar-nav {
        background-color: var(--sidebar-bg);
    }

    .ops-sidebar-nav ul.menu {
        display: flex;
        width: 100%;
        flex-flow: column nowrap;
        align-items: stretch;
    }

    .ops-sidebar-nav ul.menu > li {
        display: flex;
        width: 100%;
        max-width: none;
        flex-flow: column nowrap;
        align-self: stretch;
    }

    .ops-sidebar-nav ul.menu > li > details {
        width: 100%;
    }

    .ops-sidebar-nav ul.menu > li > details > summary,
    .ops-sidebar-nav ul.menu > li > a {
        display: flex;
        width: 100%;
        max-width: none;
        cursor: pointer;
        align-items: center;
        justify-content: flex-start;
        color: var(--sidebar-item-text);
        text-align: left;
    }

    .ops-sidebar-nav ul.menu > li > details > summary::after {
        display: none;
    }

    .ops-sidebar-nav ul.menu > li > details > summary:hover,
    .ops-sidebar-nav ul.menu > li > a:hover {
        background: var(--sidebar-item-hover-bg);
        color: var(--sidebar-item-hover-text);
    }

    .ops-sidebar-nav ul.menu > li > details > summary:hover svg,
    .ops-sidebar-nav ul.menu > li > a:hover svg {
        color: var(--sidebar-item-hover-icon);
    }

    .ops-sidebar-nav ul.menu > li > details > summary:active,
    .ops-sidebar-nav ul.menu > li > a:active {
        background: var(--sidebar-item-pressed-bg);
        color: var(--sidebar-item-pressed-text);
    }

    .ops-sidebar-nav ul.menu > li > details > summary:active svg,
    .ops-sidebar-nav ul.menu > li > a:active svg {
        color: var(--sidebar-item-pressed-icon);
    }

    .ops-sidebar-nav ul.menu > li > a.active {
        background: var(--sidebar-item-current-bg);
        color: var(--sidebar-item-current-text);
    }

    .ops-sidebar-nav ul.menu > li > a.active svg {
        color: var(--sidebar-item-current-icon);
    }

    .ops-sidebar-nav ul.ops-submenu {
        width: 100%;
        margin: 0;
        padding: 0.2rem 0 0.35rem;
    }

    .ops-sidebar-nav ul.ops-submenu::before {
        background: var(--sidebar-child-guide);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a {
        min-height: 2rem;
        padding-left: 3rem;
        color: var(--sidebar-child-text);
        font-size: 0.8125rem;
    }

    .ops-sidebar-nav ul.ops-submenu > li > a:hover {
        background: var(--sidebar-child-hover-bg);
        color: var(--sidebar-child-hover-text);
    }

    .ops-sidebar-nav ul.ops-submenu > li > a.active {
        background: var(--sidebar-child-current-bg);
        color: var(--sidebar-child-current-text);
    }

}

.drawer-toggle:not(:checked) ~ .drawer-side,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav,
.drawer-toggle:checked ~ .drawer-side:has(.ops-sidebar) {
    overflow: visible;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav > div,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav section,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav details {
    width: 100%;
    max-width: 100%;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav details {
    margin: 0;
    padding: 0;
    overflow: visible;
    background: transparent;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > a,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary {
    display: flex;
    width: 100%;
    min-width: 0;
    max-width: 100%;
    margin: 0;
    justify-content: center;
    gap: 0;
    padding-inline: 0;
    box-sizing: border-box;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > details:hover,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.menu > li > details:focus-within {
    background: transparent;
}

@media (min-width: 1024px) {
    .drawer > .drawer-toggle ~ .drawer-side > .drawer-overlay {
        display: none;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group {
        position: relative;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group > .ops-submenu {
        position: absolute;
        z-index: 110;
        top: 0;
        left: calc(100% + 0.45rem);
        display: block;
        width: 14rem;
        margin: 0;
        border: 1px solid var(--sidebar-border);
        border-radius: 0;
        background: var(--sidebar-bg);
        box-shadow: none;
        opacity: 0;
        padding: 0;
        pointer-events: none;
        transform: translateX(-0.35rem) scale(0.98);
        transform-origin: left top;
        transition: opacity 160ms ease, transform 160ms ease;
        visibility: hidden;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group > .ops-submenu::after {
        position: absolute;
        top: 0;
        right: 100%;
        width: 0.5rem;
        height: 100%;
        content: "";
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group.is-flyout-active > .ops-submenu {
        opacity: 1;
        pointer-events: auto;
        transform: translateX(0) scale(1);
        visibility: visible;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group.is-flyout-active.is-flyout-preparing > .ops-submenu,
    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group.is-flyout-active.is-flyout-closing > .ops-submenu {
        opacity: 0;
        pointer-events: none;
        transform: translateX(-0.35rem) scale(0.98);
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group[open] > summary[data-tip]::before,
    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav .ops-nav-group[open] > summary[data-tip]::after {
        display: none;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a {
        min-height: 2.25rem;
        padding-inline: 0.85rem;
        box-shadow: inset 0 0 var(--sidebar-item-hover-indicator);
        transition: color 180ms ease, background-color 180ms ease, box-shadow 180ms ease;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a > .ops-submenu-label {
        transition: transform 180ms ease;
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a:hover,
    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a:focus-visible {
        color: var(--sidebar-item-hover-text);
        box-shadow: inset var(--sidebar-item-hover-indicator-width) 0 var(--sidebar-item-hover-indicator);
    }

    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a:hover > .ops-submenu-label,
    .drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav ul.ops-submenu > li > a:focus-visible > .ops-submenu-label {
        transform: translateX(var(--sidebar-item-hover-shift));
    }
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip] {
    --tt-bg: var(--sidebar-tooltip-bg);
    overflow: visible;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]::before {
    color: var(--sidebar-tooltip-text);
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]:hover,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]:focus-visible {
    z-index: 100;
}

.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]::before,
.drawer-toggle:not(:checked) ~ .drawer-side .ops-sidebar-nav [data-tip]::after {
    z-index: 101;
}

.ops-sidebar-nav ul.menu a,
.ops-sidebar-nav ul.menu summary {
    border-radius: 0;
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary {
    box-shadow: inset 0 0 var(--sidebar-item-hover-indicator);
    transition: color 180ms ease, background-color 180ms ease, box-shadow 180ms ease;
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a:hover,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary:hover {
    box-shadow: inset var(--sidebar-item-hover-indicator-width) 0 var(--sidebar-item-hover-indicator);
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a.active {
    box-shadow: inset 3px 0 var(--sidebar-item-current-indicator);
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a > .ops-nav-icon,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a > span:last-child,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary > .ops-nav-icon,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary > span:not(.ops-nav-icon) {
    transition: transform 180ms ease;
}

.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a:hover > .ops-nav-icon,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > a:hover > span:last-child,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary:hover > .ops-nav-icon,
.drawer-toggle:checked ~ .drawer-side .ops-sidebar-nav ul.menu > li > details > summary:hover > span:not(.ops-nav-icon) {
    transform: translateX(var(--sidebar-item-hover-shift));
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
    }
}
```
