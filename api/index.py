"""Vercel serverless entrypoint for the Django project.

Vercel's Python runtime imports this module and looks for a WSGI callable, so
``app`` is the whole Django application.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aakaar_main.settings_vercel')

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
