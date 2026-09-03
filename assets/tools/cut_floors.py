"""Snijdt de vloertegels uit het goedgekeurde stijlvel.

Bron: assets/art/concepts/clueboard-light-floor-foundations-style-sheet-v3-
imagegen-light-reference.png -- daarin staat elk materiaal als één losse tegel
van 1:1, met de belichting die het spel moet krijgen: zacht licht langs boven
en links, warme schaduw langs onder en rechts, een heel ondiepe bevel en een
brede lichtval van linksboven naar rechtsonder.

Elke tegel wordt uitgesneden met zijn eigen rand, op 128x128 gezet en krijgt
doorzichtige hoeken. Die ronde hoeken zijn met opzet: leg je vier tegels tegen
elkaar, dan blijft er in het midden een klein vlekje van de ondergrond staan.
Dat leest als vier losse tegels die tegen elkaar aan liggen, precies zoals in
het stijlvel.

De maten hieronder zijn opgemeten in de bron: per tegel de linkerrand, de
bovenrand en de plek waar zijn slagschaduw begint.

Draaien:  python assets/tools/cut_floors.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter

MAAT = 128          # bronmaat van een gameplayvakje
RONDING = 7         # ronde hoek, zodat vier tegels elkaar niet dichtplakken
MARGE = 6           # de lichte rand valt net buiten de meting

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "assets", "art", "concepts",
                    "clueboard-light-floor-foundations-style-sheet-v3-imagegen-light-reference.png")
UIT = os.path.join(WORTEL, "assets", "art", "backgrounds", "foundations")

# vloer-id -> (linkerrand, bovenrand, begin slagschaduw rechts) in de bron
TEGELS = {
    # gedeelde minerale basis
    "stone":    (298, 149, 492),   # limestone
    "concrete": (529, 149, 722),   # plaster
    "tile":     (760, 149, 954),   # glazed slab
    "marble":   (990, 149, 1185),  # pale marble
    # gedeelde aardebasis
    "dirt":     (390, 427, 588),   # earth
    "sand":     (637, 427, 836),   # sand
    "gravel":   (882, 427, 1079),  # fine gravel
    # eigen structuur
    "wood":     (291, 710, 491),   # light wood
    "grass":    (522, 710, 719),   # soft grass
    "carpet":   (752, 710, 952),   # linen / felt
    "water":    (982, 710, 1184),  # shallow water
}


def masker(maat, straal):
    """Rechthoek met ronde hoeken, met een zachte rand van een halve pixel."""
    groot = maat * 4
    m = Image.new("L", (groot, groot), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, groot - 1, groot - 1],
                                        radius=straal * 4, fill=255)
    return m.resize((maat, maat), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.4))


def main():
    if not os.path.exists(BRON):
        raise SystemExit("Bron niet gevonden: " + BRON)
    os.makedirs(UIT, exist_ok=True)
    bron = Image.open(BRON).convert("RGB")
    m = masker(MAAT, RONDING)
    for naam, (l, t, r) in TEGELS.items():
        x0, y0 = l - MARGE, t - MARGE
        zij = r - x0                      # de tegel is vierkant
        tegel = bron.crop((x0, y0, x0 + zij, y0 + zij)).resize((MAAT, MAAT), Image.LANCZOS)
        uit = tegel.convert("RGBA")
        uit.putalpha(m)
        pad = os.path.join(UIT, naam + ".png")
        uit.save(pad, optimize=True)
        print("%-9s %3dpx uit de bron  ->  %s" % (naam, zij, os.path.relpath(pad, WORTEL).replace("\\", "/")))
    print("%d tegels, %dx%d, hoekronding %dpx" % (len(TEGELS), MAAT, MAAT, RONDING))


if __name__ == "__main__":
    main()
