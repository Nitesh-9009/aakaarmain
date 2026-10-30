import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# This line is CRITICAL for finding your other apps.
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# === PRODUCTION SETTINGS ===

# Pull the secret key from an environment variable.
# NEVER hard-code this in production.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG must be False in production.
DEBUG = True # Defaults to False

# Add your domain.
ALLOWED_HOSTS = ['aakaariitb.org.in', 'www.aakaariitb.org.in', '127.0.0.1', 'localhost']

# === INSTALLED_APPS ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
   
    # Unified apps
    'events',
    'compi',
    'sympo',
    'sympo.cityplan_app',
    'sympo.poster_app',
    'sympo.threemtt',

    # Other required apps
    'crispy_forms',
    'import_export',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Gunicorn is needed to run the app on the server
    'gunicorn', 
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'aakaar_main.urls'

# === TEMPLATES ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aakaar_main.wsgi.application'

# === DATABASE ===
# Configured for MySQL. We will set the environment variables in Hostinger.
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aakaar_db',                # The DB name you created
        'USER': 'aakaar_user',               # The user you created
        'PASSWORD':'Aakaar@iitb2026', # Pulled from environment
        'HOST': 'localhost',
        'PORT': '',
    }
}
# === PASSWORD VALIDATORS ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# === STATIC FILES ===
STATIC_URL = 'static/'

# 1. Where Nginx looks (Destination)
# REQUIRED for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 2. Where YOU save files (Source)
# This is the part you asked about - it is correct!
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Add this. Nginx will serve files from this directory.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === ALLAUTH SETTINGS ===
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# === PRODUCTION SECURITY SETTINGS ===
# These are vital for HTTPS
CSRF_TRUSTED_ORIGINS = ['https://aakaariitb.org.in', 'https://www.aakaariitb.org.in']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
