# -*- coding: utf-8 -*-
"""Tekent het app-icoon voor de menupagina (geinstalleerde webapp).

Zelfde beeldmerk als in de balk: drie vakjes en een loep, met een gevuld
accentvakje. Donkere ondergrond, zodat het icoon op elk startscherm past.

    python assets/tools/maak_menu_icoon.py
"""
import os
from PIL import Image, ImageDraw

DOEL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "ClueBoard Menu")

GROND = (35, 24, 25)        # --grond (bordeaux, het standaardthema)
CREME = (240, 232, 226)     # --inkt
ACCENT = (217, 165, 54)     # --accent (goud)


def teken(maat):
    """Het merkteken op 64x64-coordinaten, geschaald naar `maat`."""
    s = maat / 64.0
    im = Image.new("RGBA", (maat, maat), GROND + (255,))
    d = ImageDraw.Draw(im)

    def vak(x, y, b, r, vul=None, lijn=None, dikte=3):
        doos = [x * s, y * s, (x + b) * s, (y + b) * s]
        d.rounded_rectangle(doos, radius=r * s, fill=vul, outline=lijn,
                            width=max(1, int(round(dikte * s))))

    vak(10, 10, 17, 5, vul=ACCENT)
    vak(37, 10, 17, 5, lijn=CREME)
    vak(10, 37, 17, 5, lijn=CREME)

    # loep: cirkel plus steel
    d.ellipse([35 * s, 35 * s, 55 * s, 55 * s], outline=CREME,
              width=max(1, int(round(3.2 * s))))
    d.line([52.4 * s, 52.4 * s, 58.4 * s, 58.4 * s], fill=CREME,
           width=max(1, int(round(4 * s))))
    return im


for maat in (192, 512):
    pad = os.path.join(DOEL, "icon-%d.png" % maat)
    teken(maat).save(pad)
    print("geschreven:", os.path.basename(pad))
