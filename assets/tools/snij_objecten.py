# -*- coding: utf-8 -*-
"""Snijdt het objectenblad uit tot losse sprites, met de schaduw als schaduw.

Het blad is al vrijgesteld, maar de schaduw is dat niet goed: die staat er nog
als LICHTE pixels, deels dekkend. Een lichte pixel over een donkere vloer maakt
die vloer lichter -- je krijgt dan een waas in plaats van een schaduw.

Wat hier gebeurt:

  1. Voor elke pixel wordt teruggerekend hoe hij op wit oogde:
        L0 = kleur * dekking + 255 * (1 - dekking)
     Dat is de enige eerlijke maat voor "hoeveel donkerder maakte deze pixel
     zijn ondergrond".

  2. Vanaf de rand wordt naar binnen gelopen door alles wat op wit licht was
     (L0 boven de drempel). Zo vinden we wat BUITEN het object ligt. Lichte
     delen binnen een object -- een wit kussen, een grijs standbeeld -- worden
     niet geraakt, want de donkere omlijning houdt de vulling tegen.

  3. Wat buiten ligt wordt schaduw: donkere kleur, en een dekking van
     (255 - L0) / 255. Een schaduw die wit 24% donkerder maakte, maakt nu elke
     ondergrond 24% donkerder. Wat binnen ligt blijft onaangeroerd.

Gebruik:  python assets/tools/snij_objecten.py
"""
import os
from collections import deque

from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HIER)
BRON = os.path.join(ASSETS, "render", "inbox", "objecten-vrijgesteld.png")
DOEL = os.path.join(ASSETS, "art", "objects", "medieval")

MARGE = 20          # lucht rond het object, zodat de schaduw meekomt
# De schaduw loopt op wit van bijna 255 tot ongeveer 160. Alleen op helderheid
# scheiden lukt dus niet: de donkerste schaduw is even licht als een lichtgrijs
# deel van een object. Daarom twee eisen samen: licht genoeg EN vrijwel kleurloos.
# Een omlijning is altijd donkerder dan 120, dus daar houdt het lopen op.
BUITEN = 120        # op wit donkerder dan dit is tekening
GRIJS = 46          # meer kleurverschil dan dit is tekening
INKT = 176          # bij het opsporen van losse objecten telt alles hieronder
                    # als tekening; ruimer, anders valt een licht object uiteen
SCHADUWKLEUR = (26, 20, 12)

# Rij voor rij, links naar rechts. Namen die overeenkomen met een objectsoort
# uit de bank krijgen die slug; maatvarianten heten slug-<b>x<h>, zoals de
# player ze zoekt (objectAssetCandidates).
PLAN = [
    ["chair", "bench-2x1", "bed-2x1", "boat-2x1",
     "horse", "cow", "pig", "boar", "wolf"],
    ["table", "table-2x1", "table-3x1", "table-hoek",
     "easel", "loom", "barrel", "crate", "box", "sack",
     "shelf", "treasure", "weapon-chest"],
    ["stones", "stones-2x1", "stones-extra", "stones-3x1", "stones-hoek",
     "tree", "shrub", "plant"],
    ["catapult-2x1", "rubble", "watermill-2x1", "house", "statue", "vase"],
    ["door", "window", "gate", "well", "door-steen", "window-steen", "gate-steen"],
]


def op_wit(p):
    """Hoe licht was deze pixel toen hij nog op de witte achtergrond stond?"""
    r, g, b, a = p
    f = a / 255.0
    grijs = (r + g + b) / 3.0
    return grijs * f + 255 * (1 - f)


def kleurloos_op_wit(p):
    """Hoeveel kleur hield deze pixel over toen hij op wit stond? Een schaduw
       is vrijwel kleurloos; hout, gras en steen niet."""
    r, g, b, a = p
    f = a / 255.0
    kanalen = [k * f + 255 * (1 - f) for k in (r, g, b)]
    return max(kanalen) - min(kanalen)


