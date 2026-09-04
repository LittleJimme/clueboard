# Renderopdracht — ClueBoard objecten 1×1, versie 2

Render alle objecten van één vakje opnieuw, in hogere resolutie, elk als een
losstaand plaatje. Twee bestanden per object: een dagversie en een nachtversie.

## Waar de bestanden komen

Map: `assets/art/production/objects-1x1-v2/`

Twee bestanden per object, met precies deze namen (kleine letters, koppelteken,
geen spaties — de spelling is eerder een keer verschoven van `Boom_Donker` naar
`Boom_donker` en dat brak het inleesscript op een hoofdlettergevoelig systeem):

```
<slug>-dag.png
<slug>-nacht.png
```

Bijvoorbeeld `chair-dag.png` en `chair-nacht.png`.

## Formaat

- **Altijd vierkant: 1024 × 1024 pixels**, PNG.
- **Witte achtergrond** (`#FFFFFF`), niet transparant.
- Het object staat er **met zijn slagschaduw** op. De schaduw hoort bij het
  object en valt naar **rechtsonder**; het licht komt uit linksboven.
- De schaduw mag onder de grondlijn en tot buiten de objectbox doorlopen, maar
  moet binnen het beeld blijven.
- Geen kader, geen grondvlak, geen tegel, geen tekst, geen bijschrift. Eén
  object per bestand, verder alleen wit en de schaduw.

## De maatvoering — dit is het belangrijkste

Alle objecten worden op het bord op precies hetzelfde vierkant getekend. Daarom
moet elk plaatje dezelfde ijkpunten aanhouden:

| ijkpunt | plek in het beeld |
|---|---|
| **Grondlijn** (waar het object de vloer raakt) | **y = 880** |
| **Middenlijn** (waar het object op staat) | **x = 512** |
| Eén bordvakje komt overeen met | **640 px** |

**De onderkant van elk object staat op y = 880. Altijd. Bij elk object, in
beide standen.** Een stoel, een vat, een boom en een standbeeld raken allemaal
exact dezelfde lijn. Onder die lijn is alleen nog ruimte voor de schaduw.

## Twee hoogteklassen

Er zijn twee soorten objecten, en het **verschil in maat moet uit de tekening
komen** — niet uit schalen achteraf.

### 1. Normaal — staat in zijn vakje

Meubels en dingen waar iemand op of naast kan staan. Ze blijven binnen hun
vakje.

- Maximaal **440 px breed × 460 px hoog** (0,69 × 0,72 vakje)
- Box: x van 292 tot 732, y van 420 tot 880

### 2. Hoog, niet beloopbaar — steekt boven zijn vakje uit

Dingen die op het bord over de muur van hun ruimte heen mogen vallen.

- Maximaal **600 px breed × 840 px hoog** (0,94 × 1,31 vakje)
- Box: x van 212 tot 812, y van 40 tot 880

Een hoog object is dus ongeveer **1,8× zo hoog** als een normaal object. Vul de
box niet blindelings: een boom mag hem echt volmaken, een struik hoort een stuk
kleiner te blijven. Wat telt is dat de onderlinge verhouding klopt — een boom
naast een stoel op hetzelfde bord moet er geloofwaardig uitzien.

## Dag en nacht

De nachtversie is **exact hetzelfde object op exact dezelfde plek in het beeld**
— zelfde stand, zelfde formaat, zelfde silhouet, pixel op pixel. Alleen het
licht verandert: koeler, gedempter, donkerder, alsof het avond is. De schaduw
blijft dezelfde vorm en dezelfde plek als bij de dagversie.

## De objecten

Deze 26. Alles is één vakje.

### Hoog, niet beloopbaar (4)

| slug | Nederlands |
|---|---|
| `tree` | Boom |
| `statue` | Standbeeld |
| `shrub` | Struik |
| `plant` | Plant |

### Normaal (22)

| slug | Nederlands | | slug | Nederlands |
|---|---|---|---|---|
| `chair` | Stoel | | `sack` | Zak |
| `table` | Tafel | | `shelf` | Boekenkast |
| `crate` | Krat | | `barrel` | Vat |
| `box` | Doos | | `vase` | Vaas |
| `treasure` | Schat | | `loom` | Weefgetouw |
| `weapon-chest` | Wapenkist | | `easel` | Schildersezel |
| `weapon-rack` | Wapenrek | | `house` | Huisje |
| `stones` | Stenen | | `rubble` | Puin |
| `puddle` | Modderplas | | `horse` | Paard |
| `cow` | Koe | | `pig` | Varken |
| `boar` | Everzwijn | | `wolf` | Wolf |

De dieren staan van opzij en kijken naar rechts.

## Stijl

Dezelfde stijl als de bestaande objecten in `assets/art/objects/`: gestileerd,
zacht geboetseerd, warme aardse kleuren, licht van linksboven, geen harde
omlijning, geen cel-shading. Van bovenaf gezien onder een lichte hoek, zoals de
rest van het bord.
