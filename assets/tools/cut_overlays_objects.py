# -*- coding: utf-8 -*-
"""Knip het goedgekeurde contactvel uit tot losse tekeningen.

Bron: assets/art/concepts/clueboard-neutral-overlays-and-objects-transparent-v4.png
Dat vel is één RGBA-beeld met bovenaan elf neutrale materiaaloverlays en
daaronder acht objecten, met bijschriften ertussen. Dit gereedschap schrijft ze
weg als losse bestanden:

  assets/art/overlays/<vloersoort>.png   elf vierkanten, exact 1:1
  assets/art/objects/<naam>.png          acht objecten, op hun eigen maat

De bijschriften moeten eerst weg. Een uitsnede is een rechthoek, en bij de boom
en het staande bed valt het woord binnen diezelfde rechthoek -- de zachte
slagschaduw raakt het zelfs, dus op vorm alleen is het niet te scheiden. Op
kleur en plek wel: de bijschriften zijn bijna zwart en staan op lage regels,
terwijl de donkere delen van een tekening veel hoger doorlopen. Ze gaan
weg: we zoeken eerst de regels waarop tekst staat, en halen daar de inkt weg
met een randje eromheen tegen de grijze waas van de antialiasing.

Draaien:  python assets/tools/cut_overlays_objects.py
"""
import os
import sys
import numpy as np
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, 'assets', 'art', 'concepts',
                    'clueboard-neutral-overlays-and-objects-transparent-v4.png')
UIT_OVERLAY = os.path.join(WORTEL, 'assets', 'art', 'overlays')
UIT_OBJECT = os.path.join(WORTEL, 'assets', 'art', 'objects')

# De elf overlays staan in de volgorde van het stijlvel; de namen zijn de
# vloersoorten die een level kan opgeven.
OVERLAYS = ['stone', 'concrete', 'tile', 'marble', 'dirt', 'sand', 'gravel',
            'wood', 'grass', 'carpet', 'water']
OVERLAY_MAAT = 256          # vierkant, ruim genoeg voor een groot vakje

# De acht objecten, in leesvolgorde: eerst de rij van 1x1, dan de grote.
OBJECTEN = ['chair', 'barrel', 'shelf', 'tree',
            'table-2x1', 'table-1x2', 'bed-2x1', 'bed-1x2']

DREMPEL = 8                 # alfa waaronder een pixel als leeg telt
MIN_ZIJDE = 60              # kleiner dan dit is een letter, geen tekening
SCHADUW_ALFA = 70           # zo doorzichtig staat de ingebakken schaduw erop
SCHADUW_ZWART = 16          # en zo zwart; de tekeningen zelf worden dat nooit
INKT_LUMA = 70              # zo donker wordt alleen een bijschrift
TEKST_HOOG = 22             # hoger dan dit is geen regel tekst meer
TEKST_MIN = 100             # en zoveel zwart staat er minstens op
WAAS_LUMA = 120             # het grijs eromheen dat mee mag
TEKST_MARGE = 3             # regels marge boven en onder een regel tekst


def vlekken(masker):
    """Samenhangende vlekken in een masker, als (x0, y0, x1, y1, punten)."""
    h, b = masker.shape
    gezien = np.zeros_like(masker)
    uit = []
    for y in range(h):
        rij = masker[y]
        for x in range(b):
            if not rij[x] or gezien[y, x]:
                continue
            stapel = [(y, x)]
            gezien[y, x] = True
            punten = []
            minx = maxx = x
            miny = maxy = y
            while stapel:
                cy, cx = stapel.pop()
                punten.append((cy, cx))
                if cx < minx: minx = cx
                if cx > maxx: maxx = cx
                if cy < miny: miny = cy
                if cy > maxy: maxy = cy
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < b and masker[ny, nx] and not gezien[ny, nx]:
                        gezien[ny, nx] = True
                        stapel.append((ny, nx))
            uit.append((minx, miny, maxx, maxy, punten))
    return uit


