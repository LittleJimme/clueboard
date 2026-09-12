# -*- coding: utf-8 -*-
"""Zet de dierenportretten uit Design Department/50 Handoff to Claude/PNG Asset
Pack/Characters/Animals in assets/characters/dieren/.

Een dier kan in een zaak als getuige naast de verdachten staan. Zijn portret
hangt in hetzelfde medaillon als dat van een dorpeling, dus moet het op het
doek van 550 net zo staan als een mensenhoofd: de kop vult de schijf en steekt
er bovenaan een stukje boven uit.

De tekeningen komen in verschillende maten binnen (een paard is smal en hoog,
een varken breed en laag). Daarom wordt elk dier hier op zijn eigen maat
gezet: de kop wordt geschaald tot hij de schijf vult, horizontaal gecentreerd
op x 274 en met de bovenkant op y 85 -- dezelfde plek waar een mensenkruin
zit. In de speler is `--kruin` voor elk dier dus gelijk (DIER_KRUIN = 85).

De kruisogen van het slachtoffer gaan door dezelfde verschuiving heen en
komen als `<slug>-dood.png` naast het dier te staan. Zo blijven ze precies op
de ogen liggen, ook nu het dier is geschaald.

Daarna: python assets/tools/build_assets.py  (bakt de bank in)
        python assets/tools/maak_webp.py     (de speler laadt webp)
"""
import io, json, os, re, sys
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAK = os.path.join(WORTEL, "Design Department", "50 Handoff to Claude",
                   "PNG Asset Pack", "Characters", "Animals")
DOEL = os.path.join(WORTEL, "assets", "characters", "dieren")
OGEN = os.path.join(WORTEL, "assets", "characters", "ogen.png")
MANIFEST = os.path.join(WORTEL, "assets", "manifest.json")

DOEK = 550
KRUIN = 85          # waar de kop begint; gelijk aan --kruin in de speler
HOOG = 416          # de hoogte die de schijf vult (135..505 op het doek)
BREED_MAX = 420     # breder dan dit wordt het dier niet: oren mogen over de rand


def schrijf(im, pad):
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    tmp = pad + ".tmp"
    im.save(tmp, "PNG", optimize=True)
    os.replace(tmp, pad)


def verplaats(im, schaal, dx, dy):
    """Het hele doek op maat en op zijn plek: x' = x*schaal + dx."""
    maat = max(1, int(round(DOEK * schaal)))
    klein = im.convert("RGBA").resize((maat, maat), Image.LANCZOS)
    uit = Image.new("RGBA", (DOEK, DOEK), (0, 0, 0, 0))
    uit.alpha_composite(klein, (int(round(dx)), int(round(dy))))
    return uit


def main():
    if not os.path.isdir(PAK):
        sys.exit("Niet gevonden: " + PAK)
    ogen = Image.open(OGEN).convert("RGBA")
    manifest = json.loads(io.open(MANIFEST, encoding="utf-8").read())
    per_slug = {o["slug"]: o for o in manifest["objects"]}

    gedaan, zonder_soort = [], []
    for naam in sorted(os.listdir(PAK)):
        m = re.match(r"^\d+-([a-z0-9-]+)\.png$", naam)
        if not m:
            continue
        slug = m.group(1)
        bron = Image.open(os.path.join(PAK, naam)).convert("RGBA")
        if bron.size != (DOEK, DOEK):
            sys.exit("%s is %dx%d; verwacht %d bij %d" % ((naam,) + bron.size + (DOEK, DOEK)))
        bx0, by0, bx1, by1 = bron.getbbox()
        breed, hoog = bx1 - bx0, by1 - by0
        schaal = min(HOOG / float(hoog), BREED_MAX / float(breed))
        dx = 274 - (breed * schaal) / 2.0 - bx0 * schaal
        dy = KRUIN - by0 * schaal

        schrijf(verplaats(bron, schaal, dx, dy), os.path.join(DOEL, slug + ".png"))
        schrijf(verplaats(ogen, schaal, dx, dy), os.path.join(DOEL, slug + "-dood.png"))

        soort = per_slug.get(slug)
        if soort is None:
            zonder_soort.append(slug)
        else:
            soort["portret"] = "dieren/" + slug + ".png"
        gedaan.append((slug, breed, hoog, round(schaal, 3), soort["kind"] if soort else "-"))

    uit = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    tmp = MANIFEST + ".tmp"
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(uit)
    os.replace(tmp, MANIFEST)

    print("dieren -> assets/characters/dieren/")
    for slug, b, h, s, kind in gedaan:
        print("  %-7s bron %dx%d  schaal %.3f  soort %s" % (slug, b, h, s, kind))
    if zonder_soort:
        print("\nGeen objectsoort in de bank (dus nog niet te gebruiken als getuige): "
              + ", ".join(zonder_soort))
        print("Zo'n dier heeft eerst een soort in manifest.json nodig, met een icoon en "
              "een tekening in assets/art/objects.")


if __name__ == "__main__":
    main()
