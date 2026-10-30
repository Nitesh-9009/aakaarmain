"""Generate the pixel-craft hero scene for the AAKAAR homepage.

Emits templates/includes/hero_pixel_scene.html: an inline SVG (pixel skyline,
mountains, pine trees, crane) plus a drifting-pixel overlay. Everything is
drawn on a 6px grid with crisp edges so it reads as true pixel art, and the
palette is the Tectonic Terra system (vellum / sage / forest / ochre).

Re-run with:  python build_hero_pixel.py
"""
import io
import random

W, H = 1200, 420          # viewBox
GROUND = 300              # horizon line
U = 6                     # base pixel unit

# Tectonic Terra palette
MOUNTAIN_FAR = '#F1F8EE'
MOUNTAIN_NEAR = '#D9E7DA'
CITY = '#AABDB1'
CITY_DARK = '#9BB0A3'
WIN = '#C6D5CB'
WIN_LIT = '#EFC055'
TREE = '#1E4B36'
TREE_LIT = '#2F6C4A'
TRUNK = '#4A3410'
SNOW = '#FFFFFF'


def rect(x, y, w, h, fill, cls=None, extra=''):
    c = ' class="%s"' % cls if cls else ''
    return '<rect x="%g" y="%g" width="%g" height="%g" fill="%s"%s%s/>' % (
        x, y, w, h, fill, c, extra)


def stairs(apex_x, apex_y, half, step, fill):
    """A triangle quantised into chunky horizontal steps (run-merged rects)."""
    def height_at(cx):
        t = abs(cx - apex_x) / half
        if t >= 1:
            return 0
        return int(round((GROUND - apex_y) * (1 - t) / step)) * step

    out, x = [], 0
    while x < W:
        h = height_at(x + U / 2)
        x2 = x + U
        while x2 < W and height_at(x2 + U / 2) == h:
            x2 += U
        if h > 0:
            out.append(rect(x, GROUND - h, x2 - x, h, fill))
        x = x2
    return '\n      '.join(out)


# --- skyline -------------------------------------------------------------
# (width in units, height in units, has antenna)
BUILDINGS = [
    (9, 8, 0), (6, 12, 1), (11, 6, 0), (7, 15, 0), (13, 9, 0),
    (8, 7, 0), (10, 17, 1), (6, 10, 0), (12, 8, 0), (9, 13, 0),
    (7, 6, 0), (11, 16, 0), (6, 9, 0), (10, 11, 1), (8, 6, 0),
    (12, 14, 0), (7, 8, 0), (9, 10, 0), (11, 7, 0), (6, 15, 0),
    (10, 9, 0), (8, 12, 0), (12, 6, 0), (7, 11, 0), (9, 8, 0),
    (11, 13, 0), (6, 9, 0), (10, 6, 0), (8, 10, 0), (12, 8, 0),
]


