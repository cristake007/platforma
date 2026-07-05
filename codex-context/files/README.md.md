# README.md

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `README.md`
- App: none
- Role: `docs`
- Size: 7633 bytes
- Source SHA-256: `c3fe2818b4df619a8abf0b7579288596e63a40e8e156ee194fa66d6279d2a8ec`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

````markdown
# Platforma TUVTK

Aplicație Django locală pentru instrumentele operaționale TUVTK. Proiectul folosește PostgreSQL, Tailwind CSS și daisyUI.

## Cerințe locale

- Python 3.12
- Node.js 22 sau o versiune LTS compatibilă
- PostgreSQL local; scripturile incluse folosesc distribuția din `.postgresql/`
- PowerShell pe Windows

## Instalare

1. Creează mediul virtual: `python -m venv .venv`.
2. Activează-l cu `.venv\Scripts\Activate.ps1` sau `activate_venv.bat`.
3. Instalează pachetele Python: `pip install -r requirements-dev.txt`.
4. Instalează pachetele frontend: `cd theme\static_src` și `npm ci`.
5. Copiază `.env.example` în `.env` și ajustează valorile PostgreSQL locale.
6. Pornește PostgreSQL cu `start_postgres.bat`.
7. Aplică migrările: `python manage.py migrate`.
8. Construiește CSS: `python manage.py tailwind build`.

## Utilizatori și permisiuni

Planificatorul necesită permisiunea `planificator.use_course_planning`. Creează un superutilizator cu `python manage.py createsuperuser`, apoi acordă permisiunea utilizatorilor din Django Admin.

## Rulare

Pentru a verifica local paginile de eroare custom, ruleaza `runserver.bat --debug=false --insecure`, apoi deschide o ruta inexistenta precum `/test`.
Pentru modul local normal, ruleaza `runserver.bat` sau `runserver.bat --debug=true`.

- `runserver.bat` pornește baza locală dacă este necesar, aplică migrările, pornește watcher-ul Tailwind și serverul Django.
- `runserver.ps1` pornește serverul Django și watcher-ul când mediul este deja pregătit.
- `watch_tailwind.ps1` reconstruiește CSS când se schimbă sursele aplicației.
- `start_postgres.bat` și `stop_postgres.bat` controlează instanța PostgreSQL locală.
- `activate_venv.bat` deschide un PowerShell cu mediul Python și Node local în PATH.

## Variabile `.env`

- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `POSTGRES_HOST`, `POSTGRES_PORT`
- `POSTGRES_CONN_MAX_AGE`, `POSTGRES_CONN_HEALTH_CHECKS`
- `DJANGO_DEBUG` (`true` local; set `false` to preview production error pages)
- `DJANGO_ALLOWED_HOSTS` (comma-separated hosts, for example `127.0.0.1,localhost`)
- opțional `NPM_BIN_PATH` pentru o instalare Node neobișnuită

Fișierul `.env` este local și nu trebuie distribuit.

## Verificare

```powershell
python manage.py makemigrations --check --dry-run
python manage.py check
python -m pylint --errors-only apps core platforma_tuvtk manage.py
python manage.py test
python manage.py tailwind build
python manage.py purge_expired_schedule_generations
pip check
cd theme\static_src
npm audit
```

## Repomix

Instalează instrumentele din rădăcina proiectului cu `npm ci`, apoi generează
contextul repository-ului cu:

```powershell
npm run repomix
```

Rezultatul este scris în `repomix-output.xml`. Configurația exclude mediile
locale, dependențele, cache-urile și fișierele generate.

Planificatorul acceptă fișiere CSV UTF-8 și XLSX cu coloanele `Title`, `Durata Curs`, `Permalink` și opțional `investitie`.

## Instalare Linux cu Docker

Deployment-ul Docker este destinat Debian/Ubuntu pe `amd64` sau `arm64`. Acesta
instalează Docker Engine și pluginul Compose din repository-ul oficial Docker,
clonează proiectul, construiește CSS-ul, aplică migrările și pornește PostgreSQL,
Gunicorn și Nginx.

Pe un server nou, înlocuiește `PUBLIC_IP` cu adresa publică stabilă a serverului:

```bash
curl -fsSL https://raw.githubusercontent.com/cristake007/platforma/main/install.sh \
  | sudo bash -s -- \
      --repo-url https://github.com/cristake007/platforma.git \
      --ref main \
      --public-host PUBLIC_IP
```

Pentru instalări reproductibile, înlocuiește `main` din ambele URL-uri cu același
tag de release. Scriptul poate fi rulat din nou pentru update. El refuză să
suprascrie un checkout cu modificări locale și păstrează secretele și datele
existente.

Locațiile implicite sunt:

- cod: `/opt/tuvtk/app`;
- configurație și secrete: `/etc/tuvtk/tuvtk.env`;
- PostgreSQL și fișiere persistente: `/var/lib/tuvtk`.

Portul PostgreSQL nu este publicat. Nginx publică doar fișierele statice,
avatarurile și emblemele flotei. Biblioteca media privată și diplomele generate
rămân accesibile numai prin view-urile Django autentificate.

### Repository privat

Installer-ul nu acceptă token-uri în argumente. Pentru un repository SSH privat,
creează pe server o cheie deploy read-only, adaugă cheia publică în GitHub și
adaugă cheia host GitHub verificată în `/etc/ssh/ssh_known_hosts`. Apoi rulează:

```bash
curl -fsSL https://raw.githubusercontent.com/cristake007/platforma/main/install.sh \
  | sudo bash -s -- \
      --repo-url git@github.com:cristake007/platforma.git \
      --ssh-key /root/.ssh/platforma_deploy \
      --ref main \
      --public-host PUBLIC_IP
```

Bootstrap-ul trebuie să rămână disponibil public chiar dacă repository-ul sursă
devine privat.

### Operare

Comenzile de mai jos folosesc configurația persistentă a installer-ului:

```bash
sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml \
  exec web python manage.py createsuperuser

sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml \
  logs --follow web nginx
```

Backup PostgreSQL și fișiere încărcate:

```bash
sudo install -d -m 0700 /var/backups/tuvtk
sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml \
  exec -T db pg_dump -U tuvtk -d platforma_tuvtk -Fc \
  > /var/backups/tuvtk/database.dump
sudo tar -C /var/lib/tuvtk -czf /var/backups/tuvtk/files.tar.gz media private-media
```

Restaurarea trebuie făcută cu serviciul web oprit și după salvarea stării
curente. Pentru o bază de date inițializată:

```bash
sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml \
  stop web nginx
sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml \
  exec -T db pg_restore --clean --if-exists -U tuvtk -d platforma_tuvtk \
  < /var/backups/tuvtk/database.dump
sudo tar -C /var/lib/tuvtk -xzf /var/backups/tuvtk/files.tar.gz
```

Pentru a opri și elimina containerele fără a șterge datele:

```bash
sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml down
```

Nu șterge `/var/lib/tuvtk` sau `/etc/tuvtk` dacă datele și secretele trebuie
păstrate. Persistența nu înlocuiește backup-urile testate.

### Limitare HTTP temporară

Configurația curentă publică aplicația pe portul 80 fără TLS. Credentialele,
cookie-urile de sesiune și datele sunt necriptate în tranzit. Acest mod este doar
pentru dezvoltare temporară. Înainte de producție trebuie configurat HTTPS, apoi
activate `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_SESSION_COOKIE_SECURE` și
`DJANGO_CSRF_COOKIE_SECURE`, iar originea CSRF trebuie schimbată la `https://`.

### Verificare focalizată

```bash
sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml \
  exec web python manage.py check
```

Testul focalizat pentru randarea diplomelor se rulează manual, deoarece creează
o bază de date de test:

```bash
sudo docker compose --env-file /etc/tuvtk/tuvtk.env \
  --project-directory /opt/tuvtk/app -f /opt/tuvtk/app/compose.yaml \
  exec web python manage.py test apps.diplome.tests_generation -v 0
```
````
