# ClueBoard — Project Context

## Doel van dit document

Dit document bevat de productvisie, technische afspraken en ontwerpprincipes voor ClueBoard.

Lees dit samen met:

```text
builder/index.html
builder/CLAUDE.md
player/Levels/
```

De builder is een lokale, statische vanilla HTML/CSS/JavaScript-tool. Hij moet zonder server, framework, buildstap of externe API in een browser kunnen openen.

De opdracht aan een AI-developer is altijd:

> Werk voort op de bestaande builder, behoud wat werkt en lever één volledig werkend zelfstandig HTML-bestand terug.

Geen los prototype. Geen frameworkmigratie. Geen backend tenzij expliciet gevraagd.

---

# 1. Productvisie

ClueBoard is een visuele deductiepuzzel met een kaart, personen, ruimtes, objecten en verhalende aanwijzingen.

De speler moet afleiden:

- waar iedere persoon zich bevond;
- wie het slachtoffer is;
- wie de dader is;
- welke persoon bij welk object, gebied, rij of kolom hoort;
- hoe alle aanwijzingen tegelijk één consistente oplossing vormen.

ClueBoard combineert:

- logic-grid puzzels;
- ruimtelijke deductie;
- een kaart met kamers en gebieden;
- objecten die betekenis krijgen binnen een thema;
- verdachten met namen, rollen en uiterlijk;
- verhalende aanwijzingen;
- uiteindelijk een gepolijste 2D-game-ervaring.

De kern moet altijd eerlijk, controleerbaar en logisch blijven.

Een aanwijzing heeft twee lagen:

1. Technische, machineleesbare puzzellogica.
2. Verhalende zichtbare tekst voor de speler.

De vrije tekst mag nooit de enige plek zijn waar de echte logica bestaat.

---

# 2. Hoofdpipeline

De beoogde pipeline is:

```text
ClueBoard Builder
        ↓
Author-level JSON
        ↓
ClueBoard Player / Renderer
        ↓
Speler maakt hypotheses
        ↓
Speler dient oplossing in
```

De builder is de bron van waarheid.

De gameplayer leest JSON en mag geen level-specifieke data hardcoded bevatten.

Later kunnen meerdere renderers dezelfde JSON gebruiken:

```text
Builder JSON
   ├─ eenvoudige webplayer
   ├─ gepolijste 2D-webgame
   └─ mogelijk later Unity 2D
```

De puzzellogica en de leveldata moeten dus onafhankelijk blijven van de renderer.

---

# 3. Basisbegrippen

## Grid

- Het bord is een vierkant raster.
- Kolommen lopen van links naar rechts.
- Rijen lopen van boven naar beneden.
- Export gebruikt 1-based coördinaten.
- Tegel-ID heeft deze vorm:

```text
c{column}r{row}
```

Voorbeeld:

```text
c3r4
```

## Tegelstatus

Elke tegel heeft één status:

```text
neutral
occupiable
blocked
```

Betekenis:

| Status | Betekenis |
|---|---|
| `neutral` | Vrije vloer; een persoon mag hier staan |
| `occupiable` | Onderdeel van object waarop/in waarmee een persoon kan interacteren |
| `blocked` | Onderdeel van object waar niemand op mag staan |

## Ruimtes

- Een ruimte is een aaneengesloten groep tegels.
- Technische IDs zijn bijvoorbeeld:

```text
room-1
room-2
room-3
```

- Een ruimte kan later zichtbare naam, type en notitie krijgen.

Voorbeeld:

```json
{
  "id": "room-1",
  "name": "Bibliotheek",
  "kind": "library"
}
```

## Objecten

- Een object is een aaneengesloten groep tegels met dezelfde status.
- Technische IDs zijn bijvoorbeeld:

```text
obj-1
obj-10
obj-15
```

- Twee aangrenzende objecten zijn niet automatisch één object.
- Objecten worden alleen één object als de auteur ze expliciet koppelt.
- Objecten hebben later zichtbare naam, objectsoort, interacties en oriëntatie.

## Personen

- Personen hebben IDs:

```text
p1
p2
p3
```

- Personen worden op het bord geplaatst.
- Deze plaatsing is de verborgen eindoplossing.
- Dit zijn nadrukkelijk geen startposities voor de uiteindelijke speler.
- Eén persoon is slachtoffer.
- Eén persoon is dader.
- De rest zijn verdachten.

---

# 4. Basisregels van de puzzel

De huidige basisregels zijn meestal:

```text
één persoon per rij
één persoon per kolom
aantal personen = gridgrootte
geblokkeerde tegels blijven leeg
ruimtes zijn aaneengesloten
slachtoffer is niet de dader
```

Een persoon mag afhankelijk van het level:

- op vrije vloer staan;
- op een bezetbaar object staan/zitten;
- nooit op een geblokkeerd object staan.

De builder moet de verborgen oplossing hiertegen valideren.

Later moet een solver kunnen bewijzen dat alle aanwijzingen samen precies één oplossing overlaten. Dat is nog niet nodig voor de eerste versie.

---

# 5. Gewenste builderflow

De gewenste stappen zijn:

```text
1. Formaat
2. Ruimtes
3. Tegels
4. Objecten
5. Personen / verborgen oplossing
6. Namen & verhaal
7. Objectdetails / oriëntatie
8. Aanwijzingen
9. Validatie en export
```

## Stap 1 — Formaat

- Kies gridgrootte.
- Aantal personen volgt standaard uit gridgrootte.

## Stap 2 — Ruimtes

- Teken gebieden.
- Ruimtes moeten aaneengesloten blijven.

## Stap 3 — Tegels

- Zet tegelstatus:
  - neutral;
  - occupiable;
  - blocked.

## Stap 4 — Objecten

- Koppel tegels tot objecten.
- Alleen geldige footprints zijn toegestaan.

## Stap 5 — Personen

- Plaats alle personen op hun verborgen eindpositie.
- Kies slachtoffer en dader.
- Dit is de oplossing die later verborgen blijft voor spelers.

## Stap 6 — Namen & verhaal

- Klik op een persoon om naam, tags en omschrijving te geven.
- Klik op ruimte om naam, type en notitie te geven.
- Klik op object om naam, type, notitie en interactie te geven.

## Stap 7 — Objectdetails

- Kies objectcategorie.
- Kies objectsoort.
- Kies oriëntatie indien relevant.
- Bewaar interacties, capaciteit en toekomstige anchorinformatie.

## Stap 8 — Aanwijzingen

- Bouw machineleesbare clues.
- Voeg verhaaltekst toe.
- Valideer iedere clue tegen de verborgen oplossing.

---

# 6. Contentlaag

De abstracte puzzelstructuur staat los van zichtbare content.

## Personen

Voorbeeld:

```json
{
  "p1": {
    "name": "Archibald",
    "traits": [
      "butler",
      "man"
    ],
    "description": "De beheerste butler.",
    "presentation": {
      "pose": "auto",
      "facing": "auto",
      "interactionTargetId": null
    }
  }
}
```

### Persoondata

| Veld | Betekenis |
|---|---|
| `name` | Zichtbare naam |
| `traits` | Tags/eigenschappen |
| `description` | Korte karakteromschrijving |
| `pose` | Visuele houding |
| `facing` | Kijkrichting |
| `interactionTargetId` | Object/persoon waar character visueel mee verbonden is |

Voorbeelden van tags:

```text
vrouw
man
bandiet
heeft-taak
arts
butler
antiquair
verpleegkundige
schipper
```

Tags worden intern als array opgeslagen.

Matching is niet hoofdlettergevoelig.

## Ruimtes

Voorbeeld:

```json
{
  "room-1": {
    "name": "Bibliotheek",
    "kind": "library",
    "note": "Een donkere kamer met hoge boekenkasten."
  }
}
```

| Veld | Betekenis |
|---|---|
| `name` | Zichtbare ruimtenaam |
| `kind` | Technische ruimtetype |
| `note` | Interne auteur-notitie |

## Objecten

Voorbeeld:

```json
{
  "obj-10": {
    "label": "Fluwelen bank",
    "kind": "sofa",
    "note": "Oude groene bank naast de haard.",
    "orientation": "south",
    "interaction": [
      "sit"
    ],
    "capacity": 2,
    "visual": {
      "skin": "default",
      "anchors": []
    }
  }
}
```

| Veld | Betekenis |
|---|---|
| `label` | Zichtbare objectnaam |
| `kind` | Technische objectsoort |
| `note` | Auteur-notitie |
| `orientation` | Richting voor presentatie |
| `interaction` | Wat een persoon ermee kan doen |
| `capacity` | Maximum aantal personen |
| `skin` | Toekomstige thema-asset/variant |
| `anchors` | Toekomstige visuele interactiepunten |

---

# 7. Interactief contentbeheer

De kaart is de primaire interface.

In contentmodus bestaan drie submodi:

```text
[ Personen ] [ Ruimtes ] [ Objecten ]
```

## Personen

- Klik op pion selecteert persoon.
- Hover toont naam of fallback.
- Inspector toont naam, rol, tags, omschrijving, pose en kijkrichting.
- Naam verschijnt klein onder de pion.
- Bij ontbrekende naam toon fallback:

```text
P1
```

of:

```text
P1 · naam ontbreekt
```

## Ruimtes

- Klik op tegel selecteert volledige ruimte.
- Hover highlight volledige ruimte.
- Inspector toont ID, grootte, naam, type en notitie.
- Benoemde ruimte toont één subtiel label op het bord.
- Label staat bij voorkeur op een centrale vrije tegel.

## Objecten

- Klik op objecttegel selecteert het hele gekoppelde object.
- Hover highlight volledig object.
- Inspector toont:
  - ID;
  - status;
  - footprint;
  - label;
  - kind;
  - note;
  - orientation;
  - interaction;
  - capacity.

Content moet automatisch worden opgeslagen bij:

```text
input
blur
selectie-wissel
stap-wissel
export
```

---

# 8. Toegestane objectvormen

Ondersteun maximaal:

```text
single
line-2
line-3
corner-3
```

Betekenis:

| Footprint | Betekenis |
|---|---|
| `single` | Eén tegel |
| `line-2` | Twee aangrenzende rechte tegels |
| `line-3` | Drie aangrenzende rechte tegels |
| `corner-3` | Drie tegels in L-vorm |

Niet toegestaan:

```text
2x2
vier of meer tegels
niet-aaneengesloten vormen
kronkelige vormen
gemengde status in één object
```

De builder weet na het aanklikken al:

- status;
- footprint;
- grootte;
- locatie.

Vraag deze gegevens daarom niet opnieuw in de objectmenu’s.

---

# 9. Objectkeuze-flow

De objectkeuze moet snel zijn:

```text
Klik object
→ status + footprint zijn al bekend
→ kies functie / hoofdcategorie
→ kies concrete objectsoort
→ kies oriëntatie indien relevant
→ pas zichtbare naam aan
```

Niet:

```text
kies thema
→ kies kamer
→ kies meubel
→ kies subcategorie
→ kies object
```

Dat is te veel stappen.

## Bezetbare objecten

Bij `occupiable` kiest de auteur eerst een interactiefunctie:

```text
Zitten
Staan
Liggen
Ingaan
Gebruiken
Observeren
```

### Startcatalogus

| Functie | Single | Line-2 | Line-3 | Corner-3 |
|---|---|---|---|---|
| Zitten | stoel, paard | tweezitsbank, roeiboot | driezitsbank, limousine | hoekbank, dinerhoek |
| Staan | tapijt, modderplas | balkonstrook, loopplank | podium, brug | hoekpodium, L-vlonder |
| Liggen | eenpersoonsbed, hangmat | tweepersoonsbed, slaapbank | hemelbed, ziekenhuisbed | hoekligbank, L-slaapbank |
| Ingaan | kajak, telefooncel | auto, sloep | camper, grote tent | hoektent, hoekcabine |
| Gebruiken | piano, telescoop | bureau, werkbank | lange bar, keukenblok | hoekbureau, hoekkeuken |
| Observeren | raamnis, uitkijkpunt | balkon, wachtraam | uitkijkplatform, lang balkon | hoekbalkon, uitkijkhoek |

Voorbeelden:

```text
stoel → sit → capaciteit 1
paard → sit, ride → capaciteit 1
tweezitsbank → sit → capaciteit 2
roeiboot → enter, sit, row → capaciteit 2
piano → use → capaciteit 1
tapijt → stand → capaciteit 1
```

## Geblokkeerde objecten

Bij `blocked` kiest de auteur eerst een categorie:

```text
Opslag
Meubilair
Structuur
Natuur
Apparatuur
Decor
```

### Startcatalogus

| Categorie | Single | Line-2 | Line-3 | Corner-3 |
|---|---|---|---|---|
| Opslag | kist, ton | lage kast, boekenkast | lange boekenkast, voorraadrek | hoekkast, hoekboekenkast |
| Meubilair | bijzettafel, lamp | eettafel, bureau | lange eettafel, lange bar | hoekbureau, hoekkeuken |
| Structuur | pilaar, lantaarnpaal | hek, lage muur | lange muur, barricade | hoekmuur, hekhoek |
| Natuur | boom, rotsblok | boomstam, rotsformatie | rivierstrook, rotsrichel | rotswandhoek, waterhoek |
| Apparatuur | koelkast, generator | machine, controlepaneel | productielijn, serverrack | controlekamerhoek, machinekamerhoek |
| Decor | standbeeld, vaas | sarcofaag, vitrine | altaarwand, theaterdecor | altaarhoek, troonpodium |