def tekstbanden(a, luma):
    """De regels waarop bijschriften staan.

    Bijschrift is pikzwart en dekkend; geen van de tekeningen wordt zo donker.
    Een regel tekst is bovendien laag -- hooguit een letterhoogte -- terwijl de
    donkere delen van een tekening (de boekruggen in de kast bijvoorbeeld) veel
    hoger doorlopen. Die twee samen wijzen de regels precies aan.
    """
    zwart = (a[:, :, 3] > 200) & (luma < 50)
    perRij = zwart.sum(axis=1)
    banden = []
    start = None
    for y in range(len(perRij)):
        if perRij[y] > 0 and start is None:
            start = y
        elif perRij[y] == 0 and start is not None:
            banden.append((start, y - 1))
            start = None
    if start is not None:
        banden.append((start, len(perRij) - 1))
    return [b for b in banden
            if (b[1] - b[0] + 1) <= TEKST_HOOG and perRij[b[0]:b[1] + 1].sum() >= TEKST_MIN]


def wis_bijschriften(im):
    """Alle bijschriften van het vel halen, tekening en schaduw ongemoeid.

    Binnen zo'n regel gaat alleen de inkt weg, met een pixel eromheen tegen de
    grijze waas van de antialiasing. De zachte slagschaduw die er soms doorheen
    loopt is veel lichter en veel doorzichtiger, en blijft dus gewoon staan.
    """
    a = np.array(im)
    luma = a[:, :, :3].mean(axis=2)
    banden = tekstbanden(a, luma)
    inkt = np.zeros(a.shape[:2], dtype=bool)
    for y0, y1 in banden:
        # Een paar regels marge: de bovenste en onderste rij van een letter is
        # nooit pikzwart, dus die valt buiten de gevonden band.
        y0 = max(0, y0 - TEKST_MARGE)
        y1 = min(a.shape[0] - 1, y1 + TEKST_MARGE)
        inkt[y0:y1 + 1] |= (a[y0:y1 + 1, :, 3] > 60) & (luma[y0:y1 + 1] < INKT_LUMA)
    # Een pixel eromheen mee, zolang die ook aan de donkere kant is.
    randje = inkt.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            randje |= np.roll(np.roll(inkt, dy, axis=0), dx, axis=1)
    randje &= (luma < WAAS_LUMA)
    a[:, :, 3] = np.where(randje, 0, a[:, :, 3])
    print('bijschriften weg:', len(banden), 'regels tekst')
    return Image.fromarray(a, 'RGBA')


def schoonmaak(deel):
    """Een uitgeknipte tekening klaarmaken voor het bord.

    Twee dingen zitten er nog in die er niet horen.

    De ingebakken slagschaduw: een silhouet in zwart op zeventien procent,
    naar rechtsonder verschoven. Op het vel oogt dat goed, maar op het bord is
    het geen contactschaduw -- hij hangt los van de tegel en volgt het licht
    van het bord niet. Zwart bij zo'n lage dekking komt in de tekeningen zelf
    nergens voor, dus hij is er eenduidig uit te halen.

    En een lichte rand: de tekeningen zijn op een witte ondergrond gemaakt, dus
    elke half doorzichtige randpixel draagt een deel wit met zich mee. Op een
    lichte tegel valt dat weg, op een donkere leest het als een wit lijntje om
    het object. Door het wit er weer uit te rekenen -- de kleur die er stond
    ís de kleur van de tekening gemengd met wit -- komt de echte kleur terug en
    blijft de zachte rand gewoon zacht.
    """
    a = np.array(deel).astype(np.int16)
    alfa = a[:, :, 3]
    rgb = a[:, :, :3]

    schaduw = (alfa <= SCHADUW_ALFA) & (rgb.max(axis=2) <= SCHADUW_ZWART)
    alfa = np.where(schaduw, 0, alfa)

    # De kleur terugrekenen: waargenomen = echt * a + wit * (1 - a).
    rand = (alfa > 0) & (alfa < 250)
    f = (alfa / 255.0)[..., None]
    echt = np.where(rand[..., None],
                    np.clip((rgb - 255.0 * (1.0 - f)) / np.maximum(f, 1e-3), 0, 255),
                    rgb)
    uit = np.dstack([echt, alfa]).astype(np.uint8)

    # Zonder schaduw valt de tekening uiteen in wat er echt bij hoort en wat er
    # nog aan spikkels omheen zweeft -- de laatste resten van een bijschrift.
    # Alleen de grote vlekken houden we over.
    vlek = uit[:, :, 3] > 8
    stukken = vlekken(vlek)
    if stukken:
        grootste = max(len(s[4]) for s in stukken)
        houden = [s for s in stukken if len(s[4]) >= grootste * 0.03]
        weg = np.ones(vlek.shape, dtype=bool)
        for s in houden:
            for cy, cx in s[4]:
                weg[cy, cx] = False
        uit[:, :, 3] = np.where(weg, 0, uit[:, :, 3])

    beeld = Image.fromarray(uit, 'RGBA')
    # De uitsnede was op de oude vorm gemaakt, met de schaduw erin. Nu die weg
    # is zou de tekening scheef in zijn vak hangen; opnieuw strak knippen zet
    # hem weer in het midden van zijn eigen omvang.
    vak = beeld.getbbox()
    return beeld.crop(vak) if vak else beeld