def city():
    out = []
    x = 0
    for i, (wu, hu, antenna) in enumerate(BUILDINGS):
        w, h = wu * U, hu * U
        if x >= W:
            break
        w = min(w, W - x)
        top = GROUND - h
        fill = CITY if i % 3 else CITY_DARK
        out.append(rect(x, top, w, h + 8, fill))
        # stepped roof cap
        out.append(rect(x + U, top - U, w - 2 * U, U, fill))
        if antenna and w >= 5 * U:
            out.append(rect(x + w / 2 - U / 2, top - 4 * U, U, 3 * U, fill))
            out.append(rect(x + w / 2 - U / 2, top - 5 * U, U, U, WIN_LIT,
                            'aa-beacon'))
        # windows
        cols = max(1, int((w - U) // (2 * U)))
        rows = max(1, int((h - 3 * U) // (2 * U)))
        for r_i in range(rows):
            for c_i in range(cols):
                if (r_i * 7 + c_i * 3 + i) % 5:
                    continue
                wx = x + U + c_i * 2 * U
                wy = top + 2 * U + r_i * 2 * U
                lit = (r_i + c_i + i) % 4 == 0
                out.append(rect(
                    wx, wy, U, U, WIN_LIT if lit else WIN,
                    'aa-window' if lit else None,
                    ' style="animation-delay:-%d.%ds"' % (i % 7, (i * 3) % 10)
                    if lit else ''))
        x += w + (U if i % 2 else 0)
    return '\n      '.join(out)


# --- trees ---------------------------------------------------------------
PINE7 = ['...f...', '..fff..', '..fff..', '.fffff.', '.fffff.',
         'fffffff', 'fffffff', '.fffff.', '...t...', '...t...']
PINE5 = ['..f..', '.fff.', '.fff.', 'fffff', 'fffff', '..t..', '..t..']
PINE3 = ['.f.', 'fff', '.t.']


def tree_group():
    """Scattered pine trees standing on the ground, each quietly swaying."""
    spec = [
        (18, 356, PINE5, 7, 7.0, -1.2),
        (74, 392, PINE7, 8, 9.0, -3.4),
        (128, 330, PINE3, 6, 8.0, -2.1),
        (168, 372, PINE5, 9, 6.4, -0.6),
        (232, 344, PINE5, 6, 9.6, -4.2),
        (286, 398, PINE7, 9, 7.6, -1.8),
        (352, 336, PINE3, 7, 8.8, -5.0),
        (398, 380, PINE5, 8, 6.8, -2.6),
        (466, 352, PINE5, 6, 9.2, -3.0),
        (520, 400, PINE7, 8, 7.2, -0.9),
        (934, 350, PINE5, 6, 9.0, -1.1),
        (986, 402, PINE7, 8, 7.4, -3.3),
        (1052, 340, PINE3, 6, 8.2, -5.4),
        (1096, 376, PINE5, 7, 6.9, -2.8),
        (1152, 396, PINE7, 9, 7.9, -1.7),
    ]
    out = []
    for x, base, bm, cell, dur, delay in spec:
        hgt = len(bm) * cell
        out.append('<g class="aa-tree" style="--sd:%.1fs;--sdl:%.1fs">'
                   % (dur, delay))
        for ry, row in enumerate(bm):
            for cx, ch in enumerate(row):
                if ch == '.':
                    continue
                left = row[cx - 1] if cx else '.'
                colour = TRUNK if ch == 't' else (TREE_LIT if left == '.'
                                                  else TREE)
                out.append(rect(x + cx * cell, base - hgt + ry * cell,
                                cell, cell, colour))
        out.append('</g>')
    return '\n      '.join(out)


def crane():
    x, top, mast = 924, 196, 7
    out = [
        rect(x, top, mast, GROUND - top, '#E8B94F'),
        rect(x + mast, top, 108, mast, '#E8B94F'),
        rect(x + mast + 100, top + mast, mast, 26, '#E8B94F'),
        rect(x - 20, top, 28, mast, '#D4A33B'),
        # cross bracing on the mast
    ]
    for i in range(6):
        out.append(rect(x - mast, top + mast * 2 + i * 24, mast, mast, '#D4A33B'))
    # hanging hook + load
    out.append(rect(x + mast + 74, top + mast, 4, 44, '#D4A33B'))
    out.append('<g class="aa-hook">' + rect(x + mast + 64, top + mast + 44,
                                             24, 20, '#C9922C') + '</g>')
    return '\n      '.join(out)


CLOUD = ['..cccc....', '.cccccc...', 'cccccccc..', '.cccc.....']


def clouds():
    out = []
    for x, y, cell, dur, delay in [
        (96, 168, 9, 26, -4), (300, 232, 7, 32, -14),
        (860, 150, 10, 22, -9), (1046, 118, 7, 30, -19),
    ]:
        out.append('<g class="aa-cloud" style="--cd:%.0fs;--cdl:%.0fs">'
                   % (dur, delay))
        for ry, row in enumerate(CLOUD):
            for cx, ch in enumerate(row):
                if ch == 'c':
                    out.append(rect(x + cx * cell, y + ry * cell,
                                    cell, cell, SNOW, None,
                                    ' fill-opacity=".9"'))
        out.append('</g>')
    return '\n      '.join(out)


# --- mascots -------------------------------------------------------------
OWL = [
    '..DD....DD..',
    '..DGD..DGD..',
    '.DGGGDDGGGD.',
    '.DGGGGGGGGD.',
    'DGGWWGGWWGGD',
    'DGGWWGGWWGGD',
    'DGGWKGGWKGGD',
    'DGGGGGOOGGGD',
    'DGGCCCCCCGGD',
    'DDGCCCCCCGDD',
    '.DGCCCCCCGD.',
    '.DGCCCCCCGD.',
    '..DCCCCCCD..',
    '...DCCCCD...',
    '...O....O...',
]
OWL_KEY = {'D': '#143A2B', 'G': '#357A50', 'W': '#FFFFFF',
           'K': '#1B1C18', 'C': '#F6EFDA', 'O': '#E8B94F'}

PENGUIN = [
    '...NNNN...',
    '..NNNNNN..',
    '..NKKKKN..',
    '.NKWWWWKN.',
    '.NKWWWWKN.',
    '.NKWOOWKN.',
    '.NKKKKKKN.',
    '.NKWWWWKN.',
    '.NKWWWWKN.',
    '.NKWWWWKN.',
    '..NKKKKN..',
    '..NKKKKN..',
    '..O....O..',
    '..OO..OO..',
]
PENGUIN_KEY = {'N': '#22303C', 'K': '#1B1C18', 'W': '#FFFFFF',
               'O': '#E8B94F'}


def sprite(x, base, cell, grid, key, cls):
    """Stamp a character grid onto the 6px pixel lattice, feet on `base`."""
    out = ['<g class="%s">' % cls]
    top = base - len(grid) * cell
    for ry, row in enumerate(grid):
        for cx, ch in enumerate(row):
            if ch == '.':
                continue
            out.append(rect(x + cx * cell, top + ry * cell, cell, cell,
                            key[ch]))
    out.append('</g>')
    return '\n      '.join(out)


def owl_lids(x, base, cell):
    """Eyelid blocks that flick shut every few seconds."""
    top = base - len(OWL) * cell
    out = ['<g class="aa-owl-lids">']
    for col in (3, 7):
        out.append(rect(x + col * cell, top + 4 * cell, 2 * cell, cell,
                        OWL_KEY['D']))
    out.append('</g>')
    return '\n      '.join(out)


def bubble(x, y, w, h, label, tail_x):
    """Pixel-edged speech bubble with a hollow tail pointing down-left."""
    tx = tail_x
    pts = [
        (x + 8, y), (x + w - 8, y), (x + w - 8, y + 8), (x + w, y + 8),
        (x + w, y + h - 8), (x + w - 8, y + h - 8), (x + w - 8, y + h),
        (tx + 34, y + h), (tx + 34, y + h + 8), (tx + 24, y + h + 8),
        (tx + 24, y + h + 16), (tx + 12, y + h + 16), (tx + 12, y + h + 8),
        (tx, y + h + 8), (tx, y + h), (x + 8, y + h), (x + 8, y + h - 8),
        (x, y + h - 8), (x, y + 8), (x + 8, y + 8),
    ]
    d = 'M' + ' L'.join('%d %d' % p for p in pts) + ' Z'
    return ('<g class="aa-bubble">'
            '<path d="%s" fill="#FFFFFF" stroke="#1B1C18" '
            'stroke-width="4"/>'
            '<text class="aa-bubble-text" x="%d" y="%d" '
            'text-anchor="middle">%s</text></g>'
            % (d, x + w // 2, y + h // 2 + 5, label))


def cast():
    penguin_x, penguin_base, pc = 586, 412, 9
    owl_x, owl_base, oc = 708, 412, 9
    out = [
        sprite(penguin_x, penguin_base, pc, PENGUIN, PENGUIN_KEY,
               'aa-char aa-penguin'),
        sprite(owl_x, owl_base, oc, OWL, OWL_KEY, 'aa-char aa-owl'),
        owl_lids(owl_x, owl_base, oc),
        '<g class="aa-bubble-wrap aa-bubble-left">',
        bubble(474, 198, 192, 48, 'High five!', 556),
        '</g>',
        '<g class="aa-bubble-wrap aa-bubble-right">',
        bubble(844, 186, 208, 48, 'Hello there!', 854),
        '</g>',
    ]
    return '\n      '.join(out)


def snowfall_drift():
    """Snow bank across the foreground, so trees and mascots sit in snow."""
    steps = [
        (0, 386, 132), (132, 374, 96), (228, 382, 128), (356, 368, 120),
        (476, 378, 132), (608, 362, 148), (756, 376, 128), (884, 368, 116),
        (1000, 380, 108), (1108, 372, 92),
    ]
    out = []
    for x, y, w in steps:
        out.append(rect(x, y, w, H - y, '#FFFFFF'))
        out.append(rect(x, y, w, 6, '#FFFFFF'))
    for x, y, w in [(168, 402, 40), (392, 396, 32), (652, 400, 44),
                    (940, 398, 36), (1132, 404, 40), (532, 398, 30)]:
        out.append(rect(x, y, w, 6, '#EAF1EA'))
    return '\n      '.join(out)


def ground_patches():
    """Drifts of snow and small pebbles scattered over the ground plane."""
    spec = [
        (84, 340, 54, 12), (196, 372, 72, 12), (322, 344, 42, 12),
        (430, 398, 60, 12), (540, 366, 48, 12), (664, 408, 66, 12),
        (760, 352, 54, 12), (872, 388, 78, 12), (1004, 360, 48, 12),
        (1104, 400, 60, 12),
    ]
    out = []
    for x, y, w, h in spec:
        out.append(rect(x, y, w, h, '#FFFFFF'))
        out.append(rect(x + 12, y + h, w - 24, 6, '#EFF5EF'))
    for x, y, w, h in [(60, 356, 18, 8), (252, 402, 24, 8), (378, 380, 18, 8),
                       (596, 396, 24, 8), (708, 376, 18, 8),
                       (930, 404, 24, 8), (1032, 384, 18, 8)]:
        out.append(rect(x, y, w, h, '#DCE7DE'))
    return '\n      '.join(out)


def snow(count=54, seed=7):
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        x = round(rng.uniform(0, 99.4), 1)
        s = rng.choice([3, 4, 5, 6])
        o = round(rng.uniform(0.35, 0.95), 2)
        d = round(rng.uniform(11, 24), 1)
        dl = -round(rng.uniform(0, 24), 1)
        dx = rng.randint(-26, 26)
        ty = rng.randint(600, 820)
        colour = '#ffffff' if rng.random() < 0.62 else '#c8d7cc'
        out.append(
            '<i style="--x:%.1f%%;--s:%dpx;--o:%.2f;--d:%.1fs;--dl:%.1fs;'
            '--dx:%dpx;--ty:%dpx;--c:%s"></i>'
            % (x, s, o, d, dl, dx, ty, colour))
    return '\n    '.join(out)


SVG = '''<div class="aa-hero-scene" aria-hidden="true">
  <svg class="aa-scene-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice"
       shape-rendering="crispEdges" role="presentation" focusable="false">
    <defs>
      <linearGradient id="aa-ground" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff"/>
        <stop offset=".55" stop-color="#fdfcf6"/>
        <stop offset="1" stop-color="#fbf9f2"/>
      </linearGradient>
    </defs>
    <g class="aa-clouds">
      {clouds}
    </g>
    <g class="aa-mountains">
      {m_far}
      {m_near}
    </g>
    <g class="aa-city">
      {city}
    </g>
    <g class="aa-ground">
      <rect x="0" y="{GROUND}" width="{W}" height="{GH}" fill="url(#aa-ground)"/>
      {patches}
    </g>
    <g class="aa-crane">
      {crane}
    </g>
    <g class="aa-treeline">
      {trees}
    </g>
    <g class="aa-drift">
      {drift}
    </g>
    <g class="aa-cast">
      {cast}
    </g>
  </svg>
</div>
<div class="aa-snow" aria-hidden="true">
    {snow}
</div>
'''.format(W=W, H=H, GROUND=GROUND, GH=H - GROUND,
           clouds=clouds(),
           m_far=stairs(430, 104, 440, 18, MOUNTAIN_FAR),
           m_near=stairs(905, 152, 330, 18, MOUNTAIN_NEAR),
           city=city(),
           crane=crane(),
           patches=ground_patches(),
           trees=tree_group(),
           drift=snowfall_drift(),
           cast=cast(),
           snow=snow())

io.open('templates/includes/hero_pixel_scene.html', 'w', encoding='utf-8').write(SVG)
print('templates/includes/hero_pixel_scene.html  %d bytes' % len(SVG))