---

# 10. Oriëntatie

Gebruik geen vrije rotatie. Gebruik vaste richtingen:

```text
auto
north
east
south
west
nw
ne
se
sw
```

## Richtingsregels

| Objecttype / footprint | Richting |
|---|---|
| Ronde of symmetrische objecten | `auto` |
| Stoel, piano, telescoop | north/east/south/west |
| Bank line-2/line-3 | vaak north/south |
| Boot, auto, limousine | vaak east/west |
| L-vormig object | nw/ne/se/sw |

Voorbeelden:

```text
Stoel → alle vier hoofdrichtingen
Tweezitsbank → north/south
Roeiboot → east/west
Hoekbank → nw/ne/se/sw
Ton → auto
Boom → auto
Tapijt → auto
```

Gebruik in de UI:

Voor rechte objecten:

```text
        [ ↑ ]
[ ← ]         [ → ]
        [ ↓ ]
```

Voor L-vormen:

```text
[ ┌ ] [ ┐ ]

[ └ ] [ ┘ ]
```

Een knop:

```text
[ ↻ Draaien ]
```

gaat steeds door alleen de geldige richtingen.

---

# 11. Toekomstige 2D-renderer

De builder hoeft nog geen echte sprites of animaties te maken.

Maar de data moet later geschikt zijn voor een gepolijste 2D-game.

Gebruik een modulair systeem:

```text
objectsoort
+ objectskin
+ objectstate
+ objectoriëntatie
+ interaction anchor
+ personagepose
+ kijkrichting
= visuele scène
```

Niet:

```text
aparte afbeelding voor iedere combinatie van persoon en object
```

Voorbeeld anchor:

```json
{
  "id": "seat-left",
  "type": "sit",
  "x": 0.25,
  "y": 0.62,
  "pose": "sitting",
  "facing": "south"
}
```

Voorbeelden:

| Object | Interactie | Pose |
|---|---|---|
| Stoel | sit | sitting |
| Bank | sit | sitting |
| Paard | ride | riding |
| Auto | drive | driving |
| Roeiboot | row | rowing |
| Bed | lie | lying |
| Piano | use | using-piano |
| Bureau | use | using-desk |
| Telescoop | observe | looking-through |
| Balkon | observe | looking-out |
| Tapijt | stand | standing |

Oriëntatie en pose zijn voorlopig presentatiegegevens, geen puzzelregels.

---

# 12. Clues

Iedere clue heeft technische logica en zichtbare presentatie.

Voorbeeld:

```json
{
  "id": "clue-01",
  "category": "object-relation",
  "logic": {
    "type": "person-adjacent-to-object",
    "personId": "p2",
    "objectId": "obj-8",
    "adjacency": "orthogonal"
  },
  "presentation": {
    "defaultText": "Cora bevond zich naast de oude kist.",
    "storyText": "Cora hoorde een zacht gerammel naast de oude kist."
  }
}
```

De code gebruikt alleen:

```text
logic
```

De speler ziet:

```js
storyText || defaultText
```

## Semantische definities

| Term | Technische betekenis |
|---|---|
| Naast | Orthogonaal aangrenzend, dus boven/onder/links/rechts |
| Op object | Personentegel is onderdeel van object |
| In gebied | Personentegel heeft dezelfde roomId |
| Alleen | Enige persoon in relevante scope |
| Alleen met | Exact twee personen in scope |
| Ten oosten van | Hogere kolom, niet noodzakelijk zelfde rij |
| Direct rechts van | Zelfde rij, exact één kolom meer |
| Ten noorden van | Lagere rijwaarde |
| Manhattan-afstand | `abs(x1-x2) + abs(y1-y2)` |
| Noordelijkste | Uniek laagste rijwaarde |
| Oostelijkste | Uniek hoogste kolomwaarde |

---

# 13. Clue-builder UX

Er zijn twee modes:

```text
[ Bordgestuurd ] [ Formulier ]
```

## Bordgestuurd

Dit is de primaire flow:

```text
Klik persoon
→ clue-bubble opent
→ kies categorie
→ kies concrete geldige regel
→ selecteer eventueel target op bord
→ conceptclue verschijnt
→ schrijf storytekst
→ clue toevoegen
```

