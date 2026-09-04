# -*- coding: utf-8 -*-
"""Zet de tapijttextuur uit Photoshop klaar voor de bank.

Het bestand is een zacht reliëf dat over het hele tapijt heen gaat, bedoeld
voor een gebied van vijf bij vijf vakjes. Het origineel is 1254 pixels in het
vierkant en weegt 2,4 MB als PNG -- veel te veel voor een laag die je nauwelijks
ziet. De tekening loopt maar van 202 tot 255 en is vrijwel kleurloos, dus JPEG
kan hem zonder zichtbaar verlies tot een fractie terugbrengen. Alpha is niet
nodig: de laag vermenigvuldigt of screent, hij dekt niets af.
"""
import io, os, sys, time
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "assets", "art", "production", "carpet-light-mode",
                    "carpet-overlay-5x5-multiply-light-v1.png")
DOEL = os.path.join(WORTEL, "assets", "art", "overlays", "mat-textuur.jpg")
MAAT = 768      # vijf vakjes breed; op een telefoon is een vakje zelden 75 pixels

def main():
    if not os.path.exists(BRON):
        print("bron ontbreekt:", BRON); return 1
    im = Image.open(BRON).convert("RGB").resize((MAAT, MAAT), Image.LANCZOS)
    os.makedirs(os.path.dirname(DOEL), exist_ok=True)
    tmp = DOEL + ".tmp"
    im.save(tmp, format="JPEG", quality=90, optimize=True, subsampling=0)
    for _ in range(8):
        try:
            os.replace(tmp, DOEL); break
        except PermissionError:
            time.sleep(1)
    print("tapijttextuur %d x %d, %d kB" % (MAAT, MAAT, os.path.getsize(DOEL) // 1024))
    return 0

if __name__ == "__main__":
    sys.exit(main())
