# apps/diplome/migrations/0002_millimeter_coordinate_system.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/migrations/0002_millimeter_coordinate_system.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `migration`
- Size: 6932 bytes
- Source SHA-256: `35eb7a3d939c54088e370a24e82224fd539cdebe3f900377119a73439f4de696`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from copy import deepcopy

from django.db import migrations, models
from django.db.models import Q


A4_MM = {"landscape": (297, 210), "portrait": (210, 297)}
A4_PX = {"landscape": (1123, 794), "portrait": (794, 1123)}


def _convert_elements(elements, source_width, source_height, target_width, target_height, source_keys, target_keys):
    converted_elements = []
    for source in elements:
        element = deepcopy(source)
        source_x, source_y, source_width_key, source_height_key = source_keys
        target_x, target_y, target_width_key, target_height_key = target_keys
        width = max(1, min(target_width, round(source[source_width_key] * target_width / source_width)))
        height = max(1, min(target_height, round(source[source_height_key] * target_height / source_height)))
        x = max(0, min(target_width - width, round(source[source_x] * target_width / source_width)))
        y = max(0, min(target_height - height, round(source[source_y] * target_height / source_height)))
        for key in source_keys:
            element.pop(key, None)
        element.update({target_x: x, target_y: y, target_width_key: width, target_height_key: height})
        if element.get("type") == "background":
            element.update({target_x: 0, target_y: 0, target_width_key: target_width, target_height_key: target_height})
        converted_elements.append(element)
    return converted_elements


def forwards(apps, schema_editor):
    DiplomaTemplate = apps.get_model("diplome", "DiplomaTemplate")
    for template in DiplomaTemplate.objects.all().iterator(chunk_size=200):
        orientation = template.orientation
        width_mm, height_mm = A4_MM[orientation]
        layout = deepcopy(template.layout_json or {})
        if layout.get("version") == 1:
            page = layout.get("page", {})
            width_px = page.get("width") or template.canvas_width_px
            height_px = page.get("height") or template.canvas_height_px
            layout = {
                "version": 2,
                "page": {
                    "size": "A4",
                    "orientation": orientation,
                    "width_mm": width_mm,
                    "height_mm": height_mm,
                    "grid_mm": 1,
                    "major_grid_mm": 10,
                    "background": None,
                },
                "elements": _convert_elements(
                    layout.get("elements", []),
                    width_px,
                    height_px,
                    width_mm,
                    height_mm,
                    ("x", "y", "width", "height"),
                    ("x_mm", "y_mm", "width_mm", "height_mm"),
                ),
            }
        template.page_width_mm = width_mm
        template.page_height_mm = height_mm
        template.grid_size_mm = 1
        template.major_grid_size_mm = 10
        template.layout_json = layout
        template.save(update_fields=(
            "page_width_mm",
            "page_height_mm",
            "grid_size_mm",
            "major_grid_size_mm",
            "layout_json",
        ))


def backwards(apps, schema_editor):
    DiplomaTemplate = apps.get_model("diplome", "DiplomaTemplate")
    for template in DiplomaTemplate.objects.all().iterator(chunk_size=200):
        orientation = template.orientation
        width_px, height_px = A4_PX[orientation]
        layout = deepcopy(template.layout_json or {})
        if layout.get("version") == 2:
            page = layout.get("page", {})
            width_mm = page.get("width_mm") or template.page_width_mm
            height_mm = page.get("height_mm") or template.page_height_mm
            layout = {
                "version": 1,
                "page": {
                    "size": "A4",
                    "orientation": orientation,
                    "width": width_px,
                    "height": height_px,
                    "gridSize": 10,
                    "background": None,
                },
                "elements": _convert_elements(
                    layout.get("elements", []),
                    width_mm,
                    height_mm,
                    width_px,
                    height_px,
                    ("x_mm", "y_mm", "width_mm", "height_mm"),
                    ("x", "y", "width", "height"),
                ),
            }
        template.canvas_width_px = width_px
        template.canvas_height_px = height_px
        template.grid_size_px = 10
        template.layout_json = layout
        template.save(update_fields=(
            "canvas_width_px",
            "canvas_height_px",
            "grid_size_px",
            "layout_json",
        ))


class Migration(migrations.Migration):
    dependencies = [("diplome", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="diplomatemplate",
            name="page_width_mm",
            field=models.PositiveSmallIntegerField(default=297),
        ),
        migrations.AddField(
            model_name="diplomatemplate",
            name="page_height_mm",
            field=models.PositiveSmallIntegerField(default=210),
        ),
        migrations.AddField(
            model_name="diplomatemplate",
            name="grid_size_mm",
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="diplomatemplate",
            name="major_grid_size_mm",
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveConstraint(model_name="diplomatemplate", name="dipl_tmpl_width_gt_0"),
        migrations.RemoveConstraint(model_name="diplomatemplate", name="dipl_tmpl_height_gt_0"),
        migrations.RemoveConstraint(model_name="diplomatemplate", name="dipl_tmpl_grid_gt_0"),
        migrations.RemoveField(model_name="diplomatemplate", name="canvas_width_px"),
        migrations.RemoveField(model_name="diplomatemplate", name="canvas_height_px"),
        migrations.RemoveField(model_name="diplomatemplate", name="grid_size_px"),
        migrations.AddConstraint(
            model_name="diplomatemplate",
            constraint=models.CheckConstraint(condition=Q(page_width_mm__gt=0), name="dipl_tmpl_width_mm_gt_0"),
        ),
        migrations.AddConstraint(
            model_name="diplomatemplate",
            constraint=models.CheckConstraint(condition=Q(page_height_mm__gt=0), name="dipl_tmpl_height_mm_gt_0"),
        ),
        migrations.AddConstraint(
            model_name="diplomatemplate",
            constraint=models.CheckConstraint(condition=Q(grid_size_mm__gt=0), name="dipl_tmpl_grid_mm_gt_0"),
        ),
        migrations.AddConstraint(
            model_name="diplomatemplate",
            constraint=models.CheckConstraint(condition=Q(major_grid_size_mm__gt=0), name="dipl_tmpl_major_grid_gt_0"),
        ),
    ]
```