Voorbeeld personagebubble:

```text
Archibald — nieuwe aanwijzing

[ Locatie ]
[ Bord ]
[ Gebied ]
[ Object ]
[ Richting ]
[ Persoon ]
[ Aantallen ]
[ Extremes ]
[ Tags & rollen ]
```

Toon alleen categorieën waarin voor de geselecteerde persoon minstens één ware concrete clue bestaat.

## Targetselectie

Voorbeeld:

```text
Archibald → ten oosten van persoon
```

De builder toont:

```text
Selecteer de persoon waar Archibald ten oosten van staat.
```

Gedrag:

- hoofdfiguur blijft gemarkeerd;
- geldige targets worden gehighlight;
- ongeldige targets worden gedimd;
- Escape annuleert;
- Annuleren-knop annuleert;
- klik op persoon/object/ruimte vult technische ID in;
- conceptclue verschijnt daarna.

## Conceptclue

```text
Nieuwe aanwijzing

Technische betekenis
Archibald staat orthogonaal naast de Oude kist.

Standaardtekst
Archibald bevond zich naast de oude kist.

Storytelling voor de speler
[ De butler zag Archibald nerveus naast de oude kist staan. ]

Validatie
✓ Waar in de verborgen oplossing.

[ Aanwijzing toevoegen ]
[ Annuleren ]
```

---

# 14. Cluefamilies

De clue-engine moet centraal uitbreidbaar zijn.

Gebruik per clue-type minimaal:

```text
type
category
parameters
targetType
availability
validation
defaultText
helpText
```

## Absolute locatie

- persoon in rij;
- persoon in kolom;
- persoon op tegel;
- persoon niet in rij;
- persoon niet in kolom;
- persoon niet op tegel;
- persoon in eerste/laatste rij;
- persoon in eerste/laatste kolom;
- persoon in bovenste/onderste helft;
- persoon in linker/rechterhelft;
- persoon in kwadrant;
- persoon in één van meerdere rijen/kolommen.

## Bordgeometrie

- persoon op buitenrand;
- persoon niet op buitenrand;
- persoon in bordhoek;
- persoon niet in bordhoek;
- persoon op noord/zuid/oost/westrand.

## Ruimtes

- persoon in gebied;
- persoon niet in gebied;
- persoon in één van meerdere gebieden;
- persoon in hetzelfde/niet hetzelfde gebied als persoon;
- persoon in hetzelfde gebied als slachtoffer/dader;
- persoon in grootste/kleinste gebied;
- persoon in gebied met specifieke grootte;
- persoon in gebied met/zonder object;
- persoon in gebied met/zonder objectsoort;
- persoon in gebied met/zonder tag.

## Gebiedsgeometrie

- persoon in hoek van gebied;
- persoon niet in hoek;
- persoon op rand van gebied;
- persoon niet op rand;
- persoon aan noord/zuid/oost/westzijde;
- persoon noordelijkst/zuidelijkst/oostelijkst/westelijkst in gebied;
- persoon in centrum van gebied.

## Objectpositie

- persoon op/niet op object;
- persoon op/niet op objectsoort;
- persoon op bezetbaar object;
- persoon op vrije vloer;
- object bezet/leeg;
- exact/minimaal/maximaal aantal personen op object;
- enige persoon op object;
- enige persoon op objectsoort;
- object bevat slachtoffer/dader.

## Objectrelaties

- persoon naast/niet naast object;
- persoon naast/niet naast objectsoort;
- persoon boven/onder/links/rechts van object;
- persoon direct boven/onder/links/rechts van object;
- persoon in hetzelfde/niet hetzelfde gebied als object;
- persoon dichtst bij/verst van object;
- persoon dichter bij object A dan B;
- persoon tussen twee objecten;
- persoon naast twee objecten.

## Persoonrelaties

- persoon naast/niet naast persoon;
- persoon op dezelfde/niet dezelfde rij;
- persoon in dezelfde/niet dezelfde kolom;
- persoon in hetzelfde/niet hetzelfde gebied;
- persoon op hetzelfde/niet hetzelfde object;
- persoon oost/west/noord/zuid van persoon;
- persoon direct rechts/links/boven/onder;
- persoon op afstand exact/minimaal/maximaal N;
- persoon dichtst bij/verst van persoon;
- persoon dichter bij persoon A dan B;
- persoon tussen twee personen.

## Aantallen en exclusiviteit

