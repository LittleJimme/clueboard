# -*- coding: utf-8 -*-
"""Knip de objectbibliotheek uit tot losse tekeningen met hun contactschaduw.

Bron: assets/art/concepts/clueboard-medieval-object-library-white-spaced-v2.png
Achttien objecten op een witte ondergrond, met bijschrift en formaat eronder.

Wit wegpoetsen is hier niet één regel. Een tekening staat op wit, dus elke half
doorzichtige randpixel draagt wit met zich mee; en de contactschaduw is niets
anders dan datzelfde wit, een tikje donkerder. Die twee moeten verschillend
behandeld worden:

  * de tekening zelf wordt dekkend, met het wit uit de rand teruggerekend;
  * de schaduw wordt juist doorzichtig zwart, precies zo diep als hij donker
    was -- zo blijft hij een schaduw en wordt hij geen grijze vlek zodra hij op
    een gekleurde tegel ligt.

Om die twee uit elkaar te houden zoeken we eerst de vaste kern van elke
tekening (duidelijk donkerder dan de ondergrond) en vullen we de gaten daarin.
Wat daarbinnen valt is tekening; wat erbuiten nog van wit afwijkt is schaduw.
Zo blijven ook de lichte rotsblokken en het lichte standbeeld gewoon dekkend.

Draaien:  python assets/tools/cut_object_library.py
"""
import os
import sys
from collections import deque

import numpy as np
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONCEPTEN = os.path.join(WORTEL, 'assets', 'art', 'concepts')
UIT = os.path.join(WORTEL, 'assets', 'art', 'objects')
THEMA = os.path.join(UIT, 'medieval')

# De tekeningen in leesvolgorde per vel, met de naam waaronder de player ze
# zoekt. De Nederlandse naam op het vel staat erachter ter herkenning. Staat er
# een lijstje, dan wordt dezelfde tekening onder meerdere namen weggeschreven.
BASIS = [
    'chair',        # STOEL
    'barrel',       # TON
    'shelf',        # BOEKENKAST
    'tree',         # BOOM
    'shrub',        # STRUIK
    'table',        # TAFEL
    'horse',        # PAARD
    'stones',       # ROTSBLOKKEN
    'crate',        # KIST
    'vase',         # VAAS
    'statue',       # STANDBEELD
    'puddle',       # MODDERPLAS
    'treasure',     # SCHATKIST
    ['weapon-rack', 'weapon-chest'],  # WAPENREK -- de bank kent alleen een
                            #   Wapenkist; tot die er is staat het rek daarvoor
    'table-2x1',    # TAFEL HORIZONTAAL
    'table-1x2',    # TAFEL VERTICAAL
    'bed-2x1',      # BED HORIZONTAAL
    'bed-1x2',      # BED VERTICAAL
]

METGEZEL = [
    'easel',        # SCHILDERSEZEL
    'loom',         # WEEFGETOUW
    'boar',         # EVERZWIJN
    'cow',          # KOE
    'pig',          # VARKEN
    'wolf',         # WOLF
    'plant',        # PLANT IN VAAS
    'box',          # DOOS
    'sack',         # ZAK
    'rubble',       # PUIN
    'house',        # HUISJE
    'well',         # WATERPUT
    'bench-2x1',    # BANKJE HORIZONTAAL
    'boat-2x1',     # BOOT HORIZONTAAL
    'catapult-2x1',  # KATAPULT HORIZONTAAL
    'watermill-2x1',  # WATERRAD HORIZONTAAL
    'bench-1x2',    # BANKJE VERTICAAL
    'boat-1x2',     # BOOT VERTICAAL
    'catapult-1x2',  # KATAPULT VERTICAAL
    'watermill-1x2',  # WATERRAD VERTICAAL
]

