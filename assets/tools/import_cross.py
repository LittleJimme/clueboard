# -*- coding: utf-8 -*-
"""Snijdt het kruisje uit zijn witte achtergrond en zet het in de bank.

Uit Photoshop komt een rood kruis op wit. De achtergrond is bijna neutraal
(rood min blauw is er 3) en het kruis juist sterk rood (rond de 142), dus dat
verschil is een schone maat voor de dekking: binnen het kruis loopt hij door
tot boven de drempel en klapt hij op vol, en alleen de zachte rand krijgt een
tussenwaarde.

Daarna moet het wit er nog uit gerekend worden. Photoshop heeft namelijk
gestapeld als P = a*C + (1-a)*wit; wie alleen de dekking zet en de kleur laat
staan, houdt aan de rand een lichtroze zoom over die op een donkere vloer als
een spookrand oplicht.
"""
import os, sys, time
import numpy as np
from PIL import Image

WORTEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRON = os.path.join(WORTEL, "assets", "art", "production", "occupied-markers",
                    "occupied-cross-c-white-v1.png")
DOEL = os.path.join(WORTEL, "assets", "art", "overlays", "kruis.png")
MAAT = 384      # het kruis beslaat 70% van een vakje; ook op een groot scherm ruim
DREMPEL = 120   # hierboven is het kruis vol dekkend

def main():
    if not os.path.exists(BRON):
        print("bron ontbreekt:", BRON); return 1
    a = np.asarray(Image.open(BRON).convert("RGB"), dtype=np.float64)
    achter = np.array([254.0, 253.0, 251.0])          # het papier uit Photoshop
    dekking = np.clip((a[:, :, 0] - a[:, :, 2] - 3.0) / (DREMPEL - 3.0), 0.0, 1.0)

    # Het wit eruit rekenen: C = (P - achtergrond*(1-a)) / a
    d = np.maximum(dekking, 1e-6)[:, :, None]
    kleur = np.clip((a - achter * (1.0 - d)) / d, 0.0, 255.0)
    kleur[dekking < 0.02] = 0.0                        # volledig doorzichtig: kleur doet niet mee

    uit = np.concatenate([kleur, dekking[:, :, None] * 255.0], axis=2)
    im = Image.fromarray((uit + 0.5).astype(np.uint8), "RGBA").resize((MAAT, MAAT), Image.LANCZOS)
    os.makedirs(os.path.dirname(DOEL), exist_ok=True)
    tmp = DOEL + ".tmp"
    im.save(tmp, format="PNG", optimize=True)
    for _ in range(8):
        try:
            os.replace(tmp, DOEL); break
        except PermissionError:
            time.sleep(1)
    print("kruis %d x %d, %d kB" % (MAAT, MAAT, os.path.getsize(DOEL) // 1024))
    return 0

if __name__ == "__main__":
    sys.exit(main())
