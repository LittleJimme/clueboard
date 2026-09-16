# -*- coding: utf-8 -*-
"""Modulaire tafels (Tables Modular Day v3) inladen.

De ontwerper levert 47 bladdelen van 256x256 (een per aansluitcode, de hex
van het buurmasker) en een losse poot van 48x72. De speler zet per tafel-
object de juiste delen naast elkaar en tekent de poten eronder, in een
canvas per tafel (zie tekenTafel in player/index.html). Hier komen de PNG's
als WebP in assets/art/objects/tables/ terecht; de oude vaste tafeltekeningen
(table.png, table-1x2, ...) vervallen.

    python assets/tools/import_tafels_modulair.py
"""
import io, os, sys, time
from PIL import Image

WORTEL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BRON = os.path.join(WORTEL, "Design Department", "50 Handoff to Claude", "PNG Asset Pack",
                    "Objects", "Tables Modular Day v3")
DOEL = os.path.join(WORTEL, "assets", "art", "objects", "tables")
OUD = os.path.join(WORTEL, "assets", "art", "objects", "medieval")
KWALITEIT = 92

def schrijf(pad, beeld):
    tmp = pad + ".tmp"
    buf = io.BytesIO()
    beeld.save(buf, "WEBP", quality=KWALITEIT, method=6, exact=True)
    with open(tmp, "wb") as f:
        f.write(buf.getvalue())
    for _ in range(5):
        try:
            os.replace(tmp, pad); return
        except PermissionError:
            time.sleep(0.5)
    raise SystemExit("Kon niet schrijven: " + pad)

# Het hout van de kit is oranjer en feller dan dat van het bed (tint 30 tegen
# 38 graden, verzadiging .79 tegen .48). De bladdelen en de poot worden bij het
# inladen in HSV bijgekleurd, zodat tafel, bed en stoel hetzelfde hout lijken.
TINT_GRADEN, VERZADIGING, HELDERHEID = 8.0, 0.66, 0.88

def kleur_bij(im):
    import colorsys
    px = im.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            hh = (hh + TINT_GRADEN / 360) % 1.0
            ss = min(1.0, ss * VERZADIGING); vv = min(1.0, vv * HELDERHEID)
            r2, g2, b2 = colorsys.hsv_to_rgb(hh, ss, vv)
            px[x, y] = (round(r2 * 255), round(g2 * 255), round(b2 * 255), a)
    return im

def main():
    if not os.path.isdir(BRON):
        raise SystemExit("Bron niet gevonden: " + BRON)
    os.makedirs(DOEL, exist_ok=True)
    n = 0
    for naam in sorted(os.listdir(os.path.join(BRON, "modules"))):
        if not naam.lower().endswith(".png"):
            continue
        im = Image.open(os.path.join(BRON, "modules", naam)).convert("RGBA")
        if im.size != (256, 256):
            raise SystemExit("Onverwachte maat %s: %s" % (naam, im.size))
        schrijf(os.path.join(DOEL, naam[:-4] + ".webp"), kleur_bij(im)); n += 1
    poot = Image.open(os.path.join(BRON, "supports", "leg-day.png")).convert("RGBA")
    if poot.size != (48, 72):
        raise SystemExit("Onverwachte pootmaat: %s" % (poot.size,))
    schrijf(os.path.join(DOEL, "leg-day.webp"), kleur_bij(poot)); n += 1
    print("geschreven:", n, "bestanden in", DOEL)
    # De oude vaste tafels vervallen.
    weg = 0
    for naam in os.listdir(OUD):
        stam = naam.rsplit(".", 1)[0]
        if stam == "table" or stam.startswith("table-"):
            os.remove(os.path.join(OUD, naam)); weg += 1
    sch = os.path.join(WORTEL, "assets", "art", "objects", "shadows")
    if os.path.isdir(sch):
        for naam in os.listdir(sch):
            stam = naam.rsplit(".", 1)[0]
            if stam == "table" or stam.startswith("table-"):
                os.remove(os.path.join(sch, naam)); weg += 1
    print("oude tafels verwijderd:", weg)

if __name__ == "__main__":
    main()