def schrijf(im, pad):
    tmp = pad + '.tmp.png'
    im.save(tmp)
    os.replace(tmp, pad)


def main():
    if not os.path.exists(BRON):
        print('bron ontbreekt:', BRON)
        return 1
    vel = wis_bijschriften(Image.open(BRON).convert('RGBA'))
    zicht = np.array(vel)[:, :, 3] > DREMPEL
    os.makedirs(UIT_OVERLAY, exist_ok=True)
    os.makedirs(UIT_OBJECT, exist_ok=True)

    # Wat er nu nog op het vel staat zijn alleen de tekeningen. De overlays
    # vormen de bovenste rij van elf gelijke vierkanten; de acht objecten staan
    # daaronder in twee regels.
    vakken = [(v[0], v[1], v[2], v[3]) for v in vlekken(zicht)
              if (v[2] - v[0]) >= MIN_ZIJDE and (v[3] - v[1]) >= MIN_ZIJDE]
    vakken.sort(key=lambda v: (v[1], v[0]))
    if len(vakken) != len(OVERLAYS) + len(OBJECTEN):
        print('let op: %d tekeningen gevonden, %d verwacht'
              % (len(vakken), len(OVERLAYS) + len(OBJECTEN)))
        for v in vakken:
            print('   ', v, 'b', v[2] - v[0] + 1, 'h', v[3] - v[1] + 1)
        return 1

    rij = sorted(vakken[:len(OVERLAYS)], key=lambda v: v[0])
    for naam, v in zip(OVERLAYS, rij):
        deel = vel.crop((v[0], v[1], v[2] + 1, v[3] + 1))
        deel = deel.resize((OVERLAY_MAAT, OVERLAY_MAAT), Image.LANCZOS)
        schrijf(deel, os.path.join(UIT_OVERLAY, naam + '.png'))
        print('overlay %-9s -> %dx%d' % (naam, OVERLAY_MAAT, OVERLAY_MAAT))

    # De objecten per regel op leesvolgorde: eerst van boven naar beneden
    # groeperen, dan binnen een regel van links naar rechts.
    rest = vakken[len(OVERLAYS):]
    regels = []
    for v in rest:
        gezet = False
        for r in regels:
            if v[1] <= r[0][3] and v[3] >= r[0][1]:
                r.append(v); gezet = True; break
        if not gezet:
            regels.append([v])
    plat = []
    for r in regels:
        plat.extend(sorted(r, key=lambda v: v[0]))
    for naam, v in zip(OBJECTEN, plat):
        deel = schoonmaak(vel.crop((v[0], v[1], v[2] + 1, v[3] + 1)))
        schrijf(deel, os.path.join(UIT_OBJECT, naam + '.png'))
        print('object  %-10s -> %dx%d' % (naam, deel.width, deel.height))
    return 0


if __name__ == '__main__':
    sys.exit(main())
