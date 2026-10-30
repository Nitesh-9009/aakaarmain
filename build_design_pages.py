"""Convert the reference Stitch design HTML into Django templates.

Keeps the reference markup byte-for-byte inside <main>, and only:
  * swaps the design's dead Google-hosted images for local design assets
  * wires the placeholder `data-path` links and bare `#` anchors to real routes
  * normalises a few edition/date strings to the live festival edition
"""
import io
import os
import re
import sys

SRC = '.stitch_design/stitch_aakaar_iit_bombay_website_redesign'

ROUTES = {
    'home': '/',
    'about': '/about/',
    'about-legacy': '/about/',
    'events': '/events/',
    'workshops': '/events/workshops',
    'workshops-cenex': '/events/cenex',
    'symposium-ices': '/sympo/',
    'competitions': '/compi/',
    'partners': '/partners/',
    'partners-sponsors': '/partners/',
    'contact': '/#contact',
    'register': '/compi/',
}

# Which local images fill each page's content image slots, in document order.
IMAGES = {
    'aakaar_iit_bombay_main_festival_website': [
        'hero-engineering.jpg', 'wide-1.jpg', 'wide-2.jpg',
    ],
    'about_legacy_aakaar_iit_bombay': [
        'hero-campus.jpg', 'portrait-1.jpg', 'portrait-2.jpg', 'portrait-3.jpg',
        'photo-auditorium.jpg', 'photo-classroom.jpg', 'photo-construction.jpg',
    ],
    'competitions_aakaar_iit_bombay': [
        'photo-structure.jpg', 'photo-skyline-night.jpg', 'poster-highway.jpg',
        'poster-crackathon.jpg', 'photo-construction.jpg',
    ],
    'international_civil_engineering_symposium_ices_aakaar_iit_bombay': [
        'wide-3.jpg', 'portrait-4.jpg', 'portrait-5.jpg', 'portrait-6.jpg', 'portrait-7.jpg',
    ],
    'partners_sponsors_aakaar_iit_bombay': [
        'photo-construction.jpg',
    ],
    'workshops_cenex_aakaar_iit_bombay': [
        'photo-lab.jpg', 'photo-computerlab.jpg', 'poster-revit.jpg',
        'photo-panel.jpg', 'photo-auditorium.jpg', 'photo-classroom.jpg',
    ],
}

PAGES = [
    dict(src='aakaar_iit_bombay_main_festival_website',
         out='templates/aakaar_new.html',
         title='AAKAAR | IIT Bombay',
         default='/compi/',
         hero='pixel'),
    dict(src='about_legacy_aakaar_iit_bombay',
         out='templates/about_legacy.html',
         title='About & Legacy | AAKAAR IIT Bombay',
         default='/about/'),
    dict(src='competitions_aakaar_iit_bombay',
         out='apps/compi/templates/compi_page.html',
         title='Competitions | AAKAAR IIT Bombay',
         default='/compi/'),
    dict(src='international_civil_engineering_symposium_ices_aakaar_iit_bombay',
         out='apps/sympo/templates/sympo_main.html',
         title='International Civil Engineering Symposium | AAKAAR IIT Bombay',
         default='/sympo/paper/'),
    dict(src='partners_sponsors_aakaar_iit_bombay',
         out='templates/partners_sponsors.html',
         title='Partners & Sponsors | AAKAAR IIT Bombay',
         default='/partners/'),
    dict(src='workshops_cenex_aakaar_iit_bombay',
         out='apps/events/templates/events_page.html',
         title='Workshops & CENEX | AAKAAR IIT Bombay',
         default='/events/workshops'),
]

# The reference copy was written for a previous cycle; align it to the edition
# the live site is running (18th Edition, 2026) without touching layout.
COPY_FIXES = [
    ('16th Edition', '18th Edition'),
    ('16th edition', '18th edition'),
    ('AAKAAR 2025', 'AAKAAR 2026'),
    ('AAKAAR 2024', 'AAKAAR 2026'),
    ('SPECIFICATION DECK 2025', 'SPECIFICATION DECK 2026'),
    ('The 2025 Sponsorship Deck', 'The 2026 Sponsorship Deck'),
    ('ICES 2025', 'ICES 2026'),
    ('ices2025_template.tex', 'ices2026_template.tex'),
    ('March 2025', 'March 2026'),
    ('FEB 20, 2025', 'FEB 20, 2026'),
    ('FEB 28, 2025', 'FEB 28, 2026'),
    ('MAR 08, 2025', 'MAR 08, 2026'),
    ('MAR 21\u201323, 2025', 'MAR 21\u201323, 2026'),
    ('Feb 20, 2025', 'Feb 20, 2026'),
    ('Feb 28, 2025', 'Feb 28, 2026'),
    ('Mar 08, 2025', 'Mar 08, 2026'),
    ('\u00a9 2025', '\u00a9 2026'),
]


