# Source snapshot

## `apps/diplome/static/diplome/template_preview.js`

Size: 1.4 KB

```javascript
(function () {
    "use strict";

    const root = document.getElementById("diploma-preview")
        || document.getElementById("generation-diploma-preview");
    if (!root || !window.DiplomaRenderer) return;

    const layout = JSON.parse(document.getElementById("diploma-layout-data").textContent);
    const sampleData = JSON.parse(document.getElementById("diploma-sample-data").textContent);
    const assetsNode = document.getElementById("diploma-media-assets-data");
    const assets = new Map(
        (assetsNode ? JSON.parse(assetsNode.textContent) : []).map((asset) => [asset.id, asset]),
    );
    const canvas = document.getElementById("preview-canvas");
    const frame = document.getElementById("preview-canvas-frame");
    const workspace = root.querySelector(".preview-workspace");

    window.DiplomaRenderer.render(canvas, layout, { editable: false, sampleData, assets });

    function fitPreview() {
        const pageSize = window.DiplomaRenderer.pagePixelSize(layout);
        const available = Math.max(320, workspace.clientWidth - 64);
        const scale = Math.min(1, available / pageSize.width);
        canvas.style.transform = `scale(${scale})`;
        canvas.style.transformOrigin = "top left";
        frame.style.width = `${pageSize.width * scale}px`;
        frame.style.height = `${pageSize.height * scale}px`;
    }

    fitPreview();
    window.addEventListener("resize", fitPreview);
})();
```
