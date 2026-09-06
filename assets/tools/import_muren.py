# -*- coding: utf-8 -*-
"""Zet de muurstukken -- voorlopig alleen de deuren -- uit
Design Department/60 Repo Sources/MAIN/Muren in de assetbank.

Per stuk komen er drie bestanden uit Photoshop, allemaal 1024 bij 1024:

  Deur Horizontaal.png          het stuk zelf, vrijstaand (met alpha)
  Deur horizontaal Nacht.png    hetzelfde stuk in de nachtkleuren
  Deur Horizontaal Schaduw.png  het stuk mét zijn schaduw, plat op papier

De schaduw wordt er op dezelfde manier uitgerekend als bij de objecten
(schaduwlaag in import_outbox_objects.py).

Het stuk staat klein op zijn doek: een deur is maar een derde van het vlak.
Daarom snijden we het doek bij tot om het stuk heen -- de dag-, nacht- en
schaduwversie krijgen precies dezelfde snede, zodat ze op het bord over
elkaar blijven vallen. De speler meet de lucht om het bord aan alles wat er
op ligt; een groot leeg doek zou dan als lucht meetellen.

Wat de speler moet weten om de plaat op de muur te leggen, wordt hier
uitgerekend en afgedrukt als DEUR_PLAAT: waar de scharnierlijn door de
plaat loopt, waar het midden tussen de knoppen zit, hoe breed de pilaren
buitenom staan en hoe ver de knoppen uit elkaar liggen. De plek van de
knoppen op het oorspronkelijke doek is met de hand gemeten (KNOPPEN); de
rest volgt uit de alpha. Na een nieuwe tekening: draaien, en de afgedrukte
regel in player/index.html plakken.
"""
import os, sys
from PIL import Image

from import_outbox_objects import schaduwlaag, schrijf

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "Design Department", "60 Repo Sources", "MAIN", "Muren")
DOEL = os.path.join(WORTEL, "assets", "art", "walls")
MAAT = 512          # de langste zijde van de bijgesneden plaat
RAND = 8            # lucht om de snede heen, in pixels van het bronbeeld
DREMPEL = 10        # alpha waaronder een pixel als leeg telt

STUKKEN = {
    "door-h": {"dag": "Deur Horizontaal", "nacht": "Deur horizontaal Nacht",
               "schaduw": "Deur Horizontaal Schaduw", "as": "h"},
    "door-v": {"dag": "Deur Verticaal", "nacht": "Deur Verticaal Nacht",
               "schaduw": "Deur Verticaal Schaduw", "as": "v"},
}
# De middelpunten van de twee knoppen, als deel van het doek (x, y). De lijn
# erdoorheen is de scharnierlijn: die legt de speler op de muur.
KNOPPEN = {
    "door-h": ((0.335, 0.388), (0.656, 0.388)),
    "door-v": ((0.500, 0.330), (0.500, 0.659)),
}


def bronpad(naam):
    """Bestandsnaam zonder acht te slaan op hoofdletters: 'Deur horizontaal
    Nacht' en 'Deur Horizontaal' komen uit dezelfde hand."""
    if not os.path.isdir(BRON):
        return None
    for f in os.listdir(BRON):
        if f.lower() == (naam + ".png").lower():
            return os.path.join(BRON, f)
    return None


def alpha_bbox(im):
    a = im.getchannel("A").point(lambda v: 255 if v > DREMPEL else 0)
    return a.getbbox()


def unie(boxen):
    boxen = [b for b in boxen if b]
    return (min(b[0] for b in boxen), min(b[1] for b in boxen),
            max(b[2] for b in boxen), max(b[3] for b in boxen))


