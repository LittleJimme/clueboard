# ClueBoard

Deductiepuzzels op het bord. Elk level is een zaak.

ClueBoard bestaat uit drie losse, zelfstandige HTML-apps zonder buildstap,
framework of externe API. Je opent ze rechtstreeks in de browser.

## Structuur

```text
index.html          stuurt door naar het menu (voordeur van de site)
menu/               hoofdmenu: levellijst, upload, doorstap naar de builder
player/             de speler; player/Levels/ bevat de level-JSON's
builder/            level builder (desktop-only)
assets/             gedeelde assetbank, ingebakken door assets/tools/build_assets.py
```

## Levels

De levels staan als losse JSON-bestanden in `player/Levels/`. De speler en het
menu lezen eerst `player/Levels/index.json` — een lijst met bestandsnamen.

> **Belangrijk:** voeg een nieuw level altijd óók toe aan `index.json`. Op een
> webserver bestaat er geen map-listing om op terug te vallen, dus een level dat
> niet in `index.json` staat, verschijnt niet in de lijst.

## Een plaatsing delen (bugmelding)

In de speler staat onder **Instellingen → Plaatsing delen** de knop
*Exporteren*: het level plus wat er op het bord staat (pionnen, letters,
kruisjes en de klok) als één JSON-bestand, ook halverwege een zaak. Dat
bestand is gewoon een level met een extra blok `playerState`:

- *Inladen* in dezelfde instellingen (of uploaden via het menu) zet de stand
  terug, zodat je verder gaat waar de ander was.
- Importeren in de builder opent meteen **Controle van een plaatsing**: per
  persoon het vakje, per aanwijzing of hij klopt, de bordregels en het
  verschil met de oplossing, met dezelfde rekenaar als de oplossingenzoeker.

## Lokaal draaien

De apps lezen de levels met `fetch`, wat op `file://` geblokkeerd wordt. Start
daarom een servertje in de hoofdmap:

```
python -m http.server 8777
```

en open `http://127.0.0.1:8777/`.

## Publiceren

De site draait op GitHub Pages vanaf de `main`-branch, map `/` (root).
Wijzigingen zijn live zodra de push klaar is.