def extract_main(html):
    """Return only the sections inside the design's <main> wrapper."""
    start = html.index('<main')
    start = html.index('>', start) + 1
    end = html.index('</main>')
    inner = html[start:end].strip()
    # strip the design's own flex wrapper; base_design.html provides it
    inner = re.sub(r'^<div class="flex flex-col w-full">', '', inner, count=1)
    inner = re.sub(r'</div>\s*$', '', inner, count=1)
    return inner.strip()


def rewrite_images(html, names):
    """Swap the design's dead remote images for local design assets.

    Walks every remote image reference in document order so <img> tags and
    CSS background images share one ordered slot list.
    """
    slots = iter(names)

    def static_for(rest):
        try:
            return "{% static 'design/img/" + next(slots) + "' %}"
        except StopIteration:
            print('    !! image slots exhausted', file=sys.stderr)
            return None

    pattern = re.compile(r'<img [^>]*>|url\(\'https://lh3[^\']*\'\)')

    def repl(match):
        text = match.group(0)
        if text.startswith('<img'):
            src = re.search(r'src="([^"]*)"', text)
            if not src:
                return text
            if 'aida/AEtj' in src.group(1):          # the AAKAAR emblem
                new = "{% static 'design/img/emblem.png' %}"
            else:
                new = static_for(text)
                if new is None:
                    return text
            text = text[:src.start(1)] + new + text[src.end(1):]
            return re.sub(r'data-alt="[^"]*"', '', text)
        new = static_for(text)
        if new is None:
            return text
        return 'url(' + new + ')'

    return pattern.sub(repl, html)


def rewrite_links(html, default_url):
    """Wire data-path placeholders and bare # anchors to real routes."""
    ids = set(re.findall(r'id="([^"]+)"', html))

    def anchor(match):
        tag = match.group(0)
        path = re.search(r'data-path="([^"]+)"', tag)
        href = re.search(r'href="([^"]*)"', tag)
        if not href:
            return tag
        target = href.group(1)
        if path:
            url = ROUTES.get(path.group(1), default_url)
        elif target == '#' or target == '':
            url = default_url
        elif target.startswith('#') and target[1:] not in ids:
            url = default_url
        else:
            return tag
        tag = tag[:href.start(1)] + url + tag[href.end(1):]
        tag = re.sub(r'\s*data-path="[^"]*"', '', tag)
        return tag

    return re.sub(r'<a\b[^>]*>', anchor, html)


# The homepage hero is replaced by our own centred pixel-craft hero: one
# shared include, so regenerating from the reference never loses it.
HERO_SECTION = re.compile(r'<section\b[^>]*>.*?</section>', re.S)

# NOTE: this is a substitution *value*, so Django tags use a single %.
HERO_HEAD = (
    '{% block extra_head %}'
    '<link rel="stylesheet" href="{% static \'design/hero-pixel.css\' %}">'
    '{% endblock %}\n'
)


def main():
    for page in PAGES:
        path = os.path.join(SRC, page['src'], 'code.html')
        html = io.open(path, encoding='utf-8').read()
        body = extract_main(html)
        names = IMAGES[page['src']]
        before = body.count('<img ')
        body = rewrite_images(body, names)
        body = rewrite_links(body, page['default'])
        for old, new in COPY_FIXES:
            body = body.replace(old, new)

        head = ''
        if page.get('hero') == 'pixel':
            body = HERO_SECTION.sub(
                '{% include "includes/hero_home.html" %}', body, count=1)
            head = HERO_HEAD

        out = (
            '{%% extends "base_design.html" %%}\n'
            '{%% load static %%}\n'
            '{%% block title %%}%s{%% endblock %%}\n'
            '%s'
            '{%% block content %%}\n%s\n{%% endblock %%}\n'
        ) % (page['title'], head, body)
        io.open(page['out'], 'w', encoding='utf-8').write(out)
        print('  %-58s %6d bytes (%d images)' % (page['out'], len(out), before))


if __name__ == '__main__':
    main()
