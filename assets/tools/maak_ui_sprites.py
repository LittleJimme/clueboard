# -*- coding: utf-8 -*-
"""Tekent de UI-sprites van de middeleeuwse skin als SVG in
   assets/art/ui/medieval/. Dit zijn invalbeelden in de stijl van de
   bordobjecten; gerenderde PNG's uit assets/render/inbox/ vervangen ze
   per stuk door alleen de url in het spritesblok van de CSS om te zetten."""
import io, os

MAP = r"C:\Users\Gebruiker\Documents\ClueBoard\assets\art\ui\medieval"
os.makedirs(MAP, exist_ok=True)

INK = "#2A1B0C"

def schrijf(naam, inhoud):
    p = os.path.join(MAP, naam)
    tmp = p + ".tmp"
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(inhoud)
    os.replace(tmp, p)
    print("  ", naam)

# ── Titelbord: houten bord met gouden bies en kroonembleem ──────────
schrijf("titelbord.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 300">
<defs>
<linearGradient id="rail" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#5E4020"/><stop offset=".5" stop-color="#4E3419"/><stop offset="1" stop-color="#3A2712"/>
</linearGradient>
<linearGradient id="plank" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#94693A"/><stop offset=".55" stop-color="#8A6134"/><stop offset="1" stop-color="#7A552C"/>
</linearGradient>
<linearGradient id="veld" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#3D5E92"/><stop offset="1" stop-color="#1F3557"/>
</linearGradient>
</defs>
<ellipse cx="320" cy="272" rx="286" ry="16" fill="rgba(20,12,4,.35)"/>
<rect x="18" y="52" width="604" height="216" rx="20" fill="url(#rail)" stroke="{INK}" stroke-width="6"/>
<rect x="30" y="64" width="580" height="192" rx="13" fill="none" stroke="#C9A227" stroke-width="3" opacity=".9"/>
<rect x="42" y="76" width="556" height="168" rx="9" fill="url(#plank)" stroke="{INK}" stroke-width="4"/>
<path d="M52 96h536M52 128h536M52 192h536M52 224h536" stroke="#6E4B26" stroke-width="2.5" opacity=".55"/>
<path d="M52 84h536" stroke="#B98A50" stroke-width="3" opacity=".6"/>
<path d="M120 108c40-3 90-3 120 0M420 206c50 4 100 3 150-2" stroke="#5E4020" stroke-width="2" opacity=".4" fill="none"/>
<g>
<circle cx="52" cy="160" r="9" fill="#4A505C" stroke="{INK}" stroke-width="3.5"/>
<circle cx="49" cy="157" r="3" fill="#AEB6C2"/>
<circle cx="588" cy="160" r="9" fill="#4A505C" stroke="{INK}" stroke-width="3.5"/>
<circle cx="585" cy="157" r="3" fill="#AEB6C2"/>
</g>
<g>
<path d="M320 14c14 0 24 4 30 7v26c0 16-13 28-30 33c-17-5-30-17-30-33V21c6-3 16-7 30-7Z"
  fill="url(#veld)" stroke="{INK}" stroke-width="5"/>
<path d="M320 14c14 0 24 4 30 7v26c0 16-13 28-30 33c-17-5-30-17-30-33V21c6-3 16-7 30-7Z"
  fill="none" stroke="#C9A227" stroke-width="2.5" transform="translate(0,0)" opacity=".9"/>
<path d="M303 52v-14l7 6 10-11 10 11 7-6v14c0 3-3 5-6 5h-22c-3 0-6-2-6-5Z" fill="#C9A227" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
<path d="M310 30c4 5 6 8 4 14" stroke="rgba(255,255,255,.4)" stroke-width="3" fill="none" stroke-linecap="round"/>
</g>
</svg>
''')

# ── Controleer-schild: blauw schild met gouden rand en kroon ────────
schrijf("schild-controleer.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 240">
<defs>
<linearGradient id="blauw" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#41639B"/><stop offset=".55" stop-color="#2E4A78"/><stop offset="1" stop-color="#1F3557"/>
</linearGradient>
<linearGradient id="goudrand" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#E4C25C"/><stop offset=".5" stop-color="#C9A227"/><stop offset="1" stop-color="#8F7115"/>
</linearGradient>
</defs>
<ellipse cx="100" cy="226" rx="74" ry="10" fill="rgba(20,12,4,.4)"/>
<path d="M100 34c26 0 44 7 55 13v66c0 39-24 66-55 77c-31-11-55-38-55-77V47c11-6 29-13 55-13Z"
  fill="url(#goudrand)" stroke="{INK}" stroke-width="6"/>
<path d="M100 48c21 0 36 5 44 10v54c0 32-19 54-44 63c-25-9-44-31-44-63V58c8-5 23-10 44-10Z"
  fill="url(#blauw)" stroke="{INK}" stroke-width="4"/>
<path d="M64 62c10-6 22-9 36-9c6 0 12 1 17 2c-20 2-36 9-45 18c-5 5-8 10-9 15V62Z" fill="rgba(255,255,255,.16)"/>
<g fill="#F0D77A" stroke="{INK}" stroke-width="2">
<circle cx="100" cy="42" r="3.4"/><circle cx="64" cy="52" r="3.4"/><circle cx="136" cy="52" r="3.4"/>
<circle cx="52" cy="88" r="3.4"/><circle cx="148" cy="88" r="3.4"/>
<circle cx="60" cy="140" r="3.4"/><circle cx="140" cy="140" r="3.4"/>
<circle cx="100" cy="182" r="3.4"/>
</g>
<g>
<path d="M68 26v-16l11 8 13-14 8 9 8-9 13 14 11-8v16c0 4-4 7-8 7H76c-4 0-8-3-8-7Z"
  fill="url(#goudrand)" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>
<circle cx="79" cy="8" r="3.6" fill="#E4C25C" stroke="{INK}" stroke-width="2.5"/>
<circle cx="100" cy="2.8" r="3.6" fill="#E4C25C" stroke="{INK}" stroke-width="2.5"/>
<circle cx="121" cy="8" r="3.6" fill="#E4C25C" stroke="{INK}" stroke-width="2.5"/>
<path d="M74 20c8 3 44 3 52 0" stroke="rgba(255,255,255,.45)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
</g>
</svg>
''')

