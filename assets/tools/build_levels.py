"""Zet de lijst en het overzicht van de levels klaar.

Het menu hoeft van een zaak maar een handjevol dingen te weten: de titel, de
zwaarte, hoe groot het bord is en welk nummer hij heeft. Dat stond tot nu toe
alleen in het levelbestand zelf, dus haalde het menu elk bestand helemaal op
-- tientallen kilobytes per zaak, terwijl er een paar regels van in beeld
komen. Dit script schrijft die paar regels van alle zaken samen in een klein
overzicht, zodat het menu aan één bestand genoeg heeft. Het volledige level
wordt pas geladen als je erop klikt.

Twee bestanden komen eruit:
  index.json      welke bestanden er zijn (de speler gebruikt deze ook)
  overzicht.json  per zaak het handjevol velden dat het menu toont

Draai dit na het toevoegen of wijzigen van een level:
    python assets/tools/build_levels.py
"""
import io, json, os, sys, time

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEVELS = os.path.join(WORTEL, "player", "Levels")

def schrijf(pad, tekst):
    tmp = pad + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(tekst)
    for _ in range(5):
        try:
            os.replace(tmp, pad); return
        except PermissionError:
            time.sleep(0.5)
    raise SystemExit("Kon niet schrijven: " + pad)

def geldig(raw):
    """Dezelfde eisen als de speler stelt; een half bestand hoort er niet in."""
    if not isinstance(raw, dict): return "geen object"
    p = raw.get("puzzle")
    if not isinstance(p, dict): return "puzzle ontbreekt"
    g = p.get("grid") or {}
    if not g.get("columns") or not g.get("rows"): return "grid onvolledig"
    if not p.get("tiles"): return "tiles ontbreken"
    mensen = (p.get("people") or {}).get("placements")
    if not mensen: return "people.placements ontbreekt"
    if not (raw.get("solution") or {}).get("placements"): return "solution ontbreekt"
    return None

def samenvatting(raw, bestand):
    """Alleen wat er op een kaart in het menu komt te staan."""
    p = raw.get("puzzle") or {}
    g = p.get("grid") or {}
    c = raw.get("content") or {}
    d = raw.get("difficulty") or {}
    uit = {
        "file": bestand,
        "content": {"title": c.get("title") or "Naamloos niveau"},
        "puzzle": {"grid": {"columns": g.get("columns"), "rows": g.get("rows")}},
    }
    for veld in ("levelId", "levelNumber", "levelVersion"):
        if raw.get(veld) is not None: uit[veld] = raw[veld]
    if raw.get("demo") is True: uit["demo"] = True
    if d.get("graad"):
        uit["difficulty"] = {"graad": d["graad"]}
        if d.get("uitleg"): uit["difficulty"]["uitleg"] = d["uitleg"]
    if p.get("theme"): uit["puzzle"]["theme"] = p["theme"]
    if p.get("themeLabel"): uit["puzzle"]["themeLabel"] = p["themeLabel"]
    return uit

def main():
    if not os.path.isdir(LEVELS):
        raise SystemExit("Map niet gevonden: " + LEVELS)
    bestanden = sorted(n for n in os.listdir(LEVELS)
                       if n.lower().endswith(".json") and n.lower() not in ("index.json", "overzicht.json"))
    lijst, kaarten, overgeslagen = [], [], []
    for naam in bestanden:
        pad = os.path.join(LEVELS, naam)
        try:
            raw = json.load(io.open(pad, encoding="utf-8"))
        except Exception as e:
            overgeslagen.append((naam, "onleesbaar: %s" % e)); continue
        fout = geldig(raw)
        if fout:
            overgeslagen.append((naam, fout)); continue
        lijst.append(naam)
        kaarten.append(samenvatting(raw, naam))
    schrijf(os.path.join(LEVELS, "index.json"),
            json.dumps(lijst, ensure_ascii=False, indent=2) + "\n")
    schrijf(os.path.join(LEVELS, "overzicht.json"),
            json.dumps({"gemaakt": time.strftime("%Y-%m-%dT%H:%M:%S"), "levels": kaarten},
                       ensure_ascii=False, indent=2) + "\n")
    groot = sum(os.path.getsize(os.path.join(LEVELS, n)) for n in lijst)
    klein = os.path.getsize(os.path.join(LEVELS, "overzicht.json"))
    print("%d zaken in de lijst" % len(lijst))
    for n, r in overgeslagen: print("  overgeslagen: %-44s %s" % (n, r))
    print("het menu haalde %.0f kB op, nu %.0f kB" % (groot / 1024.0, klein / 1024.0))

if __name__ == "__main__":
    main()
