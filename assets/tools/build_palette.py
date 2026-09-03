"""Zet het vlakke kleurenpalet uit de JSON in de player.

Bron van waarheid:
  assets/art/concepts/clueboard-floor-wall-flat-colors-day-night-v1.json

De kleuren staan daar één keer. Dit script schrijft ze als één blok in
player/index.html, tussen de twee merktekens hieronder. Nergens anders in de
speler staat een vloer- of muurkleur; alles leest uit dat ene blok.

Draaien na een wijziging in de JSON:
    python assets/tools/build_palette.py
"""
import io, json, os, time

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "assets", "art", "concepts",
                    "clueboard-floor-wall-flat-colors-day-night-v1.json")
DOEL = os.path.join(WORTEL, "player", "index.html")
START = "/* @palet-begin */"
EIND = "/* @palet-eind */"


def main():
    data = json.load(io.open(BRON, encoding="utf-8"))
    vloeren = {f["id"]: {"dag": f["day"], "nacht": f["night"]} for f in data["floors"]}
    muren = {w["id"]: {"dag": w["day"], "nacht": w["night"]} for w in data["walls"]}
    ctx = data.get("contexts") or {}

    regels = ["const VLAK_PALET = {"]
    regels.append('  bron:"%s v%s",' % (data.get("format", "?"), data.get("version", "?")))
    regels.append("  vloeren:{")
    for k, v in vloeren.items():
        regels.append('    %-9s:{dag:"%s",nacht:"%s"},' % (k, v["dag"], v["nacht"]))
    regels.append("  },")
    regels.append("  muren:{")
    for k, v in muren.items():
        sleutel = k.replace("wall-", "")
        regels.append('    %-9s:{dag:"%s",nacht:"%s"},' % (sleutel, v["dag"], v["nacht"]))
    regels.append("  },")
    regels.append('  grond:{dag:"%s",nacht:"%s"},' % (ctx.get("day", "#F8F4EC"), ctx.get("night", "#252C35")))
    regels.append("};")
    blok = "\n".join(regels)

    t = io.open(DOEL, encoding="utf-8").read()
    i, j = t.index(START), t.index(EIND)
    nieuw = t[:i + len(START)] + "\n" + blok + "\n" + t[j:]
    tmp = DOEL + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(nieuw)
    for _ in range(5):
        try:
            os.replace(tmp, DOEL); break
        except PermissionError:
            time.sleep(0.5)
    print("%d vloeren en %d muren uit %s in de player gezet"
          % (len(vloeren), len(muren), os.path.basename(BRON)))


if __name__ == "__main__":
    main()
