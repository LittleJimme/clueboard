# Vloertexturen — thema Middeleeuwen

Uitgesneden uit het tegelblad *ClueBoard Medieval – Floor Tile Set*
(18 tegels, 3×6). Elke tegel is binnen zijn afgeronde hoek en zijn donkere
omlijning uitgesneden en op 256×256 gezet, zodat aangrenzende vakjes op het
bord tegen elkaar aan sluiten in plaats van elk een randje te tonen.

## Hoe ze gebruikt worden

De player koppelt op **bestandsnaam**, niet via het manifest. `applyFloorArt()`
zoekt per vloertype naar `floor-<id>.png` in deze map en valt terug op de
gedeelde map en daarna op de ingebouwde SVG-textuur. Een bestand hier
neerzetten is dus genoeg; er hoeft geen regel code bij.

De `<id>` is het vloer-id uit `ROOM_FLOORS` in de bouwer.

## Varianten

Van een aantal vloeren staan er meerdere tekeningen klaar. De eerste heet
`floor-<id>.png`, de volgende `floor-<id>-2.png`, `-3.png`, enzovoort. Hoeveel
het er zijn staat in `manifest.json` onder `floorArt.variants`.

De player deelt ze **per kamer** uit: de eerste kamer met houten vloer krijgt
`floor-wood`, de tweede `floor-wood-2`, de derde `floor-wood-3`. Zo lopen twee
kamers met hetzelfde materiaal niet in elkaar over. Zijn er meer kamers dan
varianten, dan begint het rijtje opnieuw. De volgorde is die van de kamers in
het level, dus hij ligt vast.

| vloer | varianten |
|---|---|
| Gras | 6 |
| Steen | 4 |
| Houten vloer | 4 (licht, warm, donker, visgraat) |
| Water | 4 (ondiep, helder, diep, donker) |
| Zand | 2 |
| Aarde | 2 |
| Tegelvloer, Beton, Grind | 1 |

## Wat waar vandaan komt

| bestand | vloer in het spel | tegel op het blad |
|---|---|---|
| `floor-grass*.png`   | Gras         | blad 2, GRAS 1 t/m 6 |
| `floor-stone*.png`   | Steen        | blad 2, STEEN 1 t/m 4 |
| `floor-wood*.png`    | Houten vloer | blad 2, HOUT 1 t/m 3 + PARKET |
| `floor-water*.png`   | Water        | blad 2, WATER 1 t/m 4 |
| `floor-sand*.png`    | Zand         | blad 2, ZAND 1 en 2 |
| `floor-dirt*.png`    | Aarde        | blad 2, ZAND 3 en 4 |
| `floor-tile.png`     | Tegelvloer   | blad 1, TERRACOTTA |
| `floor-concrete.png` | Beton        | blad 1, PLEISTER – WARM |
| `floor-gravel.png`   | Grind        | blad 1, GRIND |

## Nog zonder textuur

Voor deze vloeren staat er niets passends op de bladen; ze houden hun
ingebouwde tekening: **Marmer, Metaal, Tapijt, Sneeuw**.

## Klaar voor later

Vier tegels van blad 1 staan er onder hun eigen naam bij:
`baksteen`, `pleister-licht`, `leem`, `leisteen`. De andere extra's van
blad 1 (steen-licht/-donker, keien, hout-licht/-donker, parket) zijn
vervallen: blad 2 heeft daar betere versies van, en die zitten in de
varianten hierboven.

Voeg je zo'n naam als id toe aan `ROOM_FLOORS` in de bouwer, dan pakt de
player de bijbehorende textuur meteen op — er is verder niets te koppelen.

## Opnieuw uitsnijden

Het snijscript staat in `assets/tools/snij_vloertegels.py` en kent beide
bladen: `python assets/tools/snij_vloertegels.py set1` of `set2`. De bronnen
staan in `assets/render/inbox/`.
