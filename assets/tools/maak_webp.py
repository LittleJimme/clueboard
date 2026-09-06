# -*- coding: utf-8 -*-
"""Zet naast elke tekening die het spel laadt een WebP-versie klaar.

De PNG's blijven de bron: daar schrijven de importscripts naartoe en daar
kijk je in als er iets mis is. Het spel laadt de WebP en valt terug op de
PNG als die er niet is. Een WebP op kwaliteit 88 is op het bord niet van de
PNG te onderscheiden en ruim vijf keer zo klein -- op een telefoon scheelt
dat per zaak een paar megabyte aan wachten.

Draai dit na elke import van nieuwe tekeningen:
    python assets/tools/maak_webp.py
Alleen tekeningen die nieuwer zijn dan hun WebP worden opnieuw gemaakt.
"""
import io, os, sys, time
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAPPEN = [
    os.path.join("assets", "art", "objects"),
    os.path.join("assets", "art", "overlays"),
    os.path.join("assets", "characters"),
]
KWALITEIT = 88


def schrijf(pad, beeld):
    tmp = pad + ".tmp"
    buf = io.BytesIO()
    beeld.save(buf, "WEBP", quality=KWALITEIT, method=6, exact=True)
    with open(tmp, "wb") as f:
        f.write(buf.getvalue())
    for _ in range(5):
        try:
            os.replace(tmp, pad); return
        except PermissionError:
            time.sleep(0.5)
    raise SystemExit("Kon niet schrijven: " + pad)


def main(alles=False):
    gemaakt = overgeslagen = 0
    bron_kb = webp_kb = 0
    for m in MAPPEN:
        for root, _, bestanden in os.walk(os.path.join(WORTEL, m)):
            for naam in bestanden:
                stam, ext = os.path.splitext(naam)
                if ext.lower() not in (".png", ".jpg", ".jpeg"):
                    continue
                bron = os.path.join(root, naam)
                doel = os.path.join(root, stam + ".webp")
                if not alles and os.path.exists(doel) and os.path.getmtime(doel) >= os.path.getmtime(bron):
                    overgeslagen += 1
                    continue
                beeld = Image.open(bron)
                # Een JPG heeft geen doorzichtigheid; alles met alpha blijft RGBA.
                beeld = beeld.convert("RGBA" if "A" in beeld.getbands() or beeld.mode == "P" else "RGB")
                schrijf(doel, beeld)
                gemaakt += 1
                bron_kb += os.path.getsize(bron) // 1024
                webp_kb += os.path.getsize(doel) // 1024
    print("webp: %d gemaakt, %d al bij; %d KB -> %d KB" % (gemaakt, overgeslagen, bron_kb, webp_kb))


if __name__ == "__main__":
    main(alles="--alles" in sys.argv)
