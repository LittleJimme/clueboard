# ClueBoard assetbank

Eén bank voor de builder én de player. Vóór deze map had elk van beide zijn
eigen iconen, waardoor ze uit elkaar liepen en een nieuw object twee keer
toegevoegd moest worden. Dat kan nu niet meer: alles staat hier.

```text
manifest.json     bron van waarheid: per objectsoort alles wat de app moet weten
icons/objects/    24x24 lijniconen, één per objectsoort
icons/ui/         24x24 lijniconen voor de interface
icons/roles/      24x24 lijniconen per stand (edele, ridder, ...)
art/objects/      gekleurde tekeningen voor het bord
art/characters/   gekleurde tekeningen per personage
art/backgrounds/  herhaalbare vloertexturen
tools/            buildscript
preview.html      contactvel van de hele bank
```

## Werkwijze

De iconen worden **ingebakken** in `builder/index.html` en
`player/index.html`, tussen de markers
`/* @clueboard:assets-begin */` en `/* @clueboard:assets-end */`. Daardoor
blijft de builder één zelfstandig bestand en heeft de player geen `fetch` nodig
die op `file://` toch geblokkeerd wordt.

Draai na **elke** wijziging in deze map:

```bash
python assets/tools/build_assets.py
```

`--check` schrijft niets en meldt alleen of beide bestanden bij zijn.

De gekleurde tekeningen in `art/` worden **niet** ingebakken — die worden op het
bord via een URL geladen. Ontbreekt zo'n bestand, dan blijft het ingebakken
lijnicoon staan. Er verschijnt nooit een foutmelding.

## Een objectsoort toevoegen

1. Zet een regel in `manifest.json` onder `objects`:

   ```json
   {
     "kind": "Chair",
     "slug": "chair",
     "label": "Stoel",
     "labelPlural": "stoelen",
     "article": "de",
     "category": "furniture",
     "group": "Zitten",
     "type": "occupiable",
     "pose": { "ww": "zat", "vz": "op" },
     "icon": "icons/objects/chair.svg",
     "art": ["chair.svg"],
     "maxTiles": 1,
     "themes": null
   }
   ```

2. Zet `icons/objects/chair.svg` neer (24x24 lijnicoon) en eventueel
   `art/objects/chair.svg` (gekleurde tekening).
3. Draai het buildscript.

`kind` is Engels en gaat zo de export in; `label` is wat de bouwer en de speler
zien. `article` en `labelPlural` zijn nodig voor de Nederlandse zinsopbouw van
regels: *"naast **een** stoel"*, *"naast twee **stoelen**"*. Vul ze altijd in —
de terugvalregel raadt en zit er bij woorden als *stoel* en *boom* naast.

`group` bepaalt onder welk kopje de soort in de buildermenu's staat.
`category` is de as waar de regelmotor op filtert: `furniture`, `animal`,
`nature`, `decor`, `terrain`, `vehicle` of `wall`. Die twee zijn met opzet los
van elkaar — een haai staat bij de bouwer onder *Obstakels*, maar is voor de
regels een dier.

