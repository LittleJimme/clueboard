# Stijlbladen

De sierstukken en bordtekeningen komen van een klein aantal grote stijlbladen
die de gebruiker rendert (ChatGPT/Gemini). Werkwijze:

1. Render een blad met de prompt hieronder; herhaal tot het bevalt.
2. Geef bij elk volgend blad het goedgekeurde vorige blad mee als
   referentieafbeelding, met de zin: "Match the style, palette and lighting
   of the attached style sheet exactly."
3. Sla goedgekeurde bladen op in `assets/render/inbox/` als
   `stijlblad-ui.png`, `stijlblad-bord.png`, `stijlblad-texturen.png`.
4. Meld het in de chat; de sprites worden dan uitgesneden, schoongemaakt en
   ingebouwd (de `--ui-*`-tokens in de player-CSS wijzen per stuk naar één
   bestand).

De maatstreepjes die de generator bij de elementen tekent zijn welkom: ze
vallen buiten de uitsnede en maken de onderlinge schaal controleerbaar.

## Resolutie

De player schaalt elk beeld naar zijn vak (CSS background 100%/contain en
object-fit op het bord), nooit andersom. Een render in hogere resolutie
onder dezelfde bestandsnaam maakt het beeld dus alleen scherper, nooit
groter. Wat wél vast moet blijven per stuk: de beeldverhouding en een
strakke, gelijke marge rond het object. Bordobjecten proberen eerst
`<thema>/<naam>.png`, dan `<thema>/<naam>.svg`, dan de basistekening.

## Vakmaten (beeldverhouding per stuk, voor losse her-renders)

| Stuk               | Verhouding b:h | Let op |
|--------------------|----------------|--------|
| titelbord          | ±3,5:1         | kroontje bovenop telt mee in de hoogte |
| Controleer-schild  | 1,75:1         | breed schild, kroon telt mee |
| knopschildje       | 1:1,1          | |
| tabblad            | 3,5:1          | platte onderkant |
| timer-rol          | 2,5:1          | |
| lint               | 4:1            | wordt nine-slice: uiteinden blijven heel, midden rekt |
| plaquette          | 4:1            | ook nine-slice (staat op smalle én brede vakken) |
| perkamentvel       | 4:5            | nine-slice bij panelen |
| lakzegel           | 1:1            | |
| portretschild      | 1:1,1          | binnenvlak egaal lichtgrijs |
| lauwerkrans        | 1:1,1          | binnenvlak egaal lichtgrijs |
| bordobject 1×1     | 1:1            | object vult ±86% van het vak, marge overal gelijk |
| bordobject 2×1     | 2:1            | bed-2x1, tafel-2x1 |
| rol-embleem        | 1:1,1          | schild/banier/kap/schort achter portretten |

## Vaste stijlregels (onder elke prompt plakken)

