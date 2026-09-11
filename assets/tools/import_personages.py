# -*- coding: utf-8 -*-
"""Zet de personagelagen uit Design Department/50 Handoff to Claude/PNG Asset
Pack/Characters in assets/characters/.

Het doek is sinds 2026-09-11 550 bij 550: het oude doek van 512 met een rand
van 19 pixels rondom, op dezelfde schaal. Alles wat nog op 512 is aangeleverd
(haar uit het pakket van 1233, de eerste vijf baarden, de kruisogen) krijgt
die rand erbij; wat al op 550 komt (Hoofd 2, kleding, nieuwe baarden) gaat
er ongewijzigd in. Zo blijven alle lagen 1:1 op elkaar liggen en hoeft er in
de speler niets te schuiven.

  Base/Hoofd 3.png            -> hoofd.png  (hoofd met schouders; de romp
                                 gaat weg onder de zoom van de kortste
                                 mannenkleding)
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
from PIL import Image, ImageChops

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAK = os.path.join(WORTEL, "Design Department", "50 Handoff to Claude", "PNG Asset Pack", "Characters")
DOEL = os.path.join(WORTEL, "assets", "characters")
MANIFEST = os.path.join(WORTEL, "assets", "manifest.json")
DOEK, OUD, RAND = 550, 512, 19
# Niets verschuiven: alle lagen liggen 1:1 zoals ze zijn aangeleverd. De tuniek
# met ronde hals heeft 8 px lager gestaan om bij het medaillon de onderrand van
# de schijf te raken, maar dan kwamen de schouders onder de halslijn uit -- die
# schouders zitten sinds Hoofd 3 in de hoofdlaag zelf. Het personage staat nu
# iets kleiner en lager in het portret; dat lost het netter op.
SCHUIF = {}


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
    # Een tekening die onderaan buiten het doek loopt (een japon tot op de
    # grond, het hoofd met schouders) staat linksboven op hetzelfde doek: het
    # overschot valt eraf.
    if im.size[0] == DOEK and im.size[1] > DOEK:
        return im.crop((0, 0, DOEK, DOEK))
    raise SystemExit("onverwachte maat %s" % (im.size,))


def verschuif(im, dy):
    """Een laag een paar pixels omlaag op hetzelfde doek."""
    if not dy:
        return im
    n = Image.new("RGBA", im.size, (0, 0, 0, 0))
    n.paste(im, (0, dy))
    return n


def uit_pakket(im):
    """Het haar komt uit het pakket op 1233: eerst naar de oude 512 (zoals de
    bank tot nu toe was), dan de rand erbij."""
    im = im.convert("RGBA")
    if im.size != (OUD, OUD) and im.size != (DOEK, DOEK):
        im = im.resize((OUD, OUD), Image.LANCZOS)
    return op_doek(im)


def hoofd_laag(basis, vrouw):
    """De hoofdlaag: sinds 2026-09-12 Hoofd 3 -- hetzelfde hoofd als Hoofd 2,
    met schouders erbij, zodat een lage halslijn huid laat zien.

    Onder de zoom van de kortste mannenkleding gaat de romp weg. Anders keek je
    bij een korte tuniek onder de zoom tegen een blote romp aan (te zien in de
    punt van het schild en onderaan het medaillon). Wat een langere tuniek of
    een japon bedekt, bedekt hij nog steeds; de halslijnen van de damenkleding
    liggen hoger dan de zoom en blijven dus staan."""
    naam = "Hoofd 3.png" if os.path.exists(os.path.join(PAK, "Base", "Hoofd 3.png")) else "Hoofd 2.png"
    im = op_doek(Image.open(os.path.join(PAK, "Base", naam)))
    zoom = {}
    for ident, kleed in basis.items():
        if ident in vrouw:
            continue
        a = kleed.getchannel("A").load()
        for x in range(DOEK):
            for y in range(DOEK - 1, -1, -1):
                if a[x, y] > 32:
                    zoom[x] = min(zoom.get(x, DOEK), y)
                    break
    px, weg = im.load(), 0
    for x, grens in zoom.items():
        for y in range(min(grens + 3, DOEK), DOEK):
            r, g, b, a2 = px[x, y]
            if a2:
                px[x, y] = (r, g, b, 0)
                weg += 1
    return im, "%s, %d rompvlakken onder de zoom weg" % (naam, weg)


def main():
    if not os.path.isdir(PAK):
        print("pakket ontbreekt:", PAK); return 1
    regels = []

    # De kleding eerst: de hoofdlaag heeft de zomen nodig.
    kledingmap = os.path.join(PAK, "Clothing")
    vast, basis = {}, {}
    for f in sorted(os.listdir(kledingmap)):
        m = re.match(r"\d+-(.+?)(-vast| copy)?\.png$", f)
        if not m: continue
        dy = SCHUIF.get(m.group(1), 0)
        if m.group(2): vast[m.group(1)] = verschuif(op_doek(Image.open(os.path.join(kledingmap, f))), dy)
        else: basis[m.group(1)] = verschuif(op_doek(Image.open(os.path.join(kledingmap, f))), dy)
    bank = json.loads(io.open(MANIFEST, encoding="utf-8").read())
    vrouw = set(k["id"] for k in bank.get("clothing", []) if k.get("gender") == "female")

    hoofd, hoofdnaam = hoofd_laag(basis, vrouw)
    schrijf(hoofd, os.path.join(DOEL, "hoofd.png"))
    regels.append("hoofd  (" + hoofdnaam + ")")

    haarmap = os.path.join(PAK, "Hair")
    for f in sorted(os.listdir(haarmap)):
        m = re.match(r"(?:hair-|\d+-)(.+)\.png$", f)
        if not m: continue
        schrijf(uit_pakket(Image.open(os.path.join(haarmap, f))), os.path.join(DOEL, "haar", m.group(1) + ".png"))
        regels.append("haar/" + m.group(1))

    baardmap = os.path.join(PAK, "Beards")
    for f in sorted(os.listdir(baardmap)):
        if not f.endswith(".png"): continue
        # "04-straight-cut-beard.png" heet in de bank straight-cut-beard: het
        # nummer is de volgorde van de levering, geen deel van de naam.
        naam = re.sub(r"^\d+-", "", f[:-4])
        schrijf(op_doek(Image.open(os.path.join(baardmap, f))), os.path.join(DOEL, "baard", naam + ".png"))
        regels.append("baard/" + naam)

    ogen = os.path.join(DOEL, "ogen.png")
    if os.path.exists(ogen):
        schrijf(op_doek(Image.open(ogen)), ogen)
        regels.append("ogen")

    for naam, im in basis.items():
        if naam in vast:
            # De vaste laag wordt uit de basis gestanst. Anders telt het leer
            # of het bont mee in de toon waarop de kwast inkleurt, en krijgt
            # het onderhemd van de jerkin een verkeerde kleur; en langs de rand
            # van een gesp schemert anders een gekleurd randje door.
            im = im.copy()
            im.putalpha(ImageChops.multiply(im.getchannel("A"), ImageChops.invert(vast[naam].getchannel("A"))))
            schrijf(vast[naam], os.path.join(DOEL, "kleding", naam + "-vast.png"))
            regels.append("kleding/" + naam + "-vast")
        schrijf(im, os.path.join(DOEL, "kleding", naam + ".png"))
        regels.append("kleding/" + naam + ("  (uitgestanst)" if naam in vast else "")
                      + ("  (%d px lager)" % SCHUIF[naam] if naam in SCHUIF else ""))

    # De rand van de banier en het schild los: de plaat zonder het
    # binnenvlak. De bouwer legt daaronder een vlak in de lichte tint van de
    # persoon, zodat alleen de rand goud of zilver is.
    for vorm in ("banier", "schild"):
        plaat = Image.open(os.path.join(DOEL, "ui", vorm + ".png")).convert("RGBA")
        masker = Image.open(os.path.join(DOEL, "ui", "masker-" + vorm + ".png")).convert("RGBA").getchannel("A")
        rand = plaat.copy()
        rand.putalpha(ImageChops.multiply(plaat.getchannel("A"), ImageChops.invert(masker)))
        schrijf(rand, os.path.join(DOEL, "ui", vorm + "-rand.png"))
        regels.append("ui/" + vorm + "-rand")

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
