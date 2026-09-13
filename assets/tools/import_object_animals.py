# -*- coding: utf-8 -*-
"""Zet de dieren uit PNG Asset Pack/Characters/Object Animals als bordtekening
in de bank.

Per dier drie bestanden uit Photoshop, 512 bij 512, precies over elkaar:

  <slug>-...-day-...png         het dier bij dag, vrijstaand
  <slug>-...-night-...png       hetzelfde dier bij nacht
  <slug>-...-day-...schaduw.png het dier met zijn schaduw, plat op wit

Dezelfde rollen als de objecten uit Outbox, dus ook dezelfde bewerking: de
schaduw wordt uit het platte beeld teruggerekend (zie schaduwlaag() in
import_outbox_objects.py). De slug is het woord voor het eerste streepje.

Een dier op het bord hoort even groot te staan als de andere dieren: de
speler schaalt alle dieren met dezelfde maat (--dier-kader), en een
tekening die in zijn doek groter is aangeleverd staat dan groter op het bord
en steekt over de muur. De tekening wordt daarom op de maat van de bestaande
dieren gezet: 225 breed (hooguit 218 hoog), midden op x 256, voeten op
y 438. Dag, nacht en schaduw krijgen dezelfde verschuiving.

Het portret van het dier (het medaillon) komt uit import_dieren.py.
Daarna: python assets/tools/maak_webp.py
"""
import os, sys
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import import_outbox_objects as ob

WORTEL = os.path.dirname(os.path.dirname(HIER))
BRON = os.path.join(WORTEL, "Design Department", "50 Handoff to Claude", "PNG Asset Pack",
                    "Characters", "Object Animals")
OBJ = os.path.join(WORTEL, "assets", "art", "objects")


BREED, HOOG_MAX, MIDDEN_X, VOET_Y = 225, 218, 256, 438


def op_maat(im, bbox):
    """Dezelfde schaal en verschuiving als de dagtekening, op het doek van 512."""
    l, t, r, b = bbox
    schaal = min(BREED / float(r - l), HOOG_MAX / float(b - t))
    maat = int(round(512 * schaal))
    klein = im.resize((maat, maat), Image.LANCZOS)
    dx = MIDDEN_X - (l + r) / 2.0 * schaal
    dy = VOET_Y - b * schaal
    uit = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    uit.alpha_composite(klein, (int(round(dx)), int(round(dy))))
    return uit


def rol(naam):
    n = naam.lower()
    if "schaduw" in n or "shadow" in n: return "schaduw"
    if "night" in n or "nacht" in n: return "nacht"
    if "day" in n or "dag" in n: return "dag"
    return None


def main():
    if not os.path.isdir(BRON):
        sys.exit("map ontbreekt: " + BRON)
    dieren = {}
    for f in sorted(os.listdir(BRON)):
        if not f.lower().endswith(".png"): continue
        r = rol(f)
        if r: dieren.setdefault(f.split("-")[0].lower(), {})[r] = os.path.join(BRON, f)
    for slug, r in sorted(dieren.items()):
        if "dag" not in r:
            print("%s: geen dagversie, overgeslagen" % slug); continue
        dag = ob.klein(Image.open(r["dag"]).convert("RGBA"))
        vak = dag.getchannel("A").getbbox()
        ob.schrijf(op_maat(dag, vak), os.path.join(OBJ, slug + ".png"))
        ob.schrijf(op_maat(dag, vak), os.path.join(OBJ, "medieval", slug + ".png"))
        regel = slug + ": dag"
        if "nacht" in r:
            nacht = ob.klein(Image.open(r["nacht"]).convert("RGBA"))
            ob.schrijf(op_maat(nacht, vak), os.path.join(OBJ, "dark", slug + ".png"))
            regel += ", nacht"
        if "schaduw" in r and ob.is_schaduwbestand(r["schaduw"]):
            sch = ob.klein(ob.schaduwlaag(r["dag"], r["schaduw"]))
            ob.schrijf(op_maat(sch, vak), os.path.join(OBJ, "shadows", slug + ".png"))
            regel += ", schaduw"
        print(regel)


if __name__ == "__main__":
    main()