def is_buiten(p):
    return op_wit(p) > BUITEN and kleurloos_op_wit(p) < GRIJS


def componenten(im, minpx=1200):
    """Losse objecten, gezocht op wat duidelijk tekening is (niet de schaduw)."""
    w, h = im.size
    px = im.load()
    ouder = {}

    def vind(x):
        while ouder[x] != x:
            ouder[x] = ouder[ouder[x]]
            x = ouder[x]
        return x

    def voeg(x, y):
        rx, ry = vind(x), vind(y)
        if rx != ry:
            ouder[ry] = rx

    def inkt(x, y):
        p = px[x, y]
        return p[3] > 120 and op_wit(p) < INKT

    vorig, volgend, vak = [], 0, {}
    for y in range(h):
        runs, x = [], 0
        while x < w:
            if inkt(x, y):
                x0 = x
                while x < w and inkt(x, y):
                    x += 1
                runs.append((x0, x - 1))
            else:
                x += 1
        labels = []
        for (x0, x1) in runs:
            raak = [l for (rx0, rx1, l) in vorig if not (rx1 < x0 - 3 or rx0 > x1 + 3)]
            if raak:
                lab = vind(raak[0])
                for r in raak[1:]:
                    voeg(lab, r)
            else:
                lab = volgend
                ouder[lab] = lab
                volgend += 1
            labels.append(lab)
            r = vak.setdefault(lab, [x0, y, x1, y, 0])
            r[0] = min(r[0], x0); r[1] = min(r[1], y)
            r[2] = max(r[2], x1); r[3] = max(r[3], y)
            r[4] += x1 - x0 + 1
        vorig = [(runs[i][0], runs[i][1], labels[i]) for i in range(len(runs))]

    samen = {}
    for lab, r in vak.items():
        k = vind(lab)
        s = samen.get(k)
        if s is None:
            samen[k] = list(r)
        else:
            s[0] = min(s[0], r[0]); s[1] = min(s[1], r[1])
            s[2] = max(s[2], r[2]); s[3] = max(s[3], r[3])
            s[4] += r[4]
    return [v for v in samen.values() if v[4] > minpx]


def herstel_schaduw(deel):
    """Buitenom: donkere schaduw met de juiste dekking. Binnenin: ongemoeid."""
    b, h = deel.size
    px = deel.load()
    buiten = [[False] * b for _ in range(h)]
    rij = deque()
    for x in range(b):
        rij.append((x, 0)); rij.append((x, h - 1))
    for y in range(h):
        rij.append((0, y)); rij.append((b - 1, y))
    while rij:
        x, y = rij.popleft()
        if not (0 <= x < b and 0 <= y < h) or buiten[y][x]:
            continue
        if not is_buiten(px[x, y]):
            continue                      # tekening: hier houdt het op
        buiten[y][x] = True
        rij.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    uit = Image.new("RGBA", (b, h))
    up = uit.load()
    for y in range(h):
        for x in range(b):
            if not buiten[y][x]:
                up[x, y] = px[x, y]
                continue
            L = op_wit(px[x, y])
            a = int(round(255 * (255 - L) / 255.0))
            up[x, y] = SCHADUWKLEUR + (max(0, min(255, a)),)
    return uit


