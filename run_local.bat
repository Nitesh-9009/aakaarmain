@echo off
REM ============================================================
REM  Start the Aakaar website locally -> http://127.0.0.1:8000
REM
REM  * Uses local SQLite (db.sqlite3), no MySQL required
REM  * Uses aakaar_main.settings_local (plain HTTP, no HTTPS
REM    redirect) — production settings.py stays untouched
REM ============================================================
cd /d "%~dp0"
set DJANGO_SETTINGS_MODULE=aakaar_main.settings_local

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment and installing dependencies...
    python -m venv .venv
    ".venv\Scripts\python.exe" -m pip install --quiet -r requirements-local.txt
    if errorlevel 1 (
        echo Dependency installation failed.
        pause
        exit /b 1
    )
)

echo Applying database migrations...
".venv\Scripts\python.exe" manage.py migrate --noinput

REM Ensure a Google SocialApp exists so {% provider_login_url 'google' %}
REM templates render (no-op if one already exists). Local placeholder
REM credentials only — real Google sign-in needs real OAuth keys.
".venv\Scripts\python.exe" manage.py shell -c "from django.contrib.sites.models import Site; from allauth.socialaccount.models import SocialApp; s = Site.objects.get(pk=1); a, _ = SocialApp.objects.get_or_create(provider='google', defaults={'name': 'Google', 'client_id': 'LOCAL_DEV_PLACEHOLDER', 'secret': 'LOCAL_DEV_PLACEHOLDER'}); a.sites.add(s)"

echo Starting development server on http://127.0.0.1:8000 ...
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000

pause
