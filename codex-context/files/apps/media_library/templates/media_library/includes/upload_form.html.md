# Source snapshot

## `apps/media_library/templates/media_library/includes/upload_form.html`

Size: 1.5 KB

```html
<form
    method="post"
    enctype="multipart/form-data"
    class="space-y-4 border border-base-300 bg-base-100 p-5"
    hx-post="{% url 'media_library:index' %}"
    hx-target="#media-library-content"
    hx-swap="outerHTML"
    x-data="{ fileName: '', uploading: false }"
    x-on:submit="uploading = true"
>
    {% csrf_token %}
    <div>
        <h2 class="font-semibold text-base-content">Adaugă fișier</h2>
        <p class="mt-1 text-xs text-muted">SVG static sigur, PNG, JPG, JPEG sau WEBP. Maximum 10 MB.</p>
    </div>
    {% if form.non_field_errors %}<div class="alert alert-error py-2 text-sm">{{ form.non_field_errors }}</div>{% endif %}
    {% for field in form %}
        <label class="form-control w-full">
            <span class="label"><span class="label-text font-medium">{{ field.label }}</span></span>
            {% if field.name == "file" %}
                <div class="space-y-2">
                    {{ field }}
                    <p class="min-h-4 text-xs text-muted" x-text="fileName"></p>
                </div>
            {% else %}
                {{ field }}
            {% endif %}
            {% for error in field.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
    {% endfor %}
    <button type="submit" class="btn btn-primary btn-sm w-full" x-bind:disabled="!fileName || uploading">
        <span class="loading loading-spinner loading-xs" x-show="uploading" style="display: none;" aria-hidden="true"></span>
        Încarcă în bibliotecă
    </button>
</form>
```
