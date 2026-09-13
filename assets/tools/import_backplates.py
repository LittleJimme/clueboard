# -*- coding: utf-8 -*-
"""Zet de achterplaten van edele en ridder (banier en schild) in de bank.

Bron: Design Department/50 Handoff to Claude/PNG Asset Pack/UI/Backplates.
Sinds de levering van 2026-09-13 (character style v3) zijn banier en schild
precies even groot, en komt elke vorm in twee delen op hetzelfde doek van 512:

  edele-banier-character-style-v3 copy.png   -> ui/banier-rand.png  (de gouden rand)
  edele-banier-character-style-v3.png        -> ui/banier-vlak.png  (het binnenvlak met vouw)
  ridder-schild-character-style-v3 copy.png  -> ui/schild-rand.png  (de stalen rand)
  ridder-schild-character-style-v3.png       -> ui/schild-vlak.png

Het binnenvlak valt precies in de opening van de rand. Daaruit volgen ook:

  ui/masker-<vorm>.png   wit waar het binnenvlak ligt; knipt het lijf en de
                         persoonstint in de vorm
  ui/<vorm>.png          rand en vlak samen, de hele plaat (naslag)

De speler en de bouwer leggen het vlak in de lichte tint van de persoon
(vermenigvuldigd, zodat de vouw blijft), het lijf erop en de rand erover.
Daarna: python assets/tools/maak_webp.py
"""
import os
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "Design Department", "50 Handoff to Claude", "PNG Asset Pack", "UI", "Backplates")
DOEL = os.path.join(WORTEL, "assets", "characters", "ui")
MAAT = (512, 512)

VORMEN = {
    "banier": "edele-banier-character-style-v3",
    "schild": "ridder-schild-character-style-v3",
}


def schrijf(im, pad):
    tmp = pad + ".tmp"
    im.save(tmp, "PNG", optimize=True)
    os.replace(tmp, pad)


def laad(naam):
    im = Image.open(os.path.join(BRON, naam)).convert("RGBA")
    if im.size != MAAT:
        raise SystemExit("%s is %dx%d, verwacht %dx%d" % ((naam,) + im.size + MAAT))
    return im


for vorm, stam in VORMEN.items():
    rand = laad(stam + " copy.png")
    vlak = laad(stam + ".png")
    alfa = vlak.getchannel("A")
    masker = Image.new("RGBA", MAAT, (255, 255, 255, 0))
    masker.putalpha(alfa)
    plaat = vlak.copy()
    plaat.alpha_composite(rand)
    schrijf(rand, os.path.join(DOEL, vorm + "-rand.png"))
    schrijf(vlak, os.path.join(DOEL, vorm + "-vlak.png"))
    schrijf(masker, os.path.join(DOEL, "masker-" + vorm + ".png"))
    schrijf(plaat, os.path.join(DOEL, vorm + ".png"))
    print("%s: rand %s, vlak %s" % (vorm, rand.getbbox(), alfa.getbbox()))