> Style requirements: Game art for a storybook medieval deduction board game.
> Painted illustration style with soft brushwork and visible texture, warm
> daylight palette, clean dark-brown ink outlines, gentle highlights, soft
> baked drop shadow. Palette: parchment cream #F3E7CC, oak wood #8A6134 and
> #6E4B26, deep heraldic blue #2E4A78, antique gold #C9A227, dark ink
> #2A1B0C. Straight front view, no perspective tilt. IMPORTANT: absolutely no
> text, no letters, no numbers and no watermark on or inside the objects
> (small grey measurement marks beside the objects are allowed). The
> background must be plain, flat, PURE WHITE (#FFFFFF): no color, no
> gradient, no texture, no vignette behind the objects.

## Blad 1 — UI-stukken (GOEDGEKEURD, 2026-08-31)

Dertien stukken: titelbord met embleem, kroonschild, perkamentvel,
ridder-embleem, edele-banier, portretschild, lauwerkrans, knopschildje,
tabbladen (zwak gelukt — los nagenereren of recht afsnijden), plaquette,
lakzegel, perkamentrol, blauw lint. Prompt: zie de gespreksgeschiedenis van
2026-08-31; het goedgekeurde blad is de referentie voor alle volgende bladen.

## Blad 2 — Bordelementen (v2: de hoek vastgezet)

Eerste render (2026-08-31) had een kloppende stijl maar een zwevende
camerahoek: stoel, tafels, bedden, krat en paard stonden in driekwart- of
isometrisch aanzicht met zichtbare bovenkanten, en het paard was te
realistisch. Meteen bruikbaar uit die render: fiche, kruis, naamplaatje,
wachter/monnik/knecht-emblemen, struik, stenen, ton. De v2-prompt zet de
hoek vast:

> A single sprite sheet with the OBJECTS that stand on the game board, all
> painted in exactly the same style, palette and lighting as the attached
> approved style sheet (soft light from the upper left), arranged in four
> tidy rows with generous even spacing, nothing overlapping, nothing
> cropped. CAMERA RULE, the most important rule of this sheet: every object
> is drawn in strict FLAT FRONT ELEVATION, like scenery pieces on a theatre
> stage seen from the audience. The camera is level with the object. NO top
> surfaces visible, NO isometric or three-quarter angle, NO receding
> perspective: front legs and back legs of furniture stand on one straight
> base line, and a tabletop or seat shows only as one thin straight
> horizontal band. Every object gets a small soft ground shadow directly
> under its base line. Bold, simple, readable at small size. Use a
> consistent scale: 1 unit = one floor tile; the wooden chair is 0.8 units
> tall.
> ROW 1, wooden furniture: (1) a simple wooden chair, straight front view,
> 0.8 units; (2) a small square wooden table, front view, 0.9 units; (3) a
> long wooden table, front view, 2 units wide and 1 unit tall; (4) a low
> wooden bench, front view, 1.2 units wide; (5) a wooden barrel with two
> steel bands, 0.7 units; (6) a closed wooden crate, pure front face only
> with a cross of planks, 0.7 units.
> ROW 2, large pieces: (7) a single bed seen straight from the front side
> (footboard-to-headboard runs parallel to the picture plane), with a cream
> pillow at the head end and a green blanket, 1 unit wide; (8) the same bed
> as a wide double: two pillows, same green blanket, 2 units wide and 1
> unit tall; (9) a simple, chunky storybook cartoon horse in side profile
> facing left, big simple shapes, short legs on one base line, NOT
> realistic, 1.1 units tall.
> ROW 3, nature: (10) a round leafy tree with a short trunk, front view, 1
> unit; (11) a low round shrub, 0.7 units; (12) a small cluster of two or
> three grey boulders, 0.7 units.
> ROW 4, board markers and remaining character emblems: (13) a flat round
> game token with a carved wooden rim and a plain cream centre, 0.5 units,
> empty centre; (14) a bold hand-painted dark red X cross mark, two short
> brush strokes, 0.5 units; (15) a small horizontal parchment name plate
> with slightly rough edges, 1.4 by 0.4 units, empty centre; (16) a guard's
> emblem: a rounded steel shield with a vertical and a horizontal
> reinforcement band, 1.5 units tall, empty centre; (17) a monk's emblem: a
> simple raised fabric hood in undyed brown cloth, front view, 1.5 units
> tall; (18) a servant's emblem: a simple cream apron with a waist tie, 1.5
> units tall.

(plus de vaste stijlregels)

## Blad 3 — Ondergronden en texturen (v2: met rand- en padstroken)

Blad 2 (bordobjecten) is geparkeerd: de camerahoek wilde niet vast komen te
zitten. Randen en paden worden AUTOTILING in de player: de JSON houdt alleen
het vloertype per tegel, de player kiest per tegel zelf basis-, rand- of
hoekwerk op grond van de buren (die data heeft hij al). Niets hiervan komt
in de builder of de leveldata. Generators tegelen zelden echt naadloos; de
naden worden bij het uitsnijden gerepareerd.

> A single sheet of ground TEXTURES for the game, all painted in exactly
> the same style and palette as the attached approved style sheet, laid out
> in a tidy grid with clear white gaps between all pieces.
> PART A, eight equal seamless squares. Each square is completely filled
> edge to edge, evenly and flatly lit (no vignette, no border, no objects,
> no shadows), and must tile seamlessly when repeated left-right and
> top-bottom: (1) warm oak floorboards, horizontal planks; (2) grey stone
> floor of rounded cobbles; (3) pale ceramic floor tiles in a simple grid;
> (4) soft green meadow grass with tiny tufts and a few small flowers; (5)
> packed light-brown dirt, the surface of a country road, with subtle wheel
> tracks and small pebbles; (6) a dark pine-green felt table cloth with a
> fine woven fabric grain; (7) rough grey castle wall masonry; (8) cream
> parchment with soft aged mottling.
> PART B, three wide transition strips, each as wide as four of the squares
> above and one square tall, tiling seamlessly along their horizontal
> length only: (9) a grass edge: the top half is the same meadow grass as
> square 4, ending in an irregular, lively fringe of overhanging tufts and
> blades along the middle, the bottom half plain pure white; (10) a dirt
> path running horizontally through meadow grass: the same dirt as square 5
> in the middle as a slightly wavy, irregular band, the same grass as
> square 4 above and below it, with lively ragged grass fringes where they
> meet; (11) the same dirt path making one smooth quarter-turn curve from
> the left edge to the bottom edge, grass around it, same ragged fringes.
> PART C, one wide rectangle, 16:9: a calm storybook landscape background:
> soft blue sky with a few clouds at the top, distant rolling green hills
> and a small castle on the horizon in the upper third, the lower two
> thirds fading into soft, low-contrast muted parchment-green tones so
> interface cards remain readable on top of it.
> Style requirements: (de vaste stijlregels, met als aanzicht: straight
> top-down view for all ground textures, no perspective.)
