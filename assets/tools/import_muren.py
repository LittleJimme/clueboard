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

Een deur bestaat uit twee knoppen (de pilaren) op één lijn -- de
scharnierlijn, die de speler op de muur legt -- en een blad dat aan de eerste
knop hangt. De tweede knop staat vrij; daaraan wordt gemeten hoe groot de
knoppen zijn en waar de lijn precies loopt. Die vrije knop gaat ook los de
bank in: de speler kleurt hem ter plekke in de kleur van de muur (zoals de
shirts van de personages) en legt hem over de stalen knoppen van de plaat,
zodat de pilaren altijd de kleur van hun muur hebben -- overdag, 's nachts
en op een gouden muur.

Wat de speler moet weten om de plaat op de muur te leggen wordt hier
uitgerekend en afgedrukt als DEUR_PLAAT. Na een nieuwe tekening: draaien,
en de afgedrukte regels in player/index.html plakken.
"""
import os, sys
from PIL import Image, ImageDraw

from import_outbox_objects import schaduwlaag, schrijf

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "Design Department", "60 Repo Sources", "MAIN", "Muren")
DOEL = os.path.join(WORTEL, "assets", "art", "walls")
MAAT = 512          # de langste zijde van de bijgesneden plaat
KNOP_MAAT = 128     # de losse knop
RAND = 8            # lucht om de snede heen, in pixels van het bronbeeld
DREMPEL = 10        # alpha waaronder een pixel als leeg telt

STUKKEN = {
    "door-h": {"dag": "Deur Horizontaal", "nacht": "Deur horizontaal Nacht",
               "schaduw": "Deur Horizontaal Schaduw", "as": "h", "lijn": 0.39},
    "door-v": {"dag": "Deur Verticaal", "nacht": "Deur Verticaal Nacht",
               "schaduw": "Deur Verticaal Schaduw", "as": "v", "lijn": 0.50},
}
# 'lijn' is waar de scharnierlijn ongeveer ligt (deel van het doek, dwars op
# de muur); de precieze plek wordt aan de vrije knop gemeten.


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


def reeksen(waarden):
    """Aaneengesloten gevulde stukken in een rij pixels: [(van, tot), ...]."""
    uit, lo = [], None
    for i, v in enumerate(waarden):
        if v > DREMPEL and lo is None:
            lo = i
        if v <= DREMPEL and lo is not None:
            uit.append((lo, i - 1))
            lo = None
    if lo is not None:
        uit.append((lo, len(waarden) - 1))
    return uit


def lijn_langs(a, as_, dwars):
    """De alpha langs de muurrichting, op afstand 'dwars' (pixels) van de rand."""
    w, h = a.size
    if as_ == "h":
        return [a.getpixel((x, dwars)) for x in range(w)]
    return [a.getpixel((dwars, y)) for y in range(h)]


def lijn_dwars(a, as_, langs):
    """De alpha dwars op de muur, op afstand 'langs' (pixels) van de rand."""
    w, h = a.size
    if as_ == "h":
        return [a.getpixel((langs, y)) for y in range(h)]
    return [a.getpixel((x, langs)) for x in range(w)]


def meet_knoppen(dag, as_, lijn):
    """Vindt de twee knoppen. Langs de geschatte scharnierlijn liggen twee
    gevulde stukken; het laatste is de vrije knop (het blad hangt aan de
    eerste). Uit de vrije knop volgen straal en de precieze lijn; de eerste
    knop heeft dezelfde straal en een schone buitenrand."""
    a = dag.getchannel("A")
    W, H = dag.size
    dwars_maat = H if as_ == "h" else W
    stukken = reeksen(lijn_langs(a, as_, int(round(lijn * dwars_maat))))
    if len(stukken) < 2:
        raise SystemExit("geen twee knoppen gevonden op de scharnierlijn")
    vrij = stukken[-1]
    c2 = (vrij[0] + vrij[1]) / 2.0
    straal = (vrij[1] - vrij[0] + 1) / 2.0
    # de precieze scharnierlijn: het midden van de vrije knop dwars op de muur
    dw = reeksen(lijn_dwars(a, as_, int(round(c2))))
    dw = [s for s in dw if s[0] <= lijn * dwars_maat <= s[1]] or [dw[0]]
    scharnier = (dw[0][0] + dw[0][1]) / 2.0
    # de eerste knop: zijn buitenrand op de precieze lijn, plus de straal
    stukken = reeksen(lijn_langs(a, as_, int(round(scharnier))))
    c1 = stukken[0][0] + straal
    return scharnier, c1, c2, straal


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

        # De knoppen: waar ze zitten en hoe groot ze zijn, in het doek.
        as_ = st["as"]
        scharnier, c1, c2, straal = meet_knoppen(dag, as_, st["lijn"])

        # De vrije knop los. Een vierkant om de knop met één pixel lucht; de
        # speler legt hem met zijn midden op het midden van elke knop.
        if as_ == "h":
            kx, ky = c2, scharnier
        else:
            kx, ky = scharnier, c2
        r1 = straal + 1
        vak = (int(round(kx - r1)), int(round(ky - r1)), int(round(kx + r1)), int(round(ky + r1)))
        knop = dag.crop(vak)
        masker = Image.new("L", knop.size, 0)
        ImageDraw.Draw(masker).ellipse((0, 0, knop.size[0] - 1, knop.size[1] - 1), fill=255)
        alpha = Image.composite(knop.getchannel("A"), Image.new("L", knop.size, 0), masker)
        knop.putalpha(alpha)
        schrijf(knop.resize((KNOP_MAAT, KNOP_MAAT), Image.LANCZOS), os.path.join(DOEL, slug + "-knop.png"))
        regel += "  knop"
        print(regel)

        # De maten voor de speler, als deel van de bijgesneden plaat: langs de
        # muur gedeeld door de maat van de plaat in die richting, dwars erop
        # door de andere.
        if as_ == "h":
            langs, dwars = float(bw), float(bh)
            langs0, dwars0 = box[0], box[1]
        else:
            langs, dwars = float(bh), float(bw)
            langs0, dwars0 = box[1], box[0]
        p1, p2 = (c1 - langs0) / langs, (c2 - langs0) / langs
        s = straal / langs
        regels.append(
            "  %s:{scharnier:%.3f, midden:%.3f, span:%.3f, knoppen:%.3f, knop:%.3f, hoogte:%.3f}" % (
                as_, (scharnier - dwars0) / dwars, (p1 + p2) / 2, (p2 + s) - (p1 - s), p2 - p1,
                2 * r1 / langs, maat[1] / float(maat[0])))
    if regels:
        print("\nIn player/index.html:\nconst DEUR_PLAAT = {\n" + ",\n".join(regels) + "\n};")
    return 0


if __name__ == "__main__":
    sys.exit(main())