def buitenmaat(im, as_, lijn):
    """Hoe ver de pilaren buitenom reiken langs de scharnierlijn: het eerste
    en laatste gevulde punt op die lijn (een bandje van een paar pixels)."""
    a = im.getchannel("A")
    w, h = im.size
    lo, hi = None, None
    for d in range(-3, 4):
        if as_ == "h":
            y = min(h - 1, max(0, int(round(lijn * h)) + d))
            rij = [a.getpixel((x, y)) for x in range(w)]
        else:
            x = min(w - 1, max(0, int(round(lijn * w)) + d))
            rij = [a.getpixel((x, y)) for y in range(h)]
        vol = [i for i, v in enumerate(rij) if v > DREMPEL]
        if vol:
            lo = vol[0] if lo is None else min(lo, vol[0])
            hi = vol[-1] if hi is None else max(hi, vol[-1])
    return lo, hi


def main():
    if not os.path.isdir(BRON):
        print("map ontbreekt:", BRON)
        return 1
    regels = []
    for slug, st in STUKKEN.items():
        dag_pad = bronpad(st["dag"])
        if not dag_pad:
            print("%-8s ontbreekt: %s" % (slug, st["dag"]))
            continue
        dag = Image.open(dag_pad).convert("RGBA")
        nacht_pad = bronpad(st["nacht"])
        nacht = Image.open(nacht_pad).convert("RGBA") if nacht_pad else None
        plat_pad = bronpad(st["schaduw"])
        schaduw = schaduwlaag(dag_pad, plat_pad) if plat_pad else None
        if nacht and nacht.size != dag.size:
            nacht = nacht.resize(dag.size, Image.LANCZOS)
        if schaduw and schaduw.size != dag.size:
            schaduw = schaduw.resize(dag.size, Image.LANCZOS)

        W, H = dag.size
        box = unie([alpha_bbox(dag), alpha_bbox(nacht) if nacht else None,
                    alpha_bbox(schaduw) if schaduw else None])
        box = (max(0, box[0] - RAND), max(0, box[1] - RAND),
               min(W, box[2] + RAND), min(H, box[3] + RAND))
        bw, bh = box[2] - box[0], box[3] - box[1]
        f = MAAT / float(max(bw, bh))
        maat = (max(1, int(round(bw * f))), max(1, int(round(bh * f))))

        def snede(im):
            return im.crop(box).resize(maat, Image.LANCZOS)

        schrijf(snede(dag), os.path.join(DOEL, slug + ".png"))
        regel = "%-8s %dx%d" % (slug, maat[0], maat[1])
        if nacht:
            schrijf(snede(nacht), os.path.join(DOEL, "dark", slug + ".png"))
            regel += "  nacht"
        if schaduw:
            schrijf(snede(schaduw), os.path.join(DOEL, "shadows", slug + ".png"))
            regel += "  schaduw"
        print(regel)

        # De maten voor de speler, als deel van de bijgesneden plaat.
        (x1, y1), (x2, y2) = KNOPPEN[slug]
        if st["as"] == "h":
            lijn = (y1 + y2) / 2.0
            lo, hi = buitenmaat(dag, "h", lijn)
            scharnier = (lijn * H - box[1]) / float(bh)
            midden = ((x1 + x2) / 2.0 * W - box[0]) / float(bw)
            span = (hi - lo + 1) / float(bw)
            knoppen = abs(x2 - x1) * W / float(bw)
        else:
            lijn = (x1 + x2) / 2.0
            lo, hi = buitenmaat(dag, "v", lijn)
            scharnier = (lijn * W - box[0]) / float(bw)
            midden = ((y1 + y2) / 2.0 * H - box[1]) / float(bh)
            span = (hi - lo + 1) / float(bh)
            knoppen = abs(y2 - y1) * H / float(bh)
        regels.append("  %s:{scharnier:%.3f, midden:%.3f, span:%.3f, knoppen:%.3f, hoogte:%.3f}" % (
            st["as"], scharnier, midden, span, knoppen, maat[1] / float(maat[0])))
    if regels:
        print("\nIn player/index.html:\nconst DEUR_PLAAT = {\n" + ",\n".join(regels) + "\n};")
    return 0


if __name__ == "__main__":
    sys.exit(main())
