# -*- coding: utf-8 -*-
"""Zet het verbeterde waterrad uit PNG Asset Pack/Objects in de bank, als
watermolen van twee vakken (liggend 2x1 en staand 1x2).

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
}


def plan(spec, bbox):
    """Schaal, verschuiving en doekmaat, uit de dagtekening."""
    l, t, r, b = bbox
    doekB = spec["breed"] * VAK
    schaal = spec["deel"] * doekB / float(r - l)
    tekeningH = (b - t) * schaal
    dx = doekB / 2.0 - (l + r) / 2.0 * schaal
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


def main():
    for slug, spec in LEVERING.items():
        pad = lambda n: os.path.join(BRON, n)
        dag = Image.open(pad(spec["dag"])).convert("RGBA")
        schaal, dx, dy, doek = plan(spec, dag.getchannel("A").getbbox())
        schrijf(zet(dag, schaal, dx, dy, doek), os.path.join(OBJ, slug + ".png"))
        schrijf(zet(dag, schaal, dx, dy, doek), os.path.join(OBJ, "medieval", slug + ".png"))
        schrijf(zet(Image.open(pad(spec["nacht"])), schaal, dx, dy, doek), os.path.join(OBJ, "dark", slug + ".png"))
        sch = schaduwlaag(dag, Image.open(pad(spec["plat"])).convert("RGB"))
        schrijf(zet(sch, schaal, dx, dy, doek), os.path.join(OBJ, "shadows", slug + ".png"))
        print("%s: doek %dx%d, schaal %.3f" % (slug, doek[0], doek[1], schaal))


if __name__ == "__main__":
    main()
