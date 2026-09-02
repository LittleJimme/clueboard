# Herkomst van de assets

## Iconen en tekeningen

Alles in `icons/` en `art/` is voor dit project getekend. Vrij te gebruiken en
aan te passen binnen ClueBoard.

## Kenney

De kits van [Kenney](https://kenney.nl) staan onder **CC0 1.0** (publiek
domein): vrij te gebruiken, aan te passen en te verspreiden, ook commercieel,
zonder verplichte naamsvermelding. Vermelding blijft netjes, vandaar dit
bestand.

Overgenomen (inmiddels verplaatst naar `_archief/assets/kenney/`) zijn acht middeleeuws bruikbare kits:
furniture-kit, nature-kit, mini-dungeon, mini-forest, mini-market,
mini-characters, mini-arena en graveyard-kit &mdash; per model één preview en de
GLB.

Ze worden **als bron** gebruikt, niet als runtime-asset: het zijn 3D-modellen en
isometrische tegels, en die passen niet zonder bewerking op een orthogonaal
raster. De bedoeling is ze offline te renderen naar platte tegels met een vaste
camera (fase 9 van de overhaul), waarna alleen het resultaat in `art/` belandt.
Tot die tijd dienen de previews om aan de look en feel te werken.