- persoon alleen/niet alleen in gebied;
- persoon alleen op object/objectsoort;
- persoon alleen met persoon;
- persoon alleen met slachtoffer/dader;
- slachtoffer alleen met dader;
- exact/minimaal/maximaal personen in gebied;
- exact/minimaal/maximaal personen op object;
- aantallen personen met tag;
- iedereen/niemand heeft tag;
- enige persoon met tag.

## Extremes

- noordelijkste persoon;
- zuidelijkste persoon;
- meest westelijke persoon;
- meest oostelijke persoon;
- extremes binnen gebied;
- extremes binnen taggroep;
- dichtst/verst bij object;
- dichtst/verst bij persoon;
- grootste/kleinste gebied;
- grootste/kleinste object;
- dichtst/verst van bordcentrum.

## Rollen en tags

- persoon heeft/heeft niet tag;
- persoon in gebied met/niet met tag;
- persoon naast/niet naast tag;
- persoon alleen met tag;
- aantal personen met tag;
- persoon met/niet met slachtoffer;
- persoon met/niet met dader;
- slachtoffer en dader delen gebied;
- slachtoffer en dader staan naast elkaar;
- slachtoffer is alleen met dader.

---

# 15. Contextuele clue-filtering

De standaard clue-builder toont alleen regels die:

1. technisch ondersteund zijn;
2. concrete entiteiten hebben;
3. waar zijn volgens verborgen oplossing;
4. betekenisvol zijn;
5. uniek zijn wanneer dat nodig is.

Voorbeelden:

- Geen persoon op object:
  - toon geen “persoon op object”-clues.
- Geen uniek grootste gebied:
  - toon geen “in grootste gebied”.
- Twee personen even noordelijk:
  - toon geen “de noordelijkste persoon”.
- Persoon staat niet naast object:
  - toon die positieve naast-clue niet.
- Geen object met naam:
  - waarschuw om objecten eerst te benoemen.

Toggle:

```text
[✓] Toon alleen geldige mogelijkheden
```

Standaard staat deze aan.

Als uit:

- toon ook andere opties;
- valideer live rood/groen;
- blokkeer onware clues in normale modus.

---

# 16. Validatie

## Bordvalidatie

- Alle personen geplaatst.
- Eén persoon per rij wanneer actief.
- Eén persoon per kolom wanneer actief.
- Niemand op blocked tegel.
- Slachtoffer bestaat.
- Dader bestaat.
- Slachtoffer en dader verschillen.
- Objectvormen zijn geldig.

## Contentvalidatie

Waarschuw bij:

- persoon zonder naam;
- ruimte zonder naam;
- object zonder label;
- object zonder kind;
- ontbrekende oriëntatie waar vereist.

## Cluevalidatie

- Clue-type bestaat.
- Referenced IDs bestaan.
- Clue is waar volgens verborgen oplossing.
- Standaardtekst of storytekst bestaat.
- Ongeldige clue wordt rood gemarkeerd.
- Ongeldige clue mag niet ongemerkt als volledig level exporteren.

Nog niet nodig:

- Solver die unieke oplossing bewijst.
- Automatische puzzelgeneratie.
- Echte sprites.
- Echte animaties.
- Unity.
- Backend.
- Multiplayer.

---

# 17. Prioriteit

Bouw niet alles tegelijk.

Volg deze volgorde:

```text
1. Bestaande builder niet breken.
2. Automatisch content opslaan.
3. Personen, ruimtes en objecten interactief benoemen.
4. Namen onder personen en labels voor ruimtes.
5. Objectcatalogus, footprintvalidatie en oriëntatie.
6. Board-driven clue-flow.
7. Targetselectie.
8. Centrale clue-registry.
9. Meer clue-types.
10. Import/export en validatie.
11. Later pas player, sprites, animaties en thema’s.
```

---

# 18. Definitie van succes

Deze flow moet uiteindelijk volledig werken:

```text
1. Bouw een bord.
2. Teken ruimtes.
3. Maak en koppel objecten.
4. Plaats verborgen oplossing.
5. Klik op personen, ruimtes en objecten om ze te benoemen.
6. Kies objecttype, interactie en richting.
7. Klik op persoon om contextuele, ware clue-opties te zien.
8. Klik eventueel op tweede persoon, object of ruimte.
9. Schrijf storytellingtekst.
10. Exporteer JSON.
11. Importeer hetzelfde JSON-bestand opnieuw.
12. Alle data blijft behouden.
```

De builder is geslaagd wanneer hij een betrouwbare authoring-pipeline vormt:

```text
Builder → compleet JSON-level → generieke player
```