"""
Local development settings — run the site on this machine without MySQL or TLS.

Production keeps using aakaar_main.settings (MySQL + forced HTTPS).
Local usage:

    DJANGO_SETTINGS_MODULE=aakaar_main.settings_local python manage.py runserver

or just run run_local.bat.
"""

import os

# Inherit everything from the main settings (apps on sys.path, templates,
# static files, INSTALLED_APPS, ...).
from aakaar_main.settings import *  # noqa: F401,F403

# settings.py pulls the secret key from the environment; provide an offline
# fallback so the site boots without it. Local use only — production must set
# DJANGO_SECRET_KEY.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or 'django-insecure-local-development-only-key'

# Local SQLite database instead of the production MySQL server.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# The production settings force HTTPS (SSL redirect, secure cookies, HSTS),
# which cannot work on plain http://127.0.0.1:8000.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Local origins allowed to POST (login, signup, admin forms).
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
