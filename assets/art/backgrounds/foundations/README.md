# Vloer-foundations (lichte skin)

Elke PNG hier is **één gameplayvakje**: 128×128, verhouding 1:1. Ze zijn
uitgesneden uit het goedgekeurde stijlvel
`assets/art/concepts/clueboard-light-floor-foundations-style-sheet-v3-imagegen-light-reference.png`
door `assets/tools/cut_floors.py`.

In elke tekening zit de belichting die overal gelijk is: zacht licht langs
boven en links, warme schaduw langs onder en rechts, een heel ondiepe bevel en
een brede lichtval van linksboven naar rechtsonder. Die richting staat vast in
wereldcoördinaten en wordt nooit per tegel gedraaid.

Binnen een vakje staat nooit een kleiner raster — geen voegen, bakstenen,
planken of ruiten. De naad die je op het bord ziet is de rand van het vakje
zelf. De hoeken zijn licht afgerond, dus waar vier tegels samenkomen blijft een
klein vlekje voeg staan; dat leest als vier losse tegels die tegen elkaar aan
zijn gelegd.

## Zes structurele foundations, elf vloer-id's

| foundation | vloer-id's | bestand(en) |
|---|---|---|
| mineraal | `stone` `concrete` `tile` `marble` | stone.png, concrete.png, tile.png, marble.png |
| aarde | `dirt` `sand` `gravel` | dirt.png, sand.png, gravel.png |
| hout | `wood` | wood.png |
| gras | `grass` | grass.png |
| linnen/vilt | `carpet` | carpet.png |
| water | `water` | water.png |

Binnen een familie deelt de tegel dezelfde structuur uit het stijlvel en
verschilt vooral de kleur.

## Bijwerken

Pas het stijlvel aan (of de coördinaten in `cut_floors.py`) en draai:

    python assets/tools/cut_floors.py

De speler koppelt de bestanden aan de vloer-id's in de CSS onder
"Lichte vloer-foundations". Ontbreekt een bestand, dan blijft de vlakke
voegkleur van dat materiaal staan — nooit een herhalend patroon.

De oude geschilderde vloeren staan nog in `../medieval/` voor vergelijking;
die worden in deze skin niet meer geladen.
