# -*- coding: utf-8 -*-
"""Zet de personagelagen uit Design Department/50 Handoff to Claude/PNG Asset
Pack/Characters in assets/characters/.

Het doek is sinds 2026-09-11 550 bij 550: het oude doek van 512 met een rand
van 19 pixels rondom, op dezelfde schaal. Alles wat nog op 512 is aangeleverd
(haar uit het pakket van 1233, de eerste vijf baarden, de kruisogen) krijgt
die rand erbij; wat al op 550 komt (Hoofd 2, kleding, nieuwe baarden) gaat
er ongewijzigd in. Zo blijven alle lagen 1:1 op elkaar liggen en hoeft er in
de speler niets te schuiven.

  Base/Hoofd 2.png            -> hoofd.png
  Hair/hair-<id>.png (1233)   -> haar/<id>.png
  Hair/NN-<id>.png (550)      -> haar/<id>.png   (de latere levering)
  Beards/<id>.png             -> baard/<id>.png
  Clothing/NN-<id>.png        -> kleding/<id>.png          (kleurt mee)
  Clothing/NN-<id>-vast.png   -> kleding/<id>-vast.png     (kleurt niet mee:
                                 gespen, bont, leer, onderhemd; ligt erop;
                                 "NN-<id> copy.png" uit Photoshop telt ook)

De kruisogen (ogen.png) zijn ooit uit Overlays gekomen; die worden hier
alleen van 512 naar 550 gezet. Het oude shirt vervalt: de kleding neemt het
over. Daarna: python assets/tools/maak_webp.py, en de vast-vlaggen in
manifest.json worden hier bijgezet op wat er ligt.
"""
import io, json, os, re, sys
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAK = os.path.join(WORTEL, "Design Department", "50 Handoff to Claude", "PNG Asset Pack", "Characters")
DOEL = os.path.join(WORTEL, "assets", "characters")
MANIFEST = os.path.join(WORTEL, "assets", "manifest.json")
DOEK, OUD, RAND = 550, 512, 19


def schrijf(im, pad):
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    tmp = pad + ".tmp"
    im.save(tmp, "PNG", optimize=True)
    os.replace(tmp, pad)


def op_doek(im):
    """Een laag op het doek van 550. Was hij 512, dan komt de rand erbij;
    is hij al 550, dan blijft hij zoals hij is. Andere maten passen niet."""
    im = im.convert("RGBA")
    if im.size == (DOEK, DOEK):
        return im
    if im.size == (OUD, OUD):
        n = Image.new("RGBA", (DOEK, DOEK), (0, 0, 0, 0))
        n.paste(im, (RAND, RAND))
        return n
    raise SystemExit("onverwachte maat %s" % (im.size,))


def uit_pakket(im):
    """Het haar komt uit het pakket op 1233: eerst naar de oude 512 (zoals de
    bank tot nu toe was), dan de rand erbij."""
    im = im.convert("RGBA")
    if im.size != (OUD, OUD) and im.size != (DOEK, DOEK):
        im = im.resize((OUD, OUD), Image.LANCZOS)
    return op_doek(im)


def main():
    if not os.path.isdir(PAK):
        print("pakket ontbreekt:", PAK); return 1
    regels = []

    hoofd = os.path.join(PAK, "Base", "Hoofd 2.png")
    schrijf(op_doek(Image.open(hoofd)), os.path.join(DOEL, "hoofd.png"))
    regels.append("hoofd")

    haarmap = os.path.join(PAK, "Hair")
    for f in sorted(os.listdir(haarmap)):
        m = re.match(r"(?:hair-|\d+-)(.+)\.png$", f)
        if not m: continue
        schrijf(uit_pakket(Image.open(os.path.join(haarmap, f))), os.path.join(DOEL, "haar", m.group(1) + ".png"))
        regels.append("haar/" + m.group(1))

    baardmap = os.path.join(PAK, "Beards")
    for f in sorted(os.listdir(baardmap)):
        if not f.endswith(".png"): continue
        schrijf(op_doek(Image.open(os.path.join(baardmap, f))), os.path.join(DOEL, "baard", f))
        regels.append("baard/" + f[:-4])

    ogen = os.path.join(DOEL, "ogen.png")
    if os.path.exists(ogen):
        schrijf(op_doek(Image.open(ogen)), ogen)
        regels.append("ogen")

    kledingmap = os.path.join(PAK, "Clothing")
    vast = {}
    for f in sorted(os.listdir(kledingmap)):
        m = re.match(r"\d+-(.+?)(-vast| copy)?\.png$", f)
        if not m: continue
        naam = m.group(1) + ("-vast" if m.group(2) else "")
        schrijf(op_doek(Image.open(os.path.join(kledingmap, f))), os.path.join(DOEL, "kleding", naam + ".png"))
        if m.group(2): vast[m.group(1)] = True
        regels.append("kleding/" + naam)

    for oud in ("shirt.png", "shirt.webp"):
        p = os.path.join(DOEL, oud)
        if os.path.exists(p): os.remove(p); regels.append("weg: " + oud)

    # De vast-vlaggen in de bank: alleen waar er echt een vaste laag ligt.
    s = io.open(MANIFEST, encoding="utf-8").read()
    def zet(m):
        ident = m.group(1)
        return '"id": "%s"%s"vast": %s' % (ident, m.group(2), "true" if vast.get(ident) else "false")
    s2, n = re.subn(r'"id": "([a-z-]+)"(,\s*"label": "[^"]*",\s*)"vast": (?:true|false)', zet, s)
    if s2 != s:
        io.open(MANIFEST + ".tmp", "w", encoding="utf-8", newline="").write(s2)
        os.replace(MANIFEST + ".tmp", MANIFEST)
    print("\n".join(regels))
    print("vast-lagen:", sorted(vast) or "geen", "| manifest-vlaggen bijgezet:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
