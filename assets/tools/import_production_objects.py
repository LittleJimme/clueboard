# -*- coding: utf-8 -*-
"""Zet de objecten uit assets/art/production/objects in de assetbank.

Uit Photoshop komen twee bestanden per object, precies over elkaar geplaatst:

  <Naam>.png          het object bij dag, met alpha
  <Naam>_donker.png   hetzelfde object bij nacht, koeler en gedempter
  <Naam> Schaduw.png  hetzelfde beeld plat op wit, met de schaduw erin

De schaduw is er maar een: die vermenigvuldigt met de vloer en klopt dus in
beide standen vanzelf.

De bank krijgt de schaduw niet als wit vlak maar als laag met dekking; waarom
staat verderop bij schaduwlaag().

Dat tweede bestand is dus niet de schaduw alleen: het object staat erin. Zou je
het zo op multiply leggen, dan kleurde het object een tweede keer mee en nam het
de vloerkleur over. De schaduw is er wel uit te rekenen. Photoshop stapelt als

    F = C*a + s*(1-a)

met F het platte beeld, C en a de kleur en dekking van het object, en s de
schaduwlaag op wit. Waar het object dekt (a = 1) is s niet te zien, dus daar mag
wit staan; waar het niet dekt (a = 0) is F precies de schaduw. Daartussen lopen
we van het een naar het ander.

De alpha zet eerst een paar pixels uit. De rand van het uitgesneden object en de
rand in het platte beeld liggen namelijk niet op de pixel gelijk, en zonder die
speling blijft er een donker lijntje rond het object staan - dat is bij twee
pixels weg, terwijl de contactschaduw onder het object blijft.
"""
import io, os, sys, time
import numpy as np
from PIL import Image, ImageFilter

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON   = os.path.join(WORTEL, "assets", "art", "production", "objects")
OBJ    = os.path.join(WORTEL, "assets", "art", "objects")
GROEI  = 2      # pixels dat de alpha uitzet voor het uitrekenen
DREMPEL = 250   # hierboven is het papier, geen schaduw

# Photoshop-naam -> naam in de bank. De tweede en derde kolom zijn het
# schaduw- en het nachtbestand, want die zijn niet allemaal gelijk gespeld.
# Staat er None, dan is er geen nachtversie en blijft die van overdag staan.
LICHTING = [
    ("Beeld",     "Beeld Schaduw",             "Beeld_donker",     ["statue"]),
    ("Boom",      "Boom Schaduw",              "Boom_Donker",      ["tree"]),
    ("Kast",      "Kast Schaduw Multiply",     "Kast_donker",      ["shelf"]),
    ("Kist",      "Kist Schaduw",              "Kist_donker",      ["crate"]),
    ("Modder",    "Moder Schaduw",             None,               ["puddle"]),
    ("Paard",     "Paard Schaduw",             "Paard_donker",     ["horse"]),
    ("Stenen",    "Stenen Schaduw Multiply",   "Stenen_donker",    ["stones"]),
    ("Stoel",     "Stoel Schaduw",             "Stoel_donker",     ["chair"]),
    ("Struik",    "Struik Schaduw",            "Struik_donker",    ["shrub"]),
    ("Tafel 1x1", "Tafel 1x1 Schaduw",         "Tafel 1x1_donker", ["table"]),
    ("Vaas",      "Vaas Schaduw",              "Vaas_donker",      ["vase"]),
    ("Wapenrek",  "WapenrekSchaduw",           "Wapenrek_donker",  ["weapon-chest", "weapon-rack"]),
]

def zoek(naam):
    """Het bestand met deze naam, ongeacht hoofd- of kleine letters. De namen
    uit Photoshop wisselen daarin nog weleens (Boom_Donker, Boom_donker), en op
    Windows valt dat niet op terwijl het elders wel uitmaakt."""
    pad = os.path.join(BRON, naam + ".png")
    if os.path.exists(pad):
        return pad
    doel = (naam + ".png").lower()
    for f in os.listdir(BRON):
        if f.lower() == doel:
            return os.path.join(BRON, f)
    return None

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

def schaduwlaag(objectpad, platpad):
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
    # Het papier uit Photoshop is niet helemaal wit: er zit korrel in van een
    # paar waarden. Op multiply is dat onzichtbaar, maar het maakt van een leeg
    # vlak een ruisvlak dat PNG niet kan wegdrukken, en het houdt de dekking
    # overal net boven nul. Bijna-wit wordt dus echt wit.
    s[s.min(axis=2) >= DREMPEL / 255.0] = 1.0

    # Van wit-op-multiply naar een laag met dekking. Wit is bij vermenigvuldigen
    # niets, maar als vlak wist het wel: twee schaduwen die elkaar overlappen
    # zouden elkaar uitgommen, en een laag die als geheel vermenigvuldigt legt
    # zijn witte kader over de vloer. Met dekking gebeurt geen van beide.
    # Gezocht is een kleur c en dekking d zo dat c over wit weer s oplevert:
    #     d*c + (1-d) = s
    # Met d = 1 - min(s) is dat op te lossen, en dan geldt bij het uiteindelijke
    # vermenigvuldigen nog steeds precies resultaat = ondergrond * s.
    d = 1.0 - s.min(axis=2, keepdims=True)
    veilig = np.maximum(d, 1e-6)
    c = np.clip((s - 1.0 + d) / veilig, 0.0, 1.0)
    rgba = np.concatenate([c, d], axis=2)
    return Image.fromarray((rgba * 255.0 + 0.5).astype(np.uint8), "RGBA")

def main():
    if not os.path.isdir(BRON):
        print("map ontbreekt:", BRON); return 1
    totaal = 0
    for naam, schaduwnaam, nachtnaam, slugs in LICHTING:
        o = zoek(naam)
        p = zoek(schaduwnaam)
        if not (o and p):
            print("OVERGESLAGEN %-12s (bestand ontbreekt)" % naam); continue
        obj = Image.open(o).convert("RGBA")
        sch = schaduwlaag(o, p)
        nacht = None
        if nachtnaam:
            n = zoek(nachtnaam)
            if n:
                nacht = Image.open(n).convert("RGBA")
            else:
                print("   geen nachtversie voor %s" % naam)
        for slug in slugs:
            # De themamap wint van de gedeelde map, dus die moet ook mee,
            # anders blijft de oude tekening staan.
            for doel in (os.path.join(OBJ, slug + ".png"),
                         os.path.join(OBJ, "medieval", slug + ".png")):
                schrijf(obj, doel)
            schrijf(sch, os.path.join(OBJ, "shadows", slug + ".png"))
            if nacht is not None:
                schrijf(nacht, os.path.join(OBJ, "dark", slug + ".png"))
            kb = os.path.getsize(os.path.join(OBJ, "shadows", slug + ".png")) // 1024
            nkb = (os.path.getsize(os.path.join(OBJ, "dark", slug + ".png")) // 1024
                   if nacht is not None else 0)
            print("%-14s -> %-14s dag %3d kB  nacht %3d kB  schaduw %3d kB" % (
                naam, slug, os.path.getsize(os.path.join(OBJ, slug + ".png")) // 1024, nkb, kb))
            totaal += 1
    print("%d tekeningen in de bank" % totaal)
    return 0

if __name__ == "__main__":
    sys.exit(main())
