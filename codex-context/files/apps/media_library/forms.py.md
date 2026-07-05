# Source snapshot

## `apps/media_library/forms.py`

Size: 1.1 KB

```python
from pathlib import Path

from django import forms

from .validators import validate_and_prepare_media


class MediaAssetUploadForm(forms.Form):
    name = forms.CharField(
        max_length=160,
        required=False,
        label="Nume în bibliotecă",
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full", "placeholder": "Opțional"}),
    )
    file = forms.FileField(
        label="Fișier",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "file-input file-input-bordered w-full",
                "accept": ".svg,.png,.jpg,.jpeg,.webp,image/svg+xml,image/png,image/jpeg,image/webp",
            }
        ),
    )

    def clean_name(self):
        return " ".join(self.cleaned_data.get("name", "").split())

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        self.prepared_media = validate_and_prepare_media(uploaded_file)
        uploaded_file.seek(0)
        return uploaded_file

    def resolved_name(self) -> str:
        return self.cleaned_data["name"] or Path(self.cleaned_data["file"].name).stem[:160] or "Fișier media"
```
