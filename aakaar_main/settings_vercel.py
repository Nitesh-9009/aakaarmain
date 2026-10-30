"""Settings for running the site on Vercel (serverless).

Vercel gives each request a throw-away filesystem and no always-on MySQL, so
this module differs from ``aakaar_main.settings`` in four ways:

  * the database connection comes from environment variables
  * static files are served by WhiteNoise from the deployment bundle
  * media uploads go to S3-compatible object storage when configured
  * secrets never live in the repo

Local check without a database (uses SQLite):

    DJANGO_SETTINGS_MODULE=aakaar_main.settings_vercel \
    DJANGO_SECRET_KEY=local-test python manage.py check
"""

import os

# PyMySQL is a pure-Python MySQL driver, so the app does not need to compile
# mysqlclient (and its C headers) inside the Vercel build image.
try:  # pragma: no cover - trivial shim
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:  # pragma: no cover
    pass

from aakaar_main.settings import *  # noqa: F401,F403
from aakaar_main.settings import BASE_DIR

# --- core ------------------------------------------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or 'django-insecure-vercel-fallback-secret-key'

DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'

_hosts = [h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if h.strip()]
ALLOWED_HOSTS = _hosts + ['.vercel.app', 'localhost', '127.0.0.1']

_origins = [o.strip() for o in os.environ.get('DJANGO_CSRF_ORIGINS', '').split(',') if o.strip()]
CSRF_TRUSTED_ORIGINS = _origins + ['https://*.vercel.app']

# Vercel terminates TLS in front of the function and forwards the scheme.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Stay on by default (Vercel always terminates TLS); switch it off only to
# smoke-test the app over plain HTTP on localhost.
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'true').lower() != 'false'
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT

# --- database ---------------------------------------------------------------
# Any MySQL server reachable over the internet works (hosted MySQL, PlanetScale
# style providers, or the existing VPS MySQL if it is ever exposed). Falls back
# to SQLite so the settings can be exercised without a database.
if os.environ.get('DB_HOST'):
    _db_options = {
        'charset': 'utf8mb4',
        # Serverless functions open short-lived connections; don't hold them.
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
    if os.environ.get('DB_SSL', 'true').lower() != 'false':
        _db_options['ssl'] = {'ssl_mode': os.environ.get('DB_SSL_MODE', 'REQUIRED')}

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'aakaar_db'),
            'USER': os.environ.get('DB_USER', 'aakaar_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ.get('DB_PORT', '3306'),
            'CONN_MAX_AGE': 0,
            'OPTIONS': _db_options,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --- static files -----------------------------------------------------------
# Vercel serves nothing from disk on its own, so WhiteNoise serves the
# collected static files out of the function bundle.
MIDDLEWARE = list(MIDDLEWARE)
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}
WHITENOISE_KEEP_ONLY_HASHED_FILES = False
WHITENOISE_MAX_AGE = 31536000

# --- media uploads ----------------------------------------------------------
# Registration screenshots and abstracts are written to disk in production on
# the VPS. Vercel has no persistent disk, so they go to an S3-compatible bucket
# (Cloudflare R2, AWS S3, Backblaze B2, ...). Without it uploads are lost.
if os.environ.get('S3_BUCKET'):
    _s3_options = {
        'bucket_name': os.environ['S3_BUCKET'],
        'access_key': os.environ.get('S3_ACCESS_KEY_ID'),
        'secret_key': os.environ.get('S3_SECRET_ACCESS_KEY'),
        'region_name': os.environ.get('S3_REGION', 'auto'),
        'endpoint_url': os.environ.get('S3_ENDPOINT_URL') or None,
        'querystring_auth': os.environ.get('S3_QUERYSTRING_AUTH', 'true').lower() == 'true',
        'file_overwrite': False,
    }
    STORAGES['default'] = {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {k: v for k, v in _s3_options.items() if v is not None},
    }
    MEDIA_URL = os.environ.get('S3_PUBLIC_URL', MEDIA_URL)

# --- logging ----------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