`pose` is de houding: welk werkwoord en welk voorzetsel bij deze soort horen.
Op een stoel *zat* je, op een bed *lag* je, in een boot zat je *in*. De
regelmotor bouwt daar zijn zinnen mee ("Bart zat op de stoel", "Bart lag op het
bed"), dus vul het in bij elke soort met `type: "occupiable"`. Ontbreekt het,
dan valt de zin terug op *stond op* — precies goed voor een tafel of een kist,
maar fout voor alles waar je op zit of ligt.

`type` is `occupiable` (er kan iemand op staan) of `blocked`.
`maxTiles` is het aantal tegels dat de soort mag beslaan; `null` betekent 1 tot 3.
`themes` beperkt de soort tot bepaalde thema's; `null` betekent overal.

## Iconen tekenen

Canvas `0 0 24 24`, alleen lijnen, geen vulling, geen kleur:
`stroke="currentColor"`, `stroke-width="1.8"`, ronde uiteinden en hoeken. Het
buildscript pakt alleen de inhoud tussen `<svg>` en `</svg>`, dus de wikkel mag
je laten staan zoals hij is. Controleer je icoon op 20px in `preview.html` —
daar wordt het op het bord getoond.

`spareIcons` in het manifest zijn getekende iconen waar nog geen objectsoort bij
hoort (bank, spiegel, schilderij, kaars, lamp, haard, aambeeld, hooibaal). Ze
staan klaar; zet er een `objects`-regel bij en ze zijn in gebruik.

## Tekeningen

Alles wordt in tegels gemeten. Eén tegel is een canvas van **128 x 128**.

| Grootte     | viewBox        |
|-------------|----------------|
| 1x1         | `0 0 128 128`  |
| 2x1 (breed) | `0 0 256 128`  |
| 1x2 (hoog)  | `0 0 128 256`  |
| 3x1         | `0 0 384 128`  |

De tekening wordt passend geschaald (`object-fit: contain`), dus de verhouding
klopt altijd. Houd ongeveer 8px lucht aan elke rand. Een deel van de bank staat
nog op het oudere `0 0 64 64`; dat werkt, maar teken nieuwe op 128.

**Objecten van meerdere tegels** krijgen eerst een maatvariant en vallen daarna
terug op de gewone tekening: een tafel over twee tegels zoekt `table-2x1.svg`,
dan `table.svg`.

### art/characters/

Gezocht op volgorde: `<naam>.svg`, dan `<geslacht>.svg` (`male` / `female`), dan
`person.svg`. De tekening wordt bijgesneden op een cirkel (`object-fit: cover`),
dus teken op 128 x 128 met het onderwerp in het midden.

### art/backgrounds/

Vloertexturen heten `floor-<naam>.svg`, canvas 128 x 128, en worden **herhaald**
over de ruimte — de randen moeten dus naadloos aansluiten. De naam is de
ondergrond uit de builder in kleine letters met koppeltekens: vul je
`Moerassige bodem` in, dan zoekt de player `floor-moerassige-bodem.svg`.
Bestaat dat niet, dan blijft de tegel effen in de ruimtekleur.

### Submappen per thema

Elke map in `art/` mag een submap met een themanaam hebben. De player kijkt
eerst daarin en valt terug op de gedeelde map:

```text
art/objects/medieval/chair.svg   <- alleen middeleeuwse niveaus
art/objects/chair.svg            <- alle andere
```

Maak geen submappen per soort (`meubels/`, `planten/`) — daar wordt niet in
gekeken.

## Ruimtesoorten

`rooms` in het manifest is de lijst waaruit de builder kiest: 82 soorten,
gegroepeerd per wereld (Kasteel, Woning, Dorp, Markt, Klooster en kerk, Buiten,
Kamp en strijd, Onderweg). Elke soort heeft `id`, `label`, `article`, `group`,
`floor` en `themes`. Het `id` gaat de export in en moet stabiel blijven; het
`label` is wat de bouwer en de speler zien en mag je aanpassen.

De naam van een ruimte in een level stelt zich samen uit een **bepaling** en de
**soort**: "Oostelijk" + "Veld", "Anna's" + "Huis". Zo blijft de soort bewaard
voor de regelmotor ("was in een kapel") terwijl de ruimte toch zijn eigen naam
heeft. De vaste bepalingen staan in `roomQualifiers`; de namen van de personen
in het level komen daar in de builder automatisch bij. Een eigen naam intypen
kan nog steeds en wint dan van de samenstelling.

`floor` bepaalt de ondergrond en dus de textuur op het bord. Bruikbare waarden:
`wood`, `stone`, `tile`, `carpet`, `marble`, `concrete`, `dirt`, `grass`,
`gravel`, `sand`, `snow`, `water`, `metal`.

## Rollen

`roles` in het manifest bepaalt de standen die een persoon kan hebben, hun
Nederlandse naam, hun kleur en hun picto. Er zijn er zes; `available: false`
houdt een stand voorlopig uit de buildermenu's. Zet die vlag op `true` en de
stand doet meteen mee — er hoeft geen code aangepast te worden.
