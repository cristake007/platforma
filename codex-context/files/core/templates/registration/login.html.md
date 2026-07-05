# Source snapshot

## `core/templates/registration/login.html`

Size: 2.5 KB

```html
{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="ro" data-theme="tuvtk">
<head>
    <title>Loghează-te | Platforma TUVTK</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preload" href="{% static 'fonts/inter/InterVariable.woff2' %}" as="font" type="font/woff2" crossorigin>
    {% tailwind_css %}
</head>
<body class="min-h-dvh bg-base-200 text-base-content">
    <main class="hero min-h-dvh px-4 py-10">
        <section class="hero-content w-full max-w-md p-0">
            <div class="card card-border w-full bg-base-100 shadow-xl">
                <div class="card-body gap-5 p-8 sm:p-10">
                    <div class="flex flex-col items-center text-center">
                        <img src="{% static 'images/logo.svg' %}" class="h-24 w-24 object-contain sm:h-28 sm:w-28" alt="Platforma TUVTK logo">
                        <h1 class="mt-3 text-xl font-bold">Platforma TUVTK</h1>
                        <p class="text-xs uppercase tracking-[0.16em] text-muted">Internal operations</p>
                    </div>

                    <div class="divider my-0"></div>
                    <div>
                        <h2 class="text-2xl font-bold">Loghează-te</h2>
                        <p class="mt-1 text-sm text-muted">Folosește contul tău pentru a continua.</p>
                    </div>

            {% if form.errors %}
                <div class="alert alert-error text-sm" role="alert">
                    Numele de utilizator sau parola nu au fost acceptate.
                </div>
            {% endif %}

            <form method="post" class="space-y-4">
                {% csrf_token %}
                <input type="hidden" name="next" value="{{ next }}">
                <fieldset class="fieldset">
                    <legend class="fieldset-legend">Utilizator</legend>
                    <input type="text" name="username" value="{{ form.username.value|default:'' }}" autocomplete="username" autofocus required class="input input-primary w-full">
                </fieldset>
                <fieldset class="fieldset">
                    <legend class="fieldset-legend">Parolă</legend>
                    <input type="password" name="password" autocomplete="current-password" required class="input input-primary w-full">
                </fieldset>
                <button type="submit" class="btn btn-primary w-full">Loghează-te</button>
            </form>
                </div>
            </div>
        </section>
    </main>
</body>
</html>
```
