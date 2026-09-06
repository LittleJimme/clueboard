# -*- coding: utf-8 -*-
"""Zet de meervaksobjecten uit een Outbox-map in de assetbank.

Dezelfde lichting als de 1x1-objecten, maar dan over twee vakken. Per object
komen er drie bestanden uit Photoshop, alle even groot en in de verhouding van
het vak zelf (een 1x2 dus 1024 bij 2048):

  <slug>-dag-1x2.png          het object bij dag, vrijstaand (met alpha)
  <slug>-nacht-1x2.png        hetzelfde object bij nacht, zelfde plek en maat
  <slug>-dag-1x2 shadow.png   het object mét zijn schaduw, plat op papier

De slug draagt zijn maat al ("bed-1x2"); de maat achter de rol is een
herhaling uit de rendermap en wordt hier weggelaten. Namen worden zonder op
hoofdletters te letten gezocht, net als bij de 1x1-lichting.

Het uitrekenen van de schaduw gebeurt met schaduwlaag() uit
import_outbox_objects.py -- dezelfde som, want het is dezelfde Photoshop-stapel.
Die som gaat er wel van uit dat het platte beeld pixel voor pixel dezelfde
render is als het vrijstaande object. Komt er een keer een plaat langs die
verschoven of half doorzichtig is aangeleverd, dan levert de som een spookbeeld
op in plaats van een schaduw. Daarom eerst twee eisen: het platte beeld moet
overal dekkend zijn, en waar het object staat moet het plat ook donkerder zijn
dan het papier. Haalt een bestand dat niet, dan gaat alleen de schaduw niet mee
-- dag en nacht komen gewoon in de bank.
"""
import os, re, sys
import numpy as np
from PIL import Image

from import_outbox_objects import schaduwlaag, schrijf

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OBJ = os.path.join(WORTEL, "assets", "art", "objects")
DEEL = 2          # de bank krijgt de helft van de bronmaat, net als bij 1x1
DEKKING = 0.95    # zoveel van het object moet in het platte beeld terug te zien zijn

MAAT = re.compile(r"^(.*?)-(dag|nacht)(?:-\d+x\d+)?(\s+shadow)?$", re.IGNORECASE)


def lichting(bron):
    """Alle objecten in de map, met hun drie rollen."""
    uit = {}
    for f in sorted(os.listdir(bron)):
        if not f.lower().endswith(".png"):
            continue
        m = MAAT.match(f[:-4])
        if not m:
            continue
        slug, rol, schaduw = m.group(1), m.group(2).lower(), m.group(3)
        uit.setdefault(slug, {})["shadow" if schaduw else rol] = os.path.join(bron, f)
    return uit


