# -*- coding: utf-8 -*-
"""Zet de 1x1-objecten uit assets/art/MAIN/Outbox in de assetbank.

Per object komen er drie bestanden uit Photoshop, alle 1024 bij 1024:

  <slug>-dag.png     het object bij dag, al vrijstaand (met alpha)
  <slug>-nacht.png   hetzelfde object bij nacht, zelfde plek en maat
  <slug>-shadow.png  het object mét zijn schaduw, plat op wit

Een paar bestanden heten "-dag shadow" in plaats van "-shadow"; dat wordt hier
opgevangen. De namen worden ook zonder op hoofdletters te letten gezocht: die
spelling is eerder verschoven en dat brak het inlezen op de server.

Het derde bestand is niet de schaduw alleen: het object staat erin. Zo op
multiply gelegd zou het object een tweede keer meekleuren en de vloerkleur
overnemen. Omdat het object apart met alpha wordt aangeleverd, is de schaduw
eruit te rekenen -- zie schaduwlaag() voor hoe en waarom.

De bank krijgt een kleinere versie dan de bron. Het beeld beslaat in het spel
1,6 vakje; op een telefoon is dat rond de 120 punten, op een groot scherm rond
de 190. Op 512 pixels is dat ook op een scherm met dubbele dichtheid nog ruim
bemeten. De scherpe 1024-versie blijft in Outbox staan als bron.
"""
import os, re, sys, time
import numpy as np
from PIL import Image, ImageFilter

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "assets", "art", "MAIN", "Outbox")
OBJ  = os.path.join(WORTEL, "assets", "art", "objects")
MAAT = 512      # wat er in de bank komt
GROEI = 2       # pixels dat de alpha uitzet voor het uitrekenen van de schaduw
DREMPEL = 250   # hierboven is het papier, geen schaduw

# loom is onvolledig aangeleverd: er is geen -dag, en het bestand dat -shadow
# heet is geen schaduw maar juist de dagversie (met alpha, geen wit eromheen).
# Zolang dat zo is nemen we die als dag en krijgt loom geen schaduw.
UITZONDERING = {"loom": {"dag": "loom-shadow", "shadow": None}}


def zoek(naam):
    """Het bestand met deze naam, ongeacht hoofd- of kleine letters."""
    if naam is None:
        return None
    pad = os.path.join(BRON, naam + ".png")
    if os.path.exists(pad):
        return pad
    doel = (naam + ".png").lower()
    for f in os.listdir(BRON):
        if f.lower() == doel:
            return os.path.join(BRON, f)
    return None


def lichting():
    """Alle objecten in de map, met hun drie rollen."""
    uit = {}
    for f in os.listdir(BRON):
        if not f.lower().endswith(".png"):
            continue
        n = f[:-4]
        for staart, rol in (("-dag shadow", "shadow"), ("-shadow", "shadow"),
                            ("-dag", "dag"), ("-nacht", "nacht")):
            if n.lower().endswith(staart):
                uit.setdefault(n[:-len(staart)], {})[rol] = n
                break
    for slug, vast in UITZONDERING.items():
        if slug in uit:
            uit[slug].update(vast)
    return uit


def schrijf(im, pad):
    """Eerst naast het doel, dan omzetten: een half geschreven PNG is erger
    dan een oude."""
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    tmp = pad + ".tmp"
    im.save(tmp, format="PNG", optimize=True)
    for _ in range(8):
        try:
            os.replace(tmp, pad); return
        except PermissionError:
            time.sleep(1)
    raise IOError(pad)


def klein(im):
    return im.resize((MAAT, MAAT), Image.LANCZOS)


def schaduwlaag(objectpad, platpad):
    """De schaduw uit het platte beeld halen.

    Photoshop stapelt als F = C*a + s*(1-a), met F het platte beeld, C en a de
    kleur en dekking van het object, en s de schaduw op wit. Waar het object
    dekt is s niet te zien, dus daar mag wit staan; waar het niet dekt is F
    precies de schaduw. De alpha zet eerst twee pixels uit: de rand van het
    uitgesneden object en die in het platte beeld liggen niet op de pixel
    gelijk, en zonder die speling blijft er een donker lijntje omheen staan.

    Daarna gaat wit-op-multiply naar een laag met dekking. Wit is bij
    vermenigvuldigen niets, maar als vlak wist het wel: twee schaduwen die
    elkaar overlappen zouden elkaar uitgommen. Gezocht is een kleur c en
    dekking d zodat c over wit weer s oplevert (d*c + (1-d) = s); met
    d = 1 - min(s) is dat op te lossen, en bij het uiteindelijke
    vermenigvuldigen geldt dan nog steeds resultaat = ondergrond * s.
    """
    obj = Image.open(objectpad).convert("RGBA")
    plat = Image.open(platpad).convert("RGB")
    if obj.size != plat.size:
        raise ValueError("maten lopen uiteen: %s vs %s" % (obj.size, plat.size))
    a = obj.split()[3]
    if GROEI:
        a = a.filter(ImageFilter.MaxFilter(1 + 2 * GROEI))
    a = np.asarray(a, dtype=np.float64)[:, :, None] / 255.0
    F = np.asarray(plat, dtype=np.float64) / 255.0
    s = np.clip(F * (1.0 - a) + a, 0.0, 1.0)
    s[s.min(axis=2) >= DREMPEL / 255.0] = 1.0
    d = 1.0 - s.min(axis=2, keepdims=True)
    veilig = np.maximum(d, 1e-6)
    c = np.clip((s - 1.0 + d) / veilig, 0.0, 1.0)
    rgba = np.concatenate([c, d], axis=2)
    return Image.fromarray((rgba * 255.0 + 0.5).astype(np.uint8), "RGBA")


def main():
    if not os.path.isdir(BRON):
        print("map ontbreekt:", BRON); return 1
    alles = lichting()
    aantal, gemist = 0, []
    for slug in sorted(alles):
        rollen = alles[slug]
        dagpad = zoek(rollen.get("dag"))
        nachtpad = zoek(rollen.get("nacht"))
        schpad = zoek(rollen.get("shadow"))
        if not dagpad:
            gemist.append("%s: geen dagversie" % slug); continue
        dag = Image.open(dagpad).convert("RGBA")
        schrijf(klein(dag), os.path.join(OBJ, slug + ".png"))
        schrijf(klein(dag), os.path.join(OBJ, "medieval", slug + ".png"))
        regel = "%-14s dag %3d kB" % (slug, os.path.getsize(os.path.join(OBJ, slug + ".png")) // 1024)
        if nachtpad:
            schrijf(klein(Image.open(nachtpad).convert("RGBA")),
                    os.path.join(OBJ, "dark", slug + ".png"))
            regel += "  nacht %3d kB" % (os.path.getsize(os.path.join(OBJ, "dark", slug + ".png")) // 1024)
        else:
            gemist.append("%s: geen nachtversie" % slug); regel += "  nacht   -  "
        if schpad:
            schrijf(klein(schaduwlaag(dagpad, schpad)),
                    os.path.join(OBJ, "shadows", slug + ".png"))
            regel += "  schaduw %3d kB" % (os.path.getsize(os.path.join(OBJ, "shadows", slug + ".png")) // 1024)
        else:
            gemist.append("%s: geen schaduw" % slug); regel += "  schaduw   -  "
        print(regel)
        aantal += 1
    print("\n%d objecten in de bank" % aantal)
    if gemist:
        print("onvolledig aangeleverd:")
        for g in gemist:
            print("  " + g)
    return 0


if __name__ == "__main__":
    sys.exit(main())