# ── Klein donker houten schildje voor iconknoppen ───────────────────
schrijf("knop-schildje.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 124">
<defs>
<linearGradient id="walnoot" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#6A4A28"/><stop offset=".5" stop-color="#523719"/><stop offset="1" stop-color="#3A2712"/>
</linearGradient>
</defs>
<ellipse cx="60" cy="114" rx="42" ry="7" fill="rgba(20,12,4,.4)"/>
<path d="M60 8c17 0 29 4 36 8v40c0 25-16 43-36 50c-20-7-36-25-36-50V16c7-4 19-8 36-8Z"
  fill="url(#walnoot)" stroke="{INK}" stroke-width="5"/>
<path d="M60 15c14 0 25 3 30 6v36c0 21-13 37-30 43c-17-6-30-22-30-43V21c5-3 16-6 30-6Z"
  fill="none" stroke="#7E5A32" stroke-width="2.5" opacity=".8"/>
<path d="M34 22c8-4 16-6 26-6c4 0 9 0 13 1c-16 3-28 9-34 16V22Z" fill="rgba(255,255,255,.10)"/>
<g fill="#8E96A5" stroke="{INK}" stroke-width="2">
<circle cx="60" cy="14" r="3"/><circle cx="30" cy="26" r="3"/><circle cx="90" cy="26" r="3"/>
<circle cx="60" cy="99" r="3"/>
</g>
</svg>
''')

# ── Houten tabblad en zijn perkamenten (actieve) broer ──────────────
schrijf("tab-hout.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 76">
<defs>
<linearGradient id="tabhout" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#7A5228"/><stop offset=".6" stop-color="#5E4020"/><stop offset="1" stop-color="#462F16"/>
</linearGradient>
</defs>
<path d="M14 70V26c0-9 7-16 16-16h180c9 0 16 7 16 16v44Z" fill="url(#tabhout)" stroke="{INK}" stroke-width="5"/>
<path d="M22 68V28c0-6 4-10 10-10h176c6 0 10 4 10 10v40" fill="none" stroke="#8A6134" stroke-width="2.5" opacity=".7"/>
<path d="M30 26h180" stroke="rgba(255,255,255,.14)" stroke-width="3" stroke-linecap="round"/>
</svg>
''')
schrijf("tab-perkament.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 76">
<defs>
<linearGradient id="tabperk" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#F9F0DA"/><stop offset=".6" stop-color="#F3E7CC"/><stop offset="1" stop-color="#E4D3AC"/>
</linearGradient>
</defs>
<path d="M14 70V26c0-9 7-16 16-16h180c9 0 16 7 16 16v44Z" fill="url(#tabperk)" stroke="{INK}" stroke-width="5"/>
<path d="M22 68V28c0-6 4-10 10-10h176c6 0 10 4 10 10v40" fill="none" stroke="#C9AE7E" stroke-width="2.5" opacity=".9"/>
<path d="M30 24h180" stroke="rgba(255,255,255,.6)" stroke-width="3" stroke-linecap="round"/>
</svg>
''')

# ── Timer: perkamentrolletje met opgerolde uiteinden ────────────────
schrijf("timer-rol.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 100">
<defs>
<linearGradient id="rolvel" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#F9F0DA"/><stop offset=".55" stop-color="#F3E7CC"/><stop offset="1" stop-color="#E2D0A6"/>
</linearGradient>
<linearGradient id="rolcyl" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#CBB98E"/><stop offset=".45" stop-color="#F1E5C6"/><stop offset="1" stop-color="#A8925F"/>
</linearGradient>
</defs>
<ellipse cx="125" cy="90" rx="100" ry="7" fill="rgba(20,12,4,.35)"/>
<path d="M28 22c30-5 164-5 194 0v56c-30 5-164 5-194 0Z" fill="url(#rolvel)" stroke="{INK}" stroke-width="4.5"/>
<path d="M34 30c28-4 154-4 182 0" stroke="#C9AE7E" stroke-width="2" fill="none" opacity=".8"/>
<path d="M34 70c28 4 154 4 182 0" stroke="#C9AE7E" stroke-width="2" fill="none" opacity=".8"/>
<rect x="12" y="12" width="20" height="76" rx="10" fill="url(#rolcyl)" stroke="{INK}" stroke-width="4"/>
<rect x="218" y="12" width="20" height="76" rx="10" fill="url(#rolcyl)" stroke="{INK}" stroke-width="4"/>
<path d="M22 18v64M228 18v64" stroke="rgba(90,64,28,.35)" stroke-width="2"/>
</svg>
''')

