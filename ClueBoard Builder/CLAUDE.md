# ClueBoard — vaste instructies voor Claude Code

## Project

ClueBoard is een statische vanilla HTML/CSS/JavaScript level builder
voor een visuele deductiepuzzel op een grid.

De actuele builder is altijd:

```text
clueboard-builder.html
```

Werk altijd voort op dit bestand.

## Belangrijke bestanden

```text
clueboard-builder.html      actuele builder
PROJECT_CONTEXT.md          uitgebreide product- en techniekcontext
levels/                     geëxporteerde JSON-levels
backups/                    veilige kopieën vóór grote wijzigingen
../assets/                  gedeelde assetbank van builder én player
../assets/manifest.json     bron van waarheid voor objecten, iconen en rollen
```

## Assetbank

Iconen, tekeningen en objectkennis staan in `../assets/`, niet in de builder.
De builder en de player lezen allebei uit dezelfde bank.

- Voeg **nooit** een objectsoort, icoon of rolnaam rechtstreeks in de HTML toe.
  Pas `assets/manifest.json` aan en draai `python assets/tools/build_assets.py`.
- Dat script schrijft de bank tussen de markers `/* @clueboard:assets-begin */`
  en `/* @clueboard:assets-end */` in beide bestanden. Bewerk dat blok niet met
  de hand; het wordt bij de volgende build overschreven.
- Alles buiten die markers blijft van jou, inclusief het `AssetBank`-object
  eronder. Dat staat met opzet in beide bestanden identiek.
- Gebruik geen emoji als pictogram. Wat je nodig hebt komt uit de bank.
- Zie `assets/README.md` voor het toevoegen van een soort of een tekening.

Lees voor grote wijzigingen altijd eerst:

```text
PROJECT_CONTEXT.md
```

## Harde technische regels

- Gebruik alleen vanilla HTML, CSS en JavaScript.
- Gebruik geen React, Vue, npm, bundler, backend, database of externe API.
- De builder moet één zelfstandig lokaal HTML-bestand blijven.
- Vervang de bestaande builder nooit door een los nieuw prototype.
- Behoud bestaande werkende functies tenzij expliciet anders gevraagd.
- Breek import/export niet.
- Gebruik geen externe afhankelijkheden die lokaal internet vereisen.
- Houd bestaande styling en UX zoveel mogelijk intact.
- Voeg nieuwe functies gericht toe, zonder onnodige grote refactors.

## Bron van waarheid

- De builder is de bron van waarheid voor levels.
- De builder exporteert JSON.
- Een toekomstige player of renderer leest alleen JSON.
- Geen level-specifieke data hardcoden in een toekomstige player.

## Puzzelregels

- Geplaatste personen zijn de verborgen eindoplossing.
- Geplaatste personen zijn geen zichtbare startposities voor spelers.
- Technische IDs blijven stabiel:
  - personen: `p1`, `p2`, enzovoort;
  - ruimtes: `room-1`, `room-2`, enzovoort;
  - objecten: `obj-1`, `obj-2`, enzovoort.
- Storytellingtekst mag nooit de enige bron van puzzellogica zijn.
- Elke clue moet machineleesbare `logic` bevatten.
- Elke clue mag een vrije zichtbare `storyText` bevatten.

## Objectregels

- Objectstatus is altijd:
  - `occupiable`
  - `blocked`
- Objecten mogen alleen deze footprints hebben:
  - `single`
  - `line-2`
  - `line-3`
  - `corner-3`
- Een object moet aaneengesloten zijn.
- Een object mag geen gemengde tegelstatus bevatten.
- Klik op één tegel van een object selecteert altijd het volledige gekoppelde object.
- Vraag vorm en status niet opnieuw als object al gekoppeld is.

## Veiligheid en UX

- Rechtermuisklik op een pion in de Personen-stap opent een radiaal menu (Dader, Slachtoffer, Verwijderen); buiten die stap wijzigt rechtermuisklik nooit een persoon of de oplossing.
- De prominente knop `Pionnen wissen` mag niet bestaan.
- Personen verwijderen kan alleen expliciet in de plaatsingsstap, met bevestiging.
- In contentmodus en cluemodus mogen bordklikken nooit de verborgen oplossing wijzigen.
- Namen en content moeten automatisch opslaan:
  - tijdens invoer;
  - bij blur;
  - bij selectie-wissel;
  - bij stap-wissel;
  - vóór export.
- Personen met naam tonen een klein label onder hun pion.
- Benoemde ruimtes tonen een subtiel label op het bord.

## Werkwijze

1. Analyseer bestaande code vóór je grote wijzigingen maakt.
2. Werk per kleine, afgebakende feature.
3. Maak vóór grotere wijzigingen een backup in `backups/`.
4. Test na wijzigingen de builder lokaal.
5. Test import én export met een JSON-bestand uit `levels/`.
6. Geef na iedere wijziging kort weer:
   - wat is aangepast;
   - welke bestanden zijn gewijzigd;
   - hoe is getest;
   - bekende beperkingen.

## Prioriteit

1. Bestaande builder niet breken.
2. Betrouwbare automatische opslag.
3. Interactief benoemen op het bord.
4. Personage- en ruimtelabels.
5. Objectcatalogus, footprints en oriëntatie.
6. Board-driven clue-flow.
7. Centrale clue-registry.
8. Uitbreiding van clue-types.
9. Import/export en validatie.
10. Later pas: player, sprites, animaties, thema-assets en Unity.