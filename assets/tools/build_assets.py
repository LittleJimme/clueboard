# -*- coding: utf-8 -*-
"""
build_assets.py — bakt de assetbank in de builder en de player.

De bank in assets/ is de bron van waarheid. Dit script leest manifest.json plus
de losse SVG-iconen en schrijft die als één JavaScript-blok in beide HTML-
bestanden, tussen de markers:

    /* @clueboard:assets-begin */ ... /* @clueboard:assets-end */

Alles buiten die markers blijft ongemoeid. De builder blijft daardoor één
zelfstandig bestand: de 24x24 lijniconen staan er inline in, en de gekleurde
tekeningen uit assets/art/ worden alleen gebruikt als ze naast het bestand
staan. Draai dit script na elke wijziging in assets/.

Gebruik:  python assets/tools/build_assets.py [--check]
          --check schrijft niets en meldt alleen of de bestanden bij zijn.
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)
ROOT = os.path.dirname(ASSETS)

TARGETS = [
    os.path.join(ROOT, "ClueBoard Builder", "clueboard-builder.html"),
    os.path.join(ROOT, "ClueBoard Player", "Build", "index.html"),
]
BEGIN = "/* @clueboard:assets-begin */"
END = "/* @clueboard:assets-end */"


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def write_atomic(path, text):
    """Nooit rechtstreeks over het doel schrijven: eerst .tmp, dan vervangen."""
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def icon_body(rel):
    """Alleen de tekenopdrachten uit een icoonbestand; de <svg>-wikkel komt uit de code."""
    src = read(os.path.join(ASSETS, rel))
    m = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S)
    if not m:
        sys.exit("geen <svg> gevonden in " + rel)
    return re.sub(r"\s+", " ", m.group(1)).strip()


def build_block():
    manifest = json.loads(read(os.path.join(ASSETS, "manifest.json")))
    icons = {}

    def take(rel):
        if rel and rel not in icons:
            icons[rel] = icon_body(rel)

    for o in manifest["objects"]:
        take(o.get("icon"))
    for u in manifest["ui"]:
        take(u.get("icon"))
    for r in manifest["roles"]:
        take(r.get("icon"))
    for s in manifest.get("spareIcons", []):
        take(s.get("icon"))

    compact = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    bodies = json.dumps(icons, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return (
        BEGIN + "\n"
        "/* Gegenereerd door assets/tools/build_assets.py uit assets/manifest.json.\n"
        "   Niet met de hand aanpassen: wijzig de bank en draai het script opnieuw. */\n"
        "const ASSET_MANIFEST = " + compact + ";\n"
        "const ASSET_ICON_BODIES = " + bodies + ";\n"
        + END
    )


def main():
    check = "--check" in sys.argv
    block = build_block()
    stale = []
    for path in TARGETS:
        if not os.path.exists(path):
            print("overgeslagen (bestaat niet):", path)
            continue
        src = read(path)
        i, j = src.find(BEGIN), src.find(END)
        if i < 0 or j < 0:
            print("GEEN MARKERS in", os.path.basename(path), "- overgeslagen")
            continue
        new = src[:i] + block + src[j + len(END):]
        if new == src:
            print("bij:", os.path.basename(path))
            continue
        stale.append(path)
        if not check:
            write_atomic(path, new)
            print("bijgewerkt:", os.path.basename(path))
        else:
            print("VEROUDERD:", os.path.basename(path))

    manifest = json.loads(read(os.path.join(ASSETS, "manifest.json")))
    print("bank: %d objecten, %d ui-iconen, %d rollen, %d reserve-iconen"
          % (len(manifest["objects"]), len(manifest["ui"]),
             len(manifest["roles"]), len(manifest.get("spareIcons", []))))
    if not check:
        write_preview(manifest)
    return 1 if (check and stale) else 0


def write_preview(manifest):
    """Contactvel van de hele bank, te openen via een lokale webserver."""
    rows = []
    groups = [("Rollen", [r["icon"] for r in manifest["roles"]]),
              ("Interface", [u["icon"] for u in manifest["ui"]]),
              ("Objecten", [o["icon"] for o in manifest["objects"] if o.get("icon")]),
              ("Reserve", [s["icon"] for s in manifest.get("spareIcons", [])])]
    for title, paths in groups:
        cells = []
        for rel in paths:
            name = os.path.basename(rel)[:-4]
            cells.append('<figure><span class="s20">%s</span><span class="s32">%s</span>'
                         '<figcaption>%s</figcaption></figure>'
                         % (read(os.path.join(ASSETS, rel)),
                            read(os.path.join(ASSETS, rel)), name))
        rows.append("<h2>%s <em>%d</em></h2><div class=grid>%s</div>" % (title, len(paths), "".join(cells)))

    art = sorted(os.listdir(os.path.join(ASSETS, "art", "objects")))
    cells = ['<figure><img src="art/objects/%s" alt=""><figcaption>%s</figcaption></figure>'
             % (fn, fn[:-4]) for fn in art]
    rows.append("<h2>Tekeningen <em>%d</em></h2><div class=grid>%s</div>" % (len(art), "".join(cells)))

    html = """<!doctype html><meta charset="utf-8"><title>ClueBoard assetbank</title>
<style>
 body{font:13px/1.5 system-ui,sans-serif;background:#EDF1F8;color:#151A33;margin:0;padding:24px}
 h1{font-size:20px;margin:0 0 4px} p.lead{margin:0 0 20px;color:#5A6382}
 h2{font-size:13px;text-transform:uppercase;letter-spacing:.08em;margin:26px 0 8px}
 h2 em{font-style:normal;color:#8b93ad;font-weight:400}
 .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(86px,1fr));gap:8px}
 figure{margin:0;background:#fff;border-radius:10px;padding:10px 4px;text-align:center}
 figure svg{color:#2B3358;display:block;margin:0 auto}
 .s20 svg{width:20px;height:20px} .s32 svg{width:32px;height:32px;margin-top:6px}
 figure img{width:48px;height:48px;object-fit:contain}
 figcaption{font-size:10px;color:#5A6382;margin-top:6px;word-break:break-word}
</style>
<h1>ClueBoard assetbank</h1>
<p class=lead>Gegenereerd door <code>assets/tools/build_assets.py</code>. Open via een lokale
webserver, niet via <code>file://</code> &mdash; anders laden de tekeningen niet.</p>
""" + "".join(rows) + "\n"
    write_atomic(os.path.join(ASSETS, "preview.html"), html)
    print("preview.html bijgewerkt")


if __name__ == "__main__":
    sys.exit(main())