# ── Linten voor sectiekoppen: blauw, groen, paars ───────────────────
def lint(naam, licht, midden, donker):
    schrijf(naam, f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 72">
<defs>
<linearGradient id="lintband" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{licht}"/><stop offset=".55" stop-color="{midden}"/><stop offset="1" stop-color="{donker}"/>
</linearGradient>
</defs>
<path d="M30 46l-20 16 4-24-4-24 20 16Z" fill="{donker}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<path d="M262 60c6-9 6-33 0-44l12 6v34Z" fill="{donker}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<path d="M26 12h230c8 0 12 5 12 11v26c0 6-4 11-12 11H26c-6-10-6-38 0-48Z"
  fill="url(#lintband)" stroke="{INK}" stroke-width="4.5"/>
<path d="M34 20h216M34 52h216" stroke="#C9A227" stroke-width="2" opacity=".85" stroke-dasharray="1 5" stroke-linecap="round"/>
<path d="M34 17c60-3 160-3 216 0" stroke="rgba(255,255,255,.28)" stroke-width="2.5" fill="none"/>
</svg>
''')
lint("lint-blauw.svg", "#41639B", "#2E4A78", "#1F3557")
lint("lint-groen.svg", "#5E8C4B", "#4C7A3F", "#35592B")
lint("lint-paars.svg", "#7E5FA5", "#6B4E8E", "#4C3568")

# ── Plaquette: blauwe metalen plaat met gouden bies ─────────────────
schrijf("plaquette.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120">
<defs>
<linearGradient id="plaq" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#41639B"/><stop offset=".55" stop-color="#2E4A78"/><stop offset="1" stop-color="#1F3557"/>
</linearGradient>
<linearGradient id="plaqgoud" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#E4C25C"/><stop offset=".5" stop-color="#C9A227"/><stop offset="1" stop-color="#8F7115"/>
</linearGradient>
</defs>
<ellipse cx="240" cy="110" rx="212" ry="8" fill="rgba(20,12,4,.38)"/>
<rect x="10" y="8" width="460" height="98" rx="18" fill="url(#plaqgoud)" stroke="{INK}" stroke-width="5"/>
<rect x="20" y="18" width="440" height="78" rx="12" fill="url(#plaq)" stroke="{INK}" stroke-width="3.5"/>
<path d="M30 30c60-8 150-10 210-6c-70 2-150 8-196 20c-8-4-12-9-14-14Z" fill="rgba(255,255,255,.14)"/>
<g fill="#F0D77A" stroke="{INK}" stroke-width="2">
<circle cx="34" cy="32" r="3.2"/><circle cx="446" cy="32" r="3.2"/>
<circle cx="34" cy="82" r="3.2"/><circle cx="446" cy="82" r="3.2"/>
</g>
</svg>
''')