# Vel, namenlijst, en de map waar het heen gaat. De nachtversie van de eerste
# batch gaat naar een eigen map, zodat de player er in de donkere stand naar
# kan grijpen zonder dat de dagtekeningen eronder verdwijnen.
VELLEN = [
    ('clueboard-medieval-object-library-white-spaced-v2.png', BASIS, None),
    ('clueboard-medieval-object-library-companion-white-v2-diagonal-animals.png', METGEZEL, None),
    # Het nachtvel staat klaar maar wordt nog niet gesneden: de donkerste
    # onderdelen -- een boomstam, een tafelpoot, de onderkant van een ton --
    # verschillen daar te weinig van de bijna zwarte ondergrond om ze er
    # betrouwbaar uit te halen. Zodra het vel op een middengrijze ondergrond
    # staat, of met een echt alfakanaal, hoeft deze regel alleen terug.
    # ('clueboard-medieval-object-library-night-proposal-v1.png', BASIS, 'medieval-nacht'),
]

KERN = 45            # zoveel donkerder dan wit is zeker tekening
KERN_DONKER = 3      # op het nachtvel steken de tekeningen minder af
RAND_VAN = 8         # waar de zachte rand van de tekening begint
RAND_TOT = 34        # en waar hij dekkend is
SCHADUW_MAX = 0.42   # hoe diep de contactschaduw hoogstens wordt
TEKST_ZWART = 90     # zo donker is alleen een bijschrift
TEKST_HOOG = 30      # en zo laag is een regel tekst
MIN_ZIJDE = 40       # kleiner dan dit is geen tekening
SPELING = 22         # zo dicht bij elkaar hoort bij dezelfde tekening


def tekstregels(luma, donker=False, achter=254):
    """De regels waarop bijschriften staan, als (van, tot)."""
    inkt = (luma > achter + 90) if donker else (luma < TEKST_ZWART)
    zwart = inkt.sum(axis=1)
    banden, start = [], None
    for y in range(len(zwart)):
        if zwart[y] > 0 and start is None:
            start = y
        elif zwart[y] == 0 and start is not None:
            banden.append((start, y - 1))
            start = None
    if start is not None:
        banden.append((start, len(zwart) - 1))
    return [b for b in banden if (b[1] - b[0] + 1) <= TEKST_HOOG]


def vulGaten(kern):
    """Alles wat door de kern is ingesloten hoort bij de tekening.

    We lopen vanaf de rand van het vel door alles wat géén kern is; wat we niet
    bereiken zit erin opgesloten. Zo wordt een rotsblok met alleen donkere
    contouren toch een dicht vlak.
    """
    h, b = kern.shape
    buiten = np.zeros_like(kern)
    rij = deque()
    for x in range(b):
        for y in (0, h - 1):
            if not kern[y, x] and not buiten[y, x]:
                buiten[y, x] = True
                rij.append((y, x))
    for y in range(h):
        for x in (0, b - 1):
            if not kern[y, x] and not buiten[y, x]:
                buiten[y, x] = True
                rij.append((y, x))
    while rij:
        cy, cx = rij.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < b and not kern[ny, nx] and not buiten[ny, nx]:
                buiten[ny, nx] = True
                rij.append((ny, nx))
    return ~buiten


def groei(masker, stappen=2):
    uit = masker.copy()
    for _ in range(stappen):
        g = uit.copy()
        g[1:, :] |= uit[:-1, :]
        g[:-1, :] |= uit[1:, :]
        g[:, 1:] |= uit[:, :-1]
        g[:, :-1] |= uit[:, 1:]
        uit = g
    return uit


def vlekken(masker, minzijde):
    """Losse vlekken met hun omvang, groter dan minzijde."""
    h, b = masker.shape
    gezien = np.zeros_like(masker)
    uit = []
    for y in range(h):
        for x in range(b):
            if not masker[y, x] or gezien[y, x]:
                continue
            rij = deque([(y, x)])
            gezien[y, x] = True
            minx = maxx = x
            miny = maxy = y
            n = 0
            while rij:
                cy, cx = rij.popleft()
                n += 1
                if cx < minx: minx = cx
                if cx > maxx: maxx = cx
                if cy < miny: miny = cy
                if cy > maxy: maxy = cy
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < b and masker[ny, nx] and not gezien[ny, nx]:
                        gezien[ny, nx] = True
                        rij.append((ny, nx))
            if (maxx - minx + 1) >= minzijde and (maxy - miny + 1) >= minzijde:
                uit.append((minx, miny, maxx, maxy, n))
    return uit


