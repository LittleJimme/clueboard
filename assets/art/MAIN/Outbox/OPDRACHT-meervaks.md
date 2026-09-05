# Renderopdracht — objecten over meer dan één vakje

Vervolg op de 1×1-lichting die er nu in zit. Zelfde stijl, zelfde licht, zelfde
manier van renderen — alleen het vak is groter.

## De rekenregel

Alles volgt uit één maat: **één bordvakje is 640 pixels.**

Het beeld is altijd het vak plus een halve marge eromheen, zoals bij de 1×1:

```
beeldbreedte = (vakken breed + 0,6) × 640
beeldhoogte  = (vakken diep  + 0,6) × 640
```

De **grondlijn** — waar het object de vloer raakt, de voorste rand van zijn
vak — ligt **altijd 144 pixels boven de onderrand** van het beeld. Het object
staat **altijd horizontaal gecentreerd** in het beeld.

Dat geeft:

| vak | beeld | grondlijn (y) | midden (x) |
|---|---|---|---|
| 1 × 1 | 1024 × 1024 | 880 | 512 |
| **2 × 1** (breed) | **1664 × 1024** | **880** | **832** |
| **1 × 2** (diep) | **1024 × 1664** | **1520** | **512** |

Links en rechts blijft er 192 pixels marge naast het vak staan, en boven het
vak 240 pixels — precies zoals bij de 1×1.

## De tafel

De 1×1-tafel die er nu in zit meet **443 breed × 340 hoog**, met zijn voet op
de grondlijn. Ik wil letterlijk diezelfde tafel, alleen langer: **dezelfde
pootdikte, dezelfde randdikte, dezelfde houtnerf, dezelfde hoek, dezelfde
kleur**. Alleen het blad wordt langer en er komt een extra pootpaar bij waar
dat logisch is. Niet opnieuw ontwerpen, niet opnieuw uitlichten.

| bestand | vak | tafel breed | tafel hoog | voet op | midden op |
|---|---|---|---|---|---|
| `table-2x1-…` | 2 × 1 | **1083** | 340 | y 880 | x 832 |
| `table-1x2-…` | 1 × 2 | 443 | **980** | y 1520 | x 512 |

Bij 2×1 groeit alleen de breedte met precies één vakje (443 + 640 = 1083); bij
1×2 alleen de diepte (340 + 640 = 980). De tafel **blijft binnen zijn vak** —
hij steekt er niet bovenuit.

## De watermolen

`watermill-2x1-…`, beeld **1664 × 1024**, grondlijn y 880, midden x 832.

De watermolen mag wél boven zijn vak uitsteken, zoals de boom dat doet. Ter
vergelijking: de boom is 603 breed × 758 hoog en zijn kruin komt tot y 123 —
ruim boven de bovenrand van het vak (y 240). Voor de watermolen: het rad en het
dak mogen tot ongeveer **y 60** komen. Blijf binnen de zijmarges (x 192 tot
1472), anders valt hij over het buurvakje heen.

## Bestanden

Zelfde map (`assets/art/MAIN/Outbox/`), zelfde opbouw als de 1×1, drie
bestanden per object:

```
<naam>-dag.png     het object bij dag, vrijstaand (met alpha)
<naam>-nacht.png   hetzelfde bij nacht, pixel op pixel dezelfde plek en maat
<naam>-shadow.png  het object mét zijn schaduw, plat op zuiver wit
```

Dus zes bestanden voor de tafel (`table-2x1-…` en `table-1x2-…`) en drie voor
de watermolen.

Twee dingen die eerder misgingen en het inlezen kostten:

- **Het schaduwvel moet op zuiver wit staan** (255,255,255), niet op crème en
  niet op zwart. Het script rekent de schaduw uit het verschil met het papier;
  bij een gekleurd vel komt het hele silhouet als schaduw mee.
- **De naam is kleine letters met koppeltekens**, precies zoals hierboven. Een
  hoofdletter of een spatie erin en het bestand wordt op de server niet
  gevonden, terwijl het op Windows wel lijkt te werken.
