# ClueBoard

ClueBoard is een visuele deductiepuzzel.

## Belangrijkste bestanden

- `index.html` — actuele level builder
- `../player/Levels/` — geëxporteerde JSON-levels
- `CLAUDE.md` — vaste instructies voor Claude Code
- `PROJECT_CONTEXT.md` — uitgebreide productcontext
- `backups/` — veilige kopieën van oudere builderversies

## Werkwijze

1. Maak altijd eerst een backup.
2. Laat Claude Code één kleine feature tegelijk aanpassen.
3. Test de builder lokaal in de browser.
4. Exporteer een JSON-level.
5. Importeer datzelfde level opnieuw.
6. Pas daarna de volgende feature toe.