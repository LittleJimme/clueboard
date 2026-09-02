# Levels

Elk bestand hier is één niveau: de JSON die je in ClueBoard Builder exporteert.
Ze verschijnen op het beginscherm van de player, onder het ingebouwde
demo-niveau, in alfabetische volgorde op bestandsnaam.

## Een niveau toevoegen

1. Exporteer het niveau in de builder.
2. Zet het `.json`-bestand in deze map.
3. Ververs de player.

Klopt een bestand niet (geen geldige JSON, of geen geldig niveau), dan wordt het
stilletjes overgeslagen en meldt de player onder de lijst hoeveel bestanden er
zijn overgeslagen. De rest blijft gewoon werken.

## index.json

De player zoekt op twee manieren:

1. **`index.json`** — een simpele lijst met bestandsnamen.
2. **De mapinhoud** die de webserver toont.

Draai je lokaal (`python -m http.server`), dan werkt manier 2 vanzelf en hoef je
`index.json` **niet** bij te werken. Op **GitHub Pages** werkt manier 2 niet —
die toont geen mapinhoud. Zet je niveau daar dus ook in `index.json`:

```json
[
  "een_hinderlaag_vol_struikrovers.json",
  "herberg_de_doortocht.json",
  "mijn_nieuwe_niveau.json"
]
```

Volgorde in `index.json` maakt niet uit; de lijst wordt altijd alfabetisch
gesorteerd.

## Lokaal draaien

De player leest deze map met `fetch`. Dat werkt niet als je `index.html` met
dubbelklik opent (`file://`) — je ziet dan alleen het demo-niveau plus de knop
**Niveau laden**. Start in de map `ClueBoard Player`:

```
python -m http.server 8777
```

en open `http://127.0.0.1:8777/Build/index.html`.