# ── Portretlijsten: metalen schild (open midden) en gouden krans ────
schrijf("portret-schild.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 152">
<defs>
<linearGradient id="staal" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#CDD3DC"/><stop offset=".5" stop-color="#9AA2B0"/><stop offset="1" stop-color="#6E7684"/>
</linearGradient>
</defs>
<path fill-rule="evenodd" fill="url(#staal)" stroke="{INK}" stroke-width="5" d="
M70 6c20 0 34 5 42 10v48c0 30-19 51-42 59c-23-8-42-29-42-59V16c8-5 22-10 42-10Z
M70 20c-15 0-26 3-31 6v38c0 23 14 40 31 47c17-7 31-24 31-47V26c-5-3-16-6-31-6Z"/>
<path d="M70 20c15 0 26 3 31 6v38c0 23-14 40-31 47c-17-7-31-24-31-47V26c5-3 16-6 31-6Z"
  fill="none" stroke="{INK}" stroke-width="3.5"/>
<path d="M36 20c8-4 18-7 30-7c-14 4-24 9-30 16V20Z" fill="rgba(255,255,255,.45)"/>
<g fill="#E6EAF0" stroke="{INK}" stroke-width="1.8">
<circle cx="70" cy="12" r="2.8"/><circle cx="38" cy="21" r="2.8"/><circle cx="102" cy="21" r="2.8"/>
<circle cx="30" cy="62" r="2.8"/><circle cx="110" cy="62" r="2.8"/>
<circle cx="45" cy="103" r="2.8"/><circle cx="95" cy="103" r="2.8"/>
</g>
</svg>
''')
schrijf("portret-krans.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 160">
<defs>
<linearGradient id="krgoud" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#E4C25C"/><stop offset=".5" stop-color="#C9A227"/><stop offset="1" stop-color="#8F7115"/>
</linearGradient>
</defs>
<circle cx="75" cy="90" r="58" fill="none" stroke="{INK}" stroke-width="18"/>
<circle cx="75" cy="90" r="58" fill="none" stroke="url(#krgoud)" stroke-width="12"/>
<g fill="url(#krgoud)" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round">
<path d="M20 68c8-2 13 2 14 8c-7 2-13-2-14-8ZM14 92c8 0 12 5 12 11c-8 0-12-5-12-11ZM18 116c8 1 11 7 10 13c-8-1-11-7-10-13ZM32 138c7 3 9 9 6 15c-7-3-9-9-6-15Z"/>
<path d="M130 68c-8-2-13 2-14 8c7 2 13-2 14-8ZM136 92c-8 0-12 5-12 11c8 0 12-5 12-11ZM132 116c-8 1-11 7-10 13c8-1 11-7 10-13ZM118 138c-7 3-9 9-6 15c7-3 9-9 6-15Z"/>
</g>
<path d="M52 34v-15l9 7 14-13 14 13 9-7v15c0 4-3 7-7 7H59c-4 0-7-3-7-7Z"
  fill="url(#krgoud)" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="61" cy="17" r="3.2" fill="#E4C25C" stroke="{INK}" stroke-width="2.2"/>
<circle cx="75" cy="11" r="3.2" fill="#E4C25C" stroke="{INK}" stroke-width="2.2"/>
<circle cx="89" cy="17" r="3.2" fill="#E4C25C" stroke="{INK}" stroke-width="2.2"/>
</svg>
''')