def splits_te_hoge(im, comps, maxhoogte=260):
    """Twee objecten die elkaar op het blad net raken tellen als een stuk. Op
       dit blad staat de boom met zijn stam tegen het standbeeld eronder. Zit
       er een duidelijke insnoering in, dan knippen we daar door."""
    px = im.load()

    def inkt(x, y):
        p = px[x, y]
        return p[3] > 120 and op_wit(p) < INKT

    uit = []
    for (x0, y0, x1, y1, n) in comps:
        if y1 - y0 <= maxhoogte:
            uit.append((x0, y0, x1, y1, n))
            continue
        a, b = y0 + int((y1 - y0) * 0.30), y0 + int((y1 - y0) * 0.70)
        smalst, smalste_y = None, None
        for y in range(a, b + 1):
            breed = sum(1 for x in range(x0, x1 + 1) if inkt(x, y))
            if smalst is None or breed < smalst:
                smalst, smalste_y = breed, y
        print("  gesplitst op y=%d (insnoering %d px breed)" % (smalste_y, smalst))
        uit.append((x0, y0, x1, smalste_y - 1, n // 2))
        uit.append((x0, smalste_y + 1, x1, y1, n // 2))
    return uit


def knip_vak(bladmaat, eigen, alle):
    """Het uitsnijvak met wat lucht eromheen, maar nooit tot in de buur. Zonder
       die begrenzing komt er bij dicht op elkaar staande objecten een reepje
       van het buurobject mee."""
    x0, y0, x1, y1 = eigen
    l, b = x0 - MARGE, x1 + 1 + MARGE
    t, o = y0 - MARGE, y1 + 1 + MARGE
    for (ax0, ay0, ax1, ay1, _n) in alle:
        if (ax0, ay0, ax1, ay1) == eigen:
            continue
        if not (ay1 < y0 or ay0 > y1):          # zelfde hoogte: links of rechts
            if ax1 < x0:
                l = max(l, (ax1 + x0) // 2 + 1)
            elif ax0 > x1:
                b = min(b, (x1 + ax0) // 2)
        if not (ax1 < x0 or ax0 > x1):          # zelfde kolom: boven of onder
            if ay1 < y0:
                t = max(t, (ay1 + y0) // 2 + 1)
            elif ay0 > y1:
                o = min(o, (y1 + ay0) // 2)
    return (max(0, l), max(0, t), min(bladmaat[0], b), min(bladmaat[1], o))


def main():
    im = Image.open(BRON).convert("RGBA")
    comps = splits_te_hoge(im, componenten(im))
    # In leesvolgorde. Rijen niet met vaste banden bepalen: de objecten in een
    # rij verschillen sterk in hoogte en dan valt een hoge boom over de
    # bandgrens. Groeperen op het midden van elk stuk.
    comps.sort(key=lambda c: (c[1] + c[3]) / 2)
    rijen, huidig, vorig_midden = [], [], None
    for c in comps:
        midden = (c[1] + c[3]) / 2
        if vorig_midden is not None and midden - vorig_midden > 100:
            rijen.append(sorted(huidig, key=lambda k: k[0]))
            huidig = []
        huidig.append(c)
        vorig_midden = midden
    if huidig:
        rijen.append(sorted(huidig, key=lambda k: k[0]))

    if [len(r) for r in rijen] != [len(r) for r in PLAN]:
        print("LET OP: gevonden %s, verwacht %s" %
              ([len(r) for r in rijen], [len(r) for r in PLAN]))

    os.makedirs(DOEL, exist_ok=True)
    for ri, rij in enumerate(rijen):
        for ci, (x0, y0, x1, y1, _n) in enumerate(rij):
            naam = (PLAN[ri][ci] if ri < len(PLAN) and ci < len(PLAN[ri])
                    else "onbekend-%d-%d" % (ri, ci))
            vak = knip_vak(im.size, (x0, y0, x1, y1), comps)
            deel = herstel_schaduw(im.crop(vak))
            deel.save(os.path.join(DOEL, naam + ".png"), optimize=True)
            print("geschreven: %-20s %dx%d" % (naam + ".png", vak[2] - vak[0], vak[3] - vak[1]))
            # Een liggend object heeft ook een staande vorm nodig: de player
            # vraagt bed-2x1 en bed-1x2 apart op. Het blad tekent er maar een,
            # dus draaien we de andere erbij.
            if "-" in naam and naam.rsplit("-", 1)[-1] in ("2x1", "3x1"):
                stam, maat = naam.rsplit("-", 1)
                gedraaid = "%s-%sx%s" % (stam, maat[2], maat[0])
                deel.rotate(90, expand=True).save(
                    os.path.join(DOEL, gedraaid + ".png"), optimize=True)


if __name__ == "__main__":
    main()
