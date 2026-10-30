"""Idempotently normalise a template onto the design shell.

Safe to run repeatedly: it strips every previous injection (design asset
include, shell stylesheet links, mobile-menu script) and re-inserts exactly
one of each, so files that were patched more than once converge.
"""
import io
import os
import re

LIVE = [
    'templates/accomodation.html',
    'apps/compi/templates/logiq.html',
    'apps/compi/templates/seismic.html',
    'apps/compi/templates/bridgeit.html',
    'apps/compi/templates/conquerit.html',
    'apps/compi/templates/crackathon.html',
    'apps/compi/templates/idp.html',
    'apps/compi/templates/msewall.html',
    'apps/compi/templates/submission.html',
    'apps/events/templates/cenex.html',
    'apps/events/templates/workshop.html',
    'apps/events/templates/labvisit.html',
    'apps/events/templates/key.html',
    'apps/sympo/templates/poster.html',
    'apps/sympo/templates/city_front.html',
    'apps/sympo/templates/thesis_180.html',
    'apps/sympo/templates/home_new.html',
    'apps/sympo/templates/sympo_page.html',
    'apps/sympo/templates/new.html',
    'apps/sympo/templates/academic.html',
    'apps/sympo/templates/submission.html',
]

BANNER = '{# --- Tectonic Terra design shell --- #}'
ASSETS = (
    '\n{# --- Tectonic Terra design shell --- #}\n'
    '{% include "includes/design_assets.html" with preflight="off" %}\n'
    '<link rel="stylesheet" href="{% static \'css/custom-theme.css\' %}">\n'
    '<link rel="stylesheet" href="{% static \'css/site-polish.css\' %}">\n'
)
CHROME_JS = '<script src="{% static \'design/chrome.js\' %}"></script>\n'

# Everything this script owns, in any previously injected form.
STRIP = [
    re.compile(r'[ \t]*\{#\s*--- Tectonic Terra design shell ---\s*#\}\s*\n?'),
    re.compile(r'[ \t]*\{%\s*include\s+"includes/design_assets\.html"[^%]*%\}\s*\n?'),
    re.compile(r'[ \t]*<link[^>]*(?:custom-theme|site-polish)\.css[^>]*>\s*\n?'),
    re.compile(r'[ \t]*<script[^>]*design/chrome\.js[^>]*>\s*</script>\s*\n?'),
]


def normalise(path):
    text = io.open(path, encoding='utf-8', errors='replace').read()

    for pattern in STRIP:
        text = pattern.sub('', text)

    # Exactly one {% load static %}, at the very top.
    if '{% static' in text:
        text = re.sub(r'^\s*\{%\s*load\s+static\s*%\}\s*\n', '', text, count=1)
        text = '{% load static %}\n' + text

    if 'includes/design_header.html' not in text:
        m = re.search(r'<body[^>]*>', text)
        if not m:
            return 'no <body>'
        text = text[:m.end()] + '\n{% include "includes/design_header.html" %}\n' + text[m.end():]

    if 'includes/design_footer.html' not in text:
        i = text.rfind('</body>')
        if i == -1:
            return 'no </body>'
        text = text[:i] + '\n{% include "includes/design_footer.html" %}\n' + text[i:]

    i = text.find('</head>')
    if i == -1:
        return 'no </head>'
    text = text[:i] + ASSETS + text[i:]

    i = text.rfind('</body>')
    text = text[:i] + CHROME_JS + text[i:]

    io.open(path, 'w', encoding='utf-8', newline='').write(text)
    return 'normalised'


def main():
    for path in LIVE:
        if not os.path.exists(path):
            print('  ?? missing', path)
            continue
        print('  %-46s %s' % (path, normalise(path)))


if __name__ == '__main__':
    main()
