"""Build the local image assets the design pages need.

The reference build points at Google-hosted URLs that no longer resolve, so
each slot is filled from the repository's own photography. Sources are chosen
so nothing off-topic (mascot logos, catering shots) reaches the pages, and each
output is cropped to the aspect ratio its container expects.
"""
import os

from PIL import Image

OUT = 'static/design/img'

# slot name -> (source file, target width, aspect ratio or None, vertical anchor)
CARDS = {
    'photo-lab.jpg': ('static/assets/img/h1.jpg', 900, 1.5, 0.5),
    'photo-audience.jpg': ('static/assets/img/h2.jpg', 900, 1.5, 0.5),
    'photo-award.jpg': ('static/assets/img/h3.jpg', 900, 1.5, 0.5),
    'photo-auditorium.jpg': ('static/assets/img/h4.jpg', 900, 1.5, 0.5),
    'photo-festival.jpg': ('static/assets/img/h5.jpg', 900, 1.5, 0.5),
    'photo-construction.jpg': ('static/assets/img/sympo.jpg', 900, 1.5, 0.5),
    'photo-skyline-night.jpg': ('static/assets/img/smart.jpg', 900, 1.5, 0.5),
    'photo-symposium.jpg': ('static/assets/img/sym1.jpg', 900, 1.5, 0.5),
    'photo-structure.jpg': ('static/assets/img/person_1.jpg', 900, 1.5, 0.45),
    'photo-presenter.jpg': ('static/assets/img/skguota.jpg', 900, 1.5, 0.4),
    'photo-award2.jpg': ('static/sympo_events/img1.jpeg', 900, 1.5, 0.4),
    'photo-panel.jpg': ('static/sympo_events/img2.jpeg', 900, 1.5, 0.45),
    'photo-computerlab.jpg': ('static/sympo_events/img3.jpeg', 900, 1.5, 0.45),
    'photo-classroom.jpg': ('static/sympo_events/img4.jpeg', 900, 1.5, 0.45),
    'photo-group.jpg': ('static/sympo_events/img5.jpeg', 900, 1.5, 0.4),
    'poster-crackathon.jpg': ('static/compi/Crackathon.jpeg', 900, 1.5, 0.5),
    'poster-highway.jpg': ('static/compi/idp.jpeg', 900, 1.5, 0.5),
    'poster-revit.jpg': ('static/image/revit.png', 900, 1.5, 0.5),
    'poster-paper.jpg': ('static/sympo_events/Paper Presentation.png', 900, 1.5, 0.5),
    'poster-poster.jpg': ('static/sympo_events/Poster Presentation.png', 900, 1.5, 0.5),
    'poster-thesis.jpg': ('static/sympo_events/Theses 180.png', 900, 1.5, 0.5),
    'graphic-competitions.jpg': ('static/assets/img/1.png', 900, 1.5, 0.5),
    'graphic-events.jpg': ('static/assets/img/2.png', 900, 1.5, 0.5),
    'graphic-symposium.jpg': ('static/assets/img/3.png', 900, 1.5, 0.5),
    'graphic-cr.jpg': ('static/assets/img/4.png', 900, 1.5, 0.5),
}

HEROES = {
    'hero-engineering.jpg': ('static/assets/img/h1.jpg', 1400, 4 / 3, 0.5),
    'hero-campus.jpg': ('static/assets/img/h4.jpg', 1400, 4 / 3, 0.5),
    'hero-award.jpg': ('static/assets/img/h3.jpg', 1400, 4 / 3, 0.5),
}

# People: head-and-shoulders crops, biased towards the upper part of the frame.
PORTRAITS = [
    'static/assets/img/akhi.jpg',
    'static/assets/img/Nisha.jpg',
    'static/assets/img/Rahul.jpg',
    'static/img/khushal.jpeg',
    'static/img/pp1.jpeg',
    'static/img/pp2.jpeg',
    'static/img/anulaya.jpeg',
    'static/sympo_events/Rithishram.png',
]

WIDES = [
    'static/assets/img/5E2A9260.JPG',
    'static/assets/img/5E2A8940.JPG',
    'static/assets/img/5E2A9036.JPG',
    'static/assets/img/5E2A8968.JPG',
    'static/assets/img/5E2A8946.JPG',
    'static/assets/img/5E2A9261.JPG',
    'static/assets/img/5E2A9303.JPG',
    'static/assets/events/images/5E2A8637.JPG',
    'static/assets/events/images/5E2A8893.JPG',
]


def load(path):
    image = Image.open(path)
    image.load()
    return image.convert('RGB')


def crop_to(image, ratio, anchor=(0.5, 0.5)):
    width, height = image.size
    if width / height > ratio:
        new_w, new_h = int(height * ratio), height
    else:
        new_w, new_h = width, int(width / ratio)
    x = int((width - new_w) * anchor[0])
    y = int((height - new_h) * anchor[1])
    return image.crop((x, y, x + new_w, y + new_h))


def save(image, name, width, ratio, anchor):
    if ratio:
        image = crop_to(image, ratio, anchor)
    height = int(image.size[1] * width / image.size[0])
    image = image.resize((width, height), Image.LANCZOS)
    image.save(os.path.join(OUT, name), quality=86, optimize=True, progressive=True)
    print('  %-28s %s' % (name, image.size))


def build_emblem():
    """Square forest-ink emblem, lifted from the ink wordmark."""
    ink = Image.open('static/img/aakaar_logo_ink.png').convert('RGBA')
    width, height = ink.size
    mark = ink.crop((0, 0, int(width * 0.30), height))
    mark = mark.crop(mark.getbbox())
    side = max(mark.size)
    canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    canvas.paste(mark, ((side - mark.size[0]) // 2, (side - mark.size[1]) // 2), mark)
    canvas.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, 'emblem.png'))
    print('  %-28s %s' % ('emblem.png', (256, 256)))


def main():
    os.makedirs(OUT, exist_ok=True)
    build_emblem()

    for name, (source, width, ratio, anchor) in {**CARDS, **HEROES}.items():
        if os.path.exists(source):
            save(load(source), name, width, ratio, (0.5, anchor))
        else:
            print('  !! missing source for', name, source)

    for i, source in enumerate(WIDES, 1):
        if os.path.exists(source):
            save(load(source), 'wide-%d.jpg' % i, 1800, 4.0, (0.5, 0.5))

    for i, source in enumerate(PORTRAITS, 1):
        if os.path.exists(source):
            save(load(source), 'portrait-%d.jpg' % i, 700, 7 / 8, (0.5, 0.22))


if __name__ == '__main__':
    main()