def klein(im):
    return im.resize((im.width // DEEL, im.height // DEEL), Image.LANCZOS)


def platBeeld(pad):
    """Het platte beeld als RGB, met de doorzichtige randen op papierkleur.

    Sommige platen komen met alfa binnen: het beeld staat er wel helemaal op,
    maar boven en onder is een strook doorzichtig gelaten. Die strook op wit
    zetten zou niet kloppen -- het papier is roomkleurig, en dan leest de hele
    strook straks als een flauwe schaduw. De papierkleur wordt daarom aan de
    rand van het dekkende deel gemeten en de doorzichtige rest krijgt diezelfde
    kleur; daarmee is het weer één egaal vel.
    """
    im = Image.open(pad)
    if im.mode != "RGBA":
        return im.convert("RGB")
    a = np.asarray(im)
    vol = a[:, :, 3] > 250
    if not vol.any():
        return im.convert("RGB")
    ys, xs = np.nonzero(vol)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    ring = np.concatenate([a[y0:y0+6, x0:x1+1, :3].reshape(-1, 3),
                           a[max(y0, y1-5):y1+1, x0:x1+1, :3].reshape(-1, 3),
                           a[y0:y1+1, x0:x0+6, :3].reshape(-1, 3),
                           a[y0:y1+1, max(x0, x1-5):x1+1, :3].reshape(-1, 3)])
    papier = tuple(int(v) for v in np.median(ring, axis=0))
    vel = Image.new("RGB", im.size, papier)
    vel.paste(im.convert("RGB"), (0, 0), im.split()[3])
    return vel


def schaduwDeugt(objectpad, platpad):
    """Hoort dit platte beeld bij dit object? Zo niet: waarom niet."""
    obj = Image.open(objectpad).convert("RGBA")
    plaat = Image.open(platpad)
    plat = platBeeld(platpad)
    if obj.size != plat.size:
        return "de maten lopen uiteen (%s tegen %s)" % (obj.size, plat.size)
    er_op0 = np.asarray(obj)[:, :, 3] > 128
    if plaat.mode == "RGBA" and not bool((np.asarray(plaat)[:, :, 3][er_op0] > 250).all()):
        return "het object staat niet volledig op de platte plaat"
    F = np.asarray(plat, dtype=np.float64)
    rand = np.concatenate([F[:6].reshape(-1, 3), F[-6:].reshape(-1, 3),
                           F[:, :6].reshape(-1, 3), F[:, -6:].reshape(-1, 3)])
    papier = np.median(rand, axis=0)
    if papier.min() < 200:
        return "het papier is te donker (%s)" % papier.astype(int).tolist()
    donker = (F / np.maximum(papier, 1e-6)).min(axis=2) < 0.92
    er_op = np.asarray(obj)[:, :, 3] > 128
    if not er_op.any():
        return "het object heeft geen alfakanaal"
    dekking = float((donker & er_op).sum()) / float(er_op.sum())
    if dekking < DEKKING:
        return ("het object staat er maar voor %d%% op; waarschijnlijk een andere "
                "of verschoven render" % round(dekking * 100))
    return None


def main(argv):
    map_naam = argv[1] if len(argv) > 1 else "Outbox 1x2"
    bron = os.path.join(WORTEL, "Design Department", "60 Repo Sources", "MAIN", map_naam)
    if not os.path.isdir(bron):
        print("map ontbreekt:", bron)
        return 1
    alles = lichting(bron)
    if not alles:
        print("niets gevonden in", bron)
        return 1
    aantal, gemist = 0, []
    for slug in sorted(alles):
        rollen = alles[slug]
        if "dag" not in rollen:
            gemist.append("%s: geen dagversie" % slug)
            continue
        dag = Image.open(rollen["dag"]).convert("RGBA")
        schrijf(klein(dag), os.path.join(OBJ, slug + ".png"))
        schrijf(klein(dag), os.path.join(OBJ, "medieval", slug + ".png"))
        regel = "%-14s %dx%d  dag %3d kB" % (slug, dag.width, dag.height,
                                             os.path.getsize(os.path.join(OBJ, slug + ".png")) // 1024)
        if "nacht" in rollen:
            nacht = Image.open(rollen["nacht"]).convert("RGBA")
            schrijf(klein(nacht), os.path.join(OBJ, "dark", slug + ".png"))
            regel += "  nacht %3d kB" % (os.path.getsize(os.path.join(OBJ, "dark", slug + ".png")) // 1024)
        else:
            gemist.append("%s: geen nachtversie" % slug)
            regel += "  nacht   -  "
        klacht = schaduwDeugt(rollen["dag"], rollen["shadow"]) if "shadow" in rollen else "niet aangeleverd"
        if klacht:
            gemist.append("%s: schaduw overgeslagen, %s" % (slug, klacht))
            regel += "  schaduw   -  "
        else:
            schrijf(klein(schaduwlaag(rollen["dag"], platBeeld(rollen["shadow"]))),
                    os.path.join(OBJ, "shadows", slug + ".png"))
            regel += "  schaduw %3d kB" % (os.path.getsize(os.path.join(OBJ, "shadows", slug + ".png")) // 1024)
        print(regel)
        aantal += 1
    print("\n%d meervaksobjecten in de bank" % aantal)
    if gemist:
        print("aandacht nodig:")
        for g in gemist:
            print("  " + g)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
