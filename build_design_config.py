"""Generate the vendored Tailwind configs from the reference design's own config.

Some of the reference pages reference a second, ad-hoc colour vocabulary
(`playful-lime`, `deep-evergreen`, `warm-ivory`, ...) that the shared config
never declared, so those utilities compiled to nothing. The values below are
read off the design's own arbitrary-value classes (`bg-[#B8E965]`,
`shadow-[0_4px_0_#409148]`, `bg-[#175134]`) and the documented palette.
"""
import io

RAW = 'static/design/_cfg_raw.txt'
EXTRA = {
    'playful-lime': '#B8E965',      # matches bg-[#B8E965] in the reference
    'electric-lime': '#a6d654',     # matches hover:bg-[#a6d654]
    'fresh-grass': '#409148',       # matches shadow-[0_4px_0_#409148]
    'deep-evergreen': '#175134',    # matches bg-[#175134]
    'charcoal-ink': '#131f00',      # matches text-[#131f00]
    'warm-ivory': '#FAF8F1',        # documented neutral surface baseline
    'crisp-white': '#FFFFFF',
    'outline-warm': '#E2DEC9',      # documented muted sandstone border
}

cfg = io.open(RAW, encoding='utf-8').read()

inject = ','.join('"%s": "%s"' % (k, v) for k, v in EXTRA.items())
marker = '"colors": {'
if marker not in cfg:
    raise SystemExit('could not find the colors block in the design config')

cfg = cfg.replace(marker, marker + inject + ',', 1)

io.open('static/design/tailwind-config.js', 'w', encoding='utf-8').write(cfg + '\n')

legacy = cfg.replace('tailwind.config = {',
                     'tailwind.config = { corePlugins: { preflight: false },', 1)
io.open('static/design/tailwind-config-legacy.js', 'w', encoding='utf-8').write(legacy + '\n')

print('wrote tailwind-config.js and tailwind-config-legacy.js')
for k, v in EXTRA.items():
    print('  %-16s %s' % (k, v))
