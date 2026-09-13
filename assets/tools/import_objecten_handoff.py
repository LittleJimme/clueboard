# -*- coding: utf-8 -*-
"""Zet meervaksobjecten uit PNG Asset Pack/Objects in de bank, op het doek dat
de speler verwacht. Tot nu toe: het verbeterde waterrad als watermolen van
twee vakken (liggend 2x1 en staand 1x2) en de waterput van 2x2.

De levering (2026-09-13) staat niet op het doek van de meervakslichting:

  water-wheel-option-01-2x1-white-v1 copy.png     2x1 dag       1224 x 825
  water-wheel-option-01-2x1-white-v1 copy 2.png   2x1 plat+schaduw (RGB)
  water-wheel-option-01-2x1-night-v1.png          2x1 nacht
  Background.png                                  1x2 dag       1024 x 1536
  schaduw.png                                     1x2 plat+schaduw (RGB)
  water-wheel-option-04-1x2-night-v1.png          1x2 nacht

De speler zet een meervakstekening uit de nieuwe lichting neer met de breedte
van haar vak en de voet op de onderrand; de hoogte volgt uit het doek (zie
MEERVAKS_PRODUCTIE in player/index.html). Daarom wordt het rad hier op een
eigen doek gezet, op maat van zijn vak:

  2x1  doek 1024 breed (= twee vakken van 512), het rad 80% van die breedte,
       onderkant 0,12 vak boven de onderrand; de hoogte van het doek volgt,
       zodat het rad boven zijn vak uitsteekt zoals een boom (de oude molen
       deed dat ook).
  1x2  doek 512 x 1024 (precies zijn vak), het rad 80% van de breedte,
       midden in de lengte.
  2x2  (waterput, levering 13:22: "well day/night/shadow.png", 1254x1254)
       doek 1024 breed (twee vakken), de put 82% daarvan, onderkant 0,12 vak
       boven de onderrand, 0,07 vak naar links; de hoogte volgt, zodat de balk
       erboven uitsteekt. De schaduw is breder dan het doek: de laatste 48
       pixels aan beide kanten lopen zacht uit, zodat er geen harde snijrand
       ontstaat.

Dag, nacht en schaduw krijgen exact dezelfde schaal en verschuiving, gemeten
aan de dagtekening. De schaduw wordt eerst op het brondoek uitgerekend met
schaduwlaag() (dezelfde Photoshop-stapel als de rest).
Daarna: python assets/tools/maak_webp.py
"""
import os, sys
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
from import_outbox_objects import schaduwlaag, schrijf

WORTEL = os.path.dirname(os.path.dirname(HIER))
BRON = os.path.join(WORTEL, "Design Department", "50 Handoff to Claude", "PNG Asset Pack", "Objects")
OBJ = os.path.join(WORTEL, "assets", "art", "objects")
VAK = 512

LEVERING = {
    "watermill-2x1": dict(dag="water-wheel-option-01-2x1-white-v1 copy.png",
                          plat="water-wheel-option-01-2x1-white-v1 copy 2.png",
                          nacht="water-wheel-option-01-2x1-night-v1.png",
                          breed=2, hoog=1, deel=0.80, voet=0.12),
    "watermill-1x2": dict(dag="Background.png", plat="schaduw.png",
                          nacht="water-wheel-option-04-1x2-night-v1.png",
                          breed=1, hoog=2, deel=0.80, midden=0.5),
    "well-2x2":      dict(dag="well day.png", plat="well shadow.png", nacht="well night.png",
                          breed=2, hoog=2, deel=0.82, voet=0.12, opzij=-0.07, randzacht=48),
}


def plan(spec, bbox):
    """Schaal, verschuiving en doekmaat, uit de dagtekening."""
    l, t, r, b = bbox
    doekB = spec["breed"] * VAK
    schaal = spec["deel"] * doekB / float(r - l)
    tekeningH = (b - t) * schaal
    # opzij: in vakken; de schaduw van de put valt naar rechts, en zonder
    # dit stukje naar links liep hij over de rand van het doek.
    dx = doekB / 2.0 - (l + r) / 2.0 * schaal + spec.get("opzij", 0) * VAK
    if "voet" in spec:
        onder = spec["voet"] * VAK                      # lucht onder de tekening
        boven = 24                                      # lucht erboven, in pixels
        doekH = int(round(max(spec["hoog"] * VAK, tekeningH + onder + boven)))
        dy = doekH - onder - b * schaal
    else:
        doekH = spec["hoog"] * VAK
        dy = spec["midden"] * doekH - (t + b) / 2.0 * schaal
    return schaal, dx, dy, (doekB, doekH)


def zet(im, schaal, dx, dy, doek):
    im = im.convert("RGBA")
    klein = im.resize((max(1, int(round(im.width * schaal))), max(1, int(round(im.height * schaal)))), Image.LANCZOS)
    uit = Image.new("RGBA", doek, (0, 0, 0, 0))
    uit.alpha_composite(klein, (int(round(dx)), int(round(dy))))
    return uit


def zachteRand(im, breedte):
    """Laat de dekking links en rechts over `breedte` pixels naar nul lopen."""
    a = im.getchannel("A")
    ramp = Image.new("L", (im.width, 1), 255)
    for x in range(breedte):
        v = int(255 * x / float(breedte))
        ramp.putpixel((x, 0), v)
        ramp.putpixel((im.width - 1 - x, 0), v)
    from PIL import ImageChops
    a = ImageChops.multiply(a, ramp.resize(im.size))
    im = im.copy(); im.putalpha(a)
    return im


def main():
    for slug, spec in LEVERING.items():
        pad = lambda n: os.path.join(BRON, n)
        dag = Image.open(pad(spec["dag"])).convert("RGBA")
        schaal, dx, dy, doek = plan(spec, dag.getchannel("A").getbbox())
        schrijf(zet(dag, schaal, dx, dy, doek), os.path.join(OBJ, slug + ".png"))
        schrijf(zet(dag, schaal, dx, dy, doek), os.path.join(OBJ, "medieval", slug + ".png"))
        schrijf(zet(Image.open(pad(spec["nacht"])), schaal, dx, dy, doek), os.path.join(OBJ, "dark", slug + ".png"))
        sch = zet(schaduwlaag(dag, Image.open(pad(spec["plat"])).convert("RGB")), schaal, dx, dy, doek)
        if spec.get("randzacht"):
            sch = zachteRand(sch, spec["randzacht"])
        schrijf(sch, os.path.join(OBJ, "shadows", slug + ".png"))
        print("%s: doek %dx%d, schaal %.3f" % (slug, doek[0], doek[1], schaal))


if __name__ == "__main__":
    main()
