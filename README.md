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
