/* Regressieharnas voor de oplossingszoeker in de bouwer.
   Legt per level en per variant (alle regels, en telkens één regel weg -- dat
   geeft ook borden met meerdere oplossingen) de uitkomst van zoekOplossingen
   vast in localStorage. Gebruik in de console van de bouwer (via de server):

     await import-achtig laden: een <script src="/assets/tools/zoek-regressie.js">
     await zoekRegressie.meet("voor", 20000)     met de oude zoeker
     ... verbouw de zoeker, herlaad, laad dit script opnieuw ...
     await zoekRegressie.meet("na", 20000)
     zoekRegressie.vergelijk("voor", "na")       verschil moet [] zijn

   Status en aantal moeten identiek blijven; alleen de tijd mag veranderen.
   De lijst LEVELS hieronder bijwerken als er levels bijkomen of hernoemen. */
window.zoekRegressie = (function(){
  const LEVELS = [
    "Kronieken 1v6 Herberg de Doortocht.json",
    "Kronieken 2v5 Een hinderlaag vol struikrovers.json",
    "Kronieken 3v6 De Watermolen.json",
    "Kronieken 4v6 De Kathedraal.json",
    "Kronieken 5v12 De Kerkers.json",
    "Kronieken 6v8 Het Fort.json",
    "Kronieken 7v7 De Viersprong.json",
    "Kronieken 8v3 De koningklijke jachtpartij.json",
    "Kronieken 9v2 De Ambachtsstraat.json",
    "Kronieken 10v5 De taverne.json",
    "Originals 1v3 De Troonzaal.json",
    "Originals 2v3 Het Huis van Vastrad.json",
    "Originals 3v15 Achter de Gracht.json",
    "Originals 4v8 Het Jachthuis.json",
    "Originals 5v6 De Oude Gevangenis.json",
    "Originals 6v4 Het Hofbal.json",
    "Originals 7v4 Het Stille Huis.json"
  ];
  const uit = { klaar:false, rijen:[], bezig:"" };
  async function meet(label, budget, alleen){
    uit.klaar = false; uit.rijen = []; uit.label = label;
    for (const f of LEVELS){
      if (alleen && !alleen.some(a => f.indexOf(a) >= 0)) continue;
      const data = await fetch("/player/Levels/" + encodeURIComponent(f)).then(r => r.json());
      applyImport(data); initContent();
      const alle = S.content.clues.slice();
      const varianten = [{ weg:null }].concat(alle.map((c, i) => ({ weg:i })).filter(v => !alle[v.weg].locked));
      for (const v of varianten){
        uit.bezig = f + " / " + (v.weg === null ? "alle" : "zonder " + alle[v.weg].id);
        S.content.clues = v.weg === null ? alle.slice() : alle.filter((_, i) => i !== v.weg);
        await new Promise(r => setTimeout(r, 0));
        const t = performance.now();
        const r = zoekOplossingen({ ms: budget });
        uit.rijen.push({ level:f.replace(/\.json$/, ""), variant:v.weg === null ? "alle" : alle[v.weg].id,
          status:r.status, aantal:r.aantal === undefined ? null : r.aantal, meerDan:!!r.meerDan,
          ms:Math.round(performance.now() - t), knopen:r.knopen,
          eerste:(r.oplossingen || []).length ? Object.keys(r.oplossingen[0]).sort().map(p => p + ":" + r.oplossingen[0][p]).join(" ") : "" });
      }
      S.content.clues = alle;
    }
    try { localStorage.setItem("zoekRegressie:" + label, JSON.stringify(uit.rijen)); } catch (e) {}
    uit.klaar = true; uit.bezig = "";
  }
  function vergelijk(a, b){
    const A = JSON.parse(localStorage.getItem("zoekRegressie:" + a) || "[]");
    const B = JSON.parse(localStorage.getItem("zoekRegressie:" + b) || "[]");
    const sleutel = r => r.level + "|" + r.variant;
    const mapB = new Map(B.map(r => [sleutel(r), r]));
    const verschil = [], tijd = [];
    A.forEach(r => {
      const s = mapB.get(sleutel(r));
      if (!s) return;
      if (r.status !== "onbepaald" && s.status !== "onbepaald" &&
          (r.status !== s.status || r.aantal !== s.aantal || r.meerDan !== s.meerDan))
        verschil.push([sleutel(r), r.status, r.aantal, s.status, s.aantal]);
      tijd.push([sleutel(r), r.ms, s.ms, r.status, s.status]);
    });
    return { vergeleken:tijd.length, verschil, tijd };
  }
  return { meet, vergelijk, uit };
})();