def smeltSamen(vakken, speling):
    """Vlekken die dicht bij elkaar liggen horen bij dezelfde tekening.

    Op het nachtvel steekt niet elk onderdeel even ver boven de ondergrond uit,
    waardoor een stoel uiteen kan vallen in een zitting en twee poten. Ze staan
    op het vel ruim uit elkaar, dus wat elkaar bijna raakt hoort bij elkaar.
    """
    vakken = [list(v[:4]) + [v[4]] for v in vakken]
    veranderd = True
    while veranderd:
        veranderd = False
        for i in range(len(vakken)):
            for j in range(len(vakken) - 1, i, -1):
                a, b = vakken[i], vakken[j]
                if (a[0] - speling <= b[2] and b[0] - speling <= a[2]
                        and a[1] - speling <= b[3] and b[1] - speling <= a[3]):
                    a[0] = min(a[0], b[0]); a[1] = min(a[1], b[1])
                    a[2] = max(a[2], b[2]); a[3] = max(a[3], b[3])
                    a[4] += b[4]
                    vakken.pop(j)
                    veranderd = True
    return [tuple(v) for v in vakken]


def schrijf(im, pad):
    tmp = pad + '.tmp.png'
    im.save(tmp)
    os.replace(tmp, pad)


def snij(bestand, NAMEN, submap):
    bron = os.path.join(CONCEPTEN, bestand)
    if not os.path.exists(bron):
        print('bron ontbreekt:', bron)
        return 1
    rgb = np.array(Image.open(bron).convert('RGB')).astype(np.int16)
    # De ondergrond is bijna wit, maar niet op elk vel even wit -- en het
    # nachtvel staat juist op bijna zwart. De toon van de ondergrond meten we
    # dus gewoon op, en alles daarna rekent met "hoe ver van de ondergrond af".
    ACHTER = int(np.median(rgb.reshape(-1, 3).mean(axis=1)))
    donker = ACHTER < 128
    luma = rgb.mean(axis=2)

    # 1. De bijschriften weg: die regels worden gewoon weer ondergrond.
    for y0, y1 in tekstregels(luma, donker, ACHTER):
        rgb[y0:y1 + 1] = ACHTER
    luma = rgb.mean(axis=2)

    # Hoe ver van de ondergrond af. Op wit is dat het donkerste kanaal, op
    # zwart juist het lichtste.
    afstand = (rgb.max(axis=2) - ACHTER) if donker else (ACHTER - rgb.min(axis=2))

    # 2. De vaste kern van elke tekening, met de gaten erin gevuld.
    # Op het nachtvel liggen de tekeningen dichter bij hun ondergrond dan op
    # het witte vel, dus daar moet de grens lager liggen -- anders valt een
    # stoel uiteen in losse latjes.
    drempel = KERN_DONKER if donker else KERN
    kern = vulGaten(afstand > drempel)
    tekening = groei(kern, 2)               # de zachte rand hoort er ook bij

    # 3. De alfalaag opbouwen.
    hoogte, breedte = luma.shape
    kleur = rgb.astype(np.float32)
    alfa = np.zeros((hoogte, breedte), dtype=np.float32)

    # De tekening: binnen de kern altijd volledig dekkend, ook waar de kleur
    # licht is. Anders zouden lichte partijen -- de hooglichten in een boomkruin
    # bijvoorbeeld -- doorzichtig worden, en dat leest als een gat in het blad.
    # Alleen de smalle rand rond de kern loopt zacht af naar niets.
    fel = np.clip((afstand - RAND_VAN) / float(RAND_TOT - RAND_VAN), 0, 1)
    alfa = np.where(tekening, np.where(kern, 1.0, fel), alfa)
    veilig = np.maximum(alfa, 1e-3)[..., None]
    kleur = np.where(tekening[..., None],
                     np.clip((rgb - ACHTER * (1 - veilig)) / veilig, 0, 255),
                     kleur)

    # De schaduw: alles buiten de tekening dat toch van wit afwijkt. Hoe donker
    # het was, zo diep wordt de schaduw -- en warm donker in plaats van grijs,
    # zodat hij bij het bord past.
    # Op het nachtvel is de schaduw donkerder dan de al donkere ondergrond en
    # levert hij niets op; daar laten we hem weg.
    if not donker:
        schaduw = (~tekening) & (luma < ACHTER - 1)
        diep = np.clip((ACHTER - luma) / 255.0, 0, SCHADUW_MAX)
        alfa = np.where(schaduw, diep, alfa)
        kleur = np.where(schaduw[..., None], np.array([58.0, 48.0, 38.0]), kleur)

    beeld = np.dstack([kleur, alfa * 255.0]).astype(np.uint8)
    vel = Image.fromarray(beeld, 'RGBA')

    # 4. De losse tekeningen opzoeken en wegschrijven. Alleen de kern telt mee
    #    voor het vinden; de schaduw hoort bij de tekening die erboven staat.
    vakken = smeltSamen(vlekken(kern, 8), SPELING)
    vakken = [v for v in vakken
              if (v[2] - v[0] + 1) >= MIN_ZIJDE and (v[3] - v[1] + 1) >= MIN_ZIJDE]
    if len(vakken) != len(NAMEN):
        print('let op: %d tekeningen gevonden, %d verwacht' % (len(vakken), len(NAMEN)))
        for v in sorted(vakken, key=lambda v: (v[1], v[0])):
            print('   ', v[:4], 'b', v[2] - v[0] + 1, 'h', v[3] - v[1] + 1)
        return 1
    vakken.sort(key=lambda v: v[1])
    regels = []
    for v in vakken:
        gezet = False
        for r in regels:
            if v[1] <= r[0][3] and v[3] >= r[0][1]:
                r.append(v); gezet = True; break
        if not gezet:
            regels.append([v])
    plat = []
    for r in regels:
        plat.extend(sorted(r, key=lambda v: v[0]))

    doelen = [UIT, THEMA] if not submap else [os.path.join(UIT, submap)]
    for d in doelen:
        os.makedirs(d, exist_ok=True)
    heel = np.array(vel)
    for namen, v in zip(NAMEN, plat):
        namen = namen if isinstance(namen, list) else [namen]
        # Ruim om de kern heen knippen, zodat de schaduw meekomt, en daarna
        # strak op wat er werkelijk staat.
        marge = 40
        x0 = max(0, v[0] - marge); y0 = max(0, v[1] - marge)
        x1 = min(breedte, v[2] + 1 + marge); y1 = min(hoogte, v[3] + 1 + marge)
        deel = Image.fromarray(heel[y0:y1, x0:x1], 'RGBA')
        # Van een bijschrift blijft soms nog een spikkel antialiasing over, net
        # buiten de regel die we wit hebben gemaakt. Alles wat losstaat van de
        # tekening en verwaarloosbaar klein is, gaat weg.
        d = np.array(deel)
        # Op het nachtvel niet opruimen: daar zijn de donkerste onderdelen --
        # een boomstam, een tafelpoot -- losse stukjes die maar net van de
        # ondergrond verschillen. Weggooien zou het object slopen.
        stukken = vlekken(d[:, :, 3] > 6, 1)
        # Op het nachtvel ligt de grens lager: daar zijn de donkerste
        # onderdelen -- een boomstam, een tafelpoot -- maar net van de
        # ondergrond te onderscheiden, en die horen er wel bij. Wat overblijft
        # is korrel in de ondergrond zelf.
        ondergrens = 0.004 if donker else 0.02
        if stukken:
            grootste = max(s[4] for s in stukken)
            for s in stukken:
                if s[4] < grootste * ondergrens:
                    d[s[1]:s[3] + 1, s[0]:s[2] + 1, 3] = 0
            deel = Image.fromarray(d, 'RGBA')
        vak = deel.getbbox()
        if vak:
            deel = deel.crop(vak)
        for naam in namen:
            for d in doelen:
                schrijf(deel, os.path.join(d, naam + '.png'))
        print('  %-24s -> %dx%d' % (', '.join(namen), deel.width, deel.height))
    return 0


def main():
    for bestand, namen, submap in VELLEN:
        print(bestand)
        fout = snij(bestand, namen, submap)
        if fout:
            return fout
    return 0


if __name__ == '__main__':
    sys.exit(main())