# ── Lakzegel met kroon ──────────────────────────────────────────────
schrijf("zegel.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90">
<defs>
<radialGradient id="lak" cx=".35" cy=".3" r=".9">
<stop offset="0" stop-color="#E06A5C"/><stop offset=".45" stop-color="#B03A2E"/><stop offset="1" stop-color="#7E1F16"/>
</radialGradient>
</defs>
<path d="M45 6c12-2 24 3 31 12c7 9 9 20 5 30c5 8 3 18-4 24c-8 7-18 9-27 12c-10 3-21 1-28-6C15 71 10 62 12 52C8 43 10 32 17 25C24 17 34 8 45 6Z"
  fill="url(#lak)" stroke="#5E140D" stroke-width="3"/>
<path d="M30 55v-13l7 5 8-9 8 9 7-5v13c0 2-2 4-4 4H34c-2 0-4-2-4-4Z"
  fill="none" stroke="#F3D9CE" stroke-width="3.4" stroke-linejoin="round" opacity=".85"/>
<path d="M24 22c6-6 14-9 21-9" stroke="rgba(255,255,255,.5)" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>
''')

# ── Breed schild voor de Controleer-knop: het woord past erin ───────
schrijf("schild-breed.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 176">
<defs>
<linearGradient id="sbblauw" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#41639B"/><stop offset=".55" stop-color="#2E4A78"/><stop offset="1" stop-color="#1F3557"/>
</linearGradient>
<linearGradient id="sbgoud" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#E4C25C"/><stop offset=".5" stop-color="#C9A227"/><stop offset="1" stop-color="#8F7115"/>
</linearGradient>
</defs>
<ellipse cx="150" cy="164" rx="118" ry="9" fill="rgba(20,12,4,.4)"/>
<path d="M150 34c46 0 78 6 96 12v52c0 34-42 58-96 70c-54-12-96-36-96-70V46c18-6 50-12 96-12Z"
  fill="url(#sbgoud)" stroke="{INK}" stroke-width="6"/>
<path d="M150 47c40 0 68 5 83 10v40c0 28-36 49-83 60c-47-11-83-32-83-60V57c15-5 43-10 83-10Z"
  fill="url(#sbblauw)" stroke="{INK}" stroke-width="4"/>
<path d="M74 60c18-7 44-11 76-11c10 0 20 0 29 1c-40 3-72 10-92 22c-7-3-11-7-13-12Z" fill="rgba(255,255,255,.15)"/>
<g fill="#F0D77A" stroke="{INK}" stroke-width="2">
<circle cx="150" cy="41" r="3.4"/><circle cx="92" cy="46" r="3.4"/><circle cx="208" cy="46" r="3.4"/>
<circle cx="62" cy="66" r="3.4"/><circle cx="238" cy="66" r="3.4"/>
<circle cx="70" cy="118" r="3.4"/><circle cx="230" cy="118" r="3.4"/>
<circle cx="150" cy="160" r="3.4"/>
</g>
<g>
<path d="M118 26V9l12 8 12-12 8 8 8-8 12 12 12-8v17c0 4-4 7-8 7h-48c-4 0-8-3-8-7Z"
  fill="url(#sbgoud)" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>
<circle cx="130" cy="7" r="3.6" fill="#E4C25C" stroke="{INK}" stroke-width="2.5"/>
<circle cx="150" cy="2.6" r="3.6" fill="#E4C25C" stroke="{INK}" stroke-width="2.5"/>
<circle cx="170" cy="7" r="3.6" fill="#E4C25C" stroke="{INK}" stroke-width="2.5"/>
<path d="M124 20c14 3 38 3 52 0" stroke="rgba(255,255,255,.45)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
</g>
</svg>
''')

print("klaar")
