# -*- coding: utf-8 -*-
"""Snijdt een tegelblad uit tot losse vloertexturen voor de player.

Het blad is een raster van tegels met een bijschrift eronder, op een creme
ondergrond, met per tegel een afgeronde hoek, een donkere omlijning en een
slagschaduw. Die drie dingen moeten er juist AF: op het bord staan de vakjes
tegen elkaar aan, dus wat we willen is alleen het materiaal.

De player koppelt op bestandsnaam (assets/art/backgrounds/<thema>/floor-<id>.png,
zie applyFloorArt + withThemeFallback); er hoeft dus niets in het manifest --
behalve het aantal varianten, dat staat in manifest.json onder floorArt.

Gebruik:  python assets/tools/snij_vloertegels.py <blad>
          blad = "set1" of "set3" (zie BLADEN hieronder)
"""
import os
import sys

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HIER)
DOEL = os.path.join(ASSETS, "art", "backgrounds", "medieval")
INBOX = os.path.join(ASSETS, "render", "inbox")

MAAT = 256      # ruim boven de celgrootte op het scherm

# Twee manieren van uitsnijden:
#   "vlak"    binnen de omlijning snijden, zodat aangrenzende vakjes in elkaar
#             overlopen tot een doorlopende vloer (bladen 1 en 2)
#   "tegel"   de tegel met zijn rand en reliëf laten staan, zodat elk vakje
#             als eigen tegel leest en het raster zichtbaar wordt (blad 3)
INSET_VLAK = 15
INSET_TEGEL = 1
HOEKSTRAAL = 0.03   # afronding van de tegelhoek, als deel van de zijde

# Per blad: het bronbestand en de namen, rij voor rij, links naar rechts.
# Een naam die eindigt op -2, -3, ... is een variant van dezelfde vloer; de
# player wisselt ze af zodat twee kamers met hetzelfde materiaal toch van
# elkaar te onderscheiden zijn. Namen zonder vloer-id staan klaar voor het
# geval er een vloersoort bij komt.
BLADEN = {
    # Eerste blad: 3x6, één tegel per materiaal.
    "set1": ("vloertegels-blad.png", [
        ["grass", "dirt",     "sand",           "steen-licht", "stone",       "steen-donker"],
        ["keien", "gravel",   "hout-licht",     "wood",        "hout-donker", "parket"],
        ["tile",  "baksteen", "pleister-licht", "concrete",    "leem",        "leisteen"],
    ]),
    # Derde blad: dezelfde varianten, maar nu met reliëf op elke tegel. Deze
    # worden mét hun rand uitgesneden, zodat het raster zichtbaar blijft.
    "set3": ("vloertegels-relief.png", [
        ["grass", "grass-2", "grass-3", "grass-4", "grass-5", "grass-6"],
        ["stone", "stone-2", "stone-3", "stone-4",
         "sand",  "sand-2",  "dirt",    "gravel"],
        ["wood",  "wood-2",  "wood-3",  "wood-4",  "water"],
    ]),
}


def helder(px):
    return (px[0] + px[1] + px[2]) / 3.0


def blokken(profiel, minlengte, drempel):
    """Aaneengesloten stukken waar het profiel boven de drempel ligt."""
    uit, start = [], None
    for i, v in enumerate(profiel):
        if v > drempel and start is None:
            start = i
        elif v <= drempel and start is not None:
            if i - start >= minlengte:
                uit.append((start, i - 1))
            start = None
    if start is not None and len(profiel) - start >= minlengte:
        uit.append((start, len(profiel) - 1))
    return uit


def rand(im, vast, bereik, as_x, omgekeerd):
    """De scherpste donkere sprong: dat is de omlijning van de tegel."""
    beste, bestev, vorig = None, -1, None
    reeks = list(bereik)[::-1] if omgekeerd else list(bereik)
    for i in reeks:
        h = helder(im.getpixel((i, vast) if as_x else (vast, i)))
        if vorig is not None and vorig - h > bestev:
            bestev, beste = vorig - h, i
        vorig = h
    return beste


def hoekmasker(maat, straal):
    """Alfamasker met licht afgeronde hoeken, zodat er geen crème van het blad
       in de hoeken van de tegel blijft staan. Wat daar doorschijnt is de
       kleur van de ruimte -- dat maakt het raster juist duidelijker."""
    from PIL import ImageDraw
    m = Image.new("L", (maat, maat), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, maat - 1, maat - 1),
                                        radius=max(1, int(maat * straal)), fill=255)
    return m


def main(blad):
    bestand, plan = BLADEN[blad]
    tegelvorm = (blad == "set3")
    inset = INSET_TEGEL if tegelvorm else INSET_VLAK
    im = Image.open(os.path.join(INBOX, bestand)).convert("RGB")
    w, h = im.size
    grond = im.getpixel((5, 5))

    def afwijkt(px, d=26):
        return max(abs(px[i] - grond[i]) for i in range(3)) > d

    rij = [sum(1 for x in range(0, w, 4) if afwijkt(im.getpixel((x, y)))) for y in range(h)]
    banden = blokken(rij, 60, 10)
    if len(banden) != len(plan):
        sys.exit("%d rijbanden gevonden, %d verwacht." % (len(banden), len(plan)))

    os.makedirs(DOEL, exist_ok=True)
    for ri, (y0, y1) in enumerate(banden):
        ym = (y0 + y1) // 2
        kol = [sum(1 for y in range(y0, y1, 3) if afwijkt(im.getpixel((x, y)))) for x in range(w)]
        kolommen = blokken(kol, 80, 4)
        if len(kolommen) != len(plan[ri]):
            sys.exit("Rij %d: %d tegels gevonden, %d verwacht."
                     % (ri + 1, len(kolommen), len(plan[ri])))
        for ci, (x0, x1) in enumerate(kolommen):
            xm = (x0 + x1) // 2
            l = rand(im, ym, range(x0 - 6, x0 + 18), True, False)
            r = rand(im, ym, range(x1 - 18, x1 + 6), True, True)
            t = rand(im, xm, range(y0 - 6, y0 + 18), False, False)
            # Tegels zijn vierkant; de breedte is de maat. De onderrand valt
            # samen met de slagschaduw en is daar niet betrouwbaar voor.
            zij = r - l
            vak = (l + inset, t + inset, l + zij - inset, t + zij - inset)
            tegel = im.crop(vak).resize((MAAT, MAAT), Image.LANCZOS)
            if tegelvorm:
                tegel = tegel.convert("RGBA")
                tegel.putalpha(hoekmasker(MAAT, HOEKSTRAAL))
            naam = "floor-%s.png" % plan[ri][ci]
            tegel.save(os.path.join(DOEL, naam), optimize=True)
            print("geschreven:", naam)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in BLADEN:
        sys.exit(__doc__)
    main(sys.argv[1])
