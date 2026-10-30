"""Export public Django routes and static assets to a static folder (dist/) for Netlify.
"""
import os
import shutil
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aakaar_main.settings_local')
os.environ.setdefault('DJANGO_SECRET_KEY', 'local-export-key')

import django
django.setup()

from django.core.management import call_command
from django.test import Client

OUTPUT_DIR = Path('dist')

ROUTES = [
    ('/', 'index.html'),
    ('/about/', 'about/index.html'),
    ('/partners/', 'partners/index.html'),
    ('/accomodation/', 'accomodation/index.html'),
    ('/events/', 'events/index.html'),
    ('/events/workshops', 'events/workshops/index.html'),
    ('/events/cenex', 'events/cenex/index.html'),
    ('/compi/', 'compi/index.html'),
    ('/sympo/', 'sympo/index.html'),
]

def main():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Run migrations so all database tables exist in the export environment
    print("Preparing export database...")
    call_command('migrate', verbosity=0)
    try:
        from django.contrib.sites.models import Site
        from allauth.socialaccount.models import SocialApp
        site, _ = Site.objects.get_or_create(id=1, defaults={'domain': 'localhost', 'name': 'localhost'})
        app, _ = SocialApp.objects.get_or_create(
            provider='google',
            defaults={'name': 'Google', 'client_id': 'export_dummy', 'secret': 'export_dummy'}
        )
        app.sites.add(site)
    except Exception as e:
        print(f"Site setup note: {e}")

    # 1. Copy static assets to dist/static/
    static_src = Path('static')
    static_dest = OUTPUT_DIR / 'static'
    if static_src.exists():
        print(f"Copying static files from {static_src} to {static_dest}...")
        shutil.copytree(static_src, static_dest, dirs_exist_ok=True)

    # 2. Render each route via Django test client
    client = Client()
    for route, dest_rel_path in ROUTES:
        print(f"Rendering route {route} -> {dest_rel_path}...")
        response = client.get(route)
        if response.status_code == 200:
            dest_file = OUTPUT_DIR / dest_rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            content = response.content
            dest_file.write_bytes(content)
        elif response.status_code in (301, 302):
            # Follow redirect if applicable
            redirect_url = response.headers.get('Location', '')
            print(f"  Redirect {route} -> {redirect_url}")
            redirect_response = client.get(redirect_url)
            if redirect_response.status_code == 200:
                dest_file = OUTPUT_DIR / dest_rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_bytes(redirect_response.content)
            else:
                print(f"  Warning: Redirect failed for {route} (status {redirect_response.status_code})")
        else:
            print(f"  Warning: Route {route} returned status {response.status_code}")

    # 3. Create a Netlify _redirects file for clean SPA-like routing fallback
    redirects_file = OUTPUT_DIR / '_redirects'
    redirects_file.write_text("/*    /index.html   200\n", encoding='utf-8')
    print("Static export complete in dist/")

if __name__ == '__main__':
    main()

