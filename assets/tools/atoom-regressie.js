/* ============================================================
   Regressieharnas voor de regelmotor
   ------------------------------------------------------------
   Plak dit in de console van de builder (of laad het via een
   <script>-tag) en gebruik:

     atoomRegressie.leg("voor")     eerst, met de oude motor
     ... verbouw de motor ...
     atoomRegressie.vergelijk("voor")   daarna

   Het harnas loopt elk atoom af, met elke zinnige combinatie van
   argumenten, voor elke persoon op het bord. Dat levert enkele
   duizenden uitspraken op per level. Verandert er één van waar
   naar onwaar, dan evalueert een level straks anders dan de
   bouwer bedoelde — en dat merk je zonder dit harnas pas veel
   later, als een puzzel ineens twee oplossingen blijkt te hebben.

   De meting gaat via localStorage, zodat er geen bestanden heen
   en weer hoeven en je zo vaak kunt vergelijken als je wilt.
   ============================================================ */
(function (global) {
  "use strict";

  var LEVELS = [
    "/ClueBoard%20Player/Levels/een_hinderlaag_vol_struikrovers.json",
    "/ClueBoard%20Player/Levels/herberg_de_doortocht.json"
  ];
  var MAX_WAARDEN = 12;    /* per slot: zoveel opties proberen */
  var MAX_COMBOS = 240;    /* per atoom: zoveel combinaties    */

  /* Alle uitspraken van één bord, als {sleutel: waar/onwaar}. */
  function tabelVanHuidigBord() {
    var uit = {};
    var personen = Object.keys(S.people).sort(function (a, b) {
      return parseInt(a.slice(1), 10) - parseInt(b.slice(1), 10);
    });
    Object.keys(ATOMS).forEach(function (id) {
      var def = ATOMS[id];
      var slots = def.slots || {};
      var namen = Object.keys(slots);
      var combos = [{}];
      namen.forEach(function (nm) {
        var opts = slotOptions(slots[nm], {});
        var waarden = opts.length ? opts.map(function (o) { return o.v; }) : [""];
        var nieuw = [];
        combos.forEach(function (c) {
          waarden.slice(0, MAX_WAARDEN).forEach(function (v) {
            var kopie = Object.assign({}, c);
            kopie[nm] = v;
            nieuw.push(kopie);
          });
        });
        combos = nieuw.slice(0, MAX_COMBOS);
      });
      combos.forEach(function (args) {
        var sleutel = id + "(" + namen.map(function (n) {
          return n + "=" + args[n];
        }).join(",") + ")";
        if (def.scope === "person") {
          personen.forEach(function (p) {
            uit[sleutel + "|" + p] = !!atomTrue(id, args, p);
          });
        } else {
          uit[sleutel] = !!atomTrue(id, args, null);
        }
      });
    });
    return uit;
  }

  function wacht(ms) {
    return new Promise(function (r) { setTimeout(r, ms); });
  }

  async function meet() {
    var uit = {};
    for (var i = 0; i < LEVELS.length; i++) {
      var raw = await fetch(LEVELS[i]).then(function (r) { return r.json(); });
      applyImport(JSON.parse(JSON.stringify(raw)));
      await wacht(350);
      var t = tabelVanHuidigBord();
      uit[LEVELS[i]] = {
        aantal: Object.keys(t).length,
        waar: Object.keys(t).filter(function (k) { return t[k]; }).sort()
      };
    }
    return uit;
  }

  async function leg(naam) {
    var m = await meet();
    localStorage.setItem("clueboard_atoom_" + naam, JSON.stringify(m));
    var totaal = 0, waar = 0;
    Object.keys(m).forEach(function (k) { totaal += m[k].aantal; waar += m[k].waar.length; });
    console.log("vastgelegd als '" + naam + "': " + totaal + " uitspraken, " + waar + " waar");
    return m;
  }

  async function vergelijk(naam) {
    var oud = JSON.parse(localStorage.getItem("clueboard_atoom_" + naam) || "null");
    if (!oud) { console.error("geen meting '" + naam + "' gevonden"); return null; }
    var nu = await meet();
    var verschillen = [];
    Object.keys(oud).forEach(function (lvl) {
      var a = new Set(oud[lvl].waar), b = new Set((nu[lvl] || {}).waar || []);
      if (!nu[lvl]) { verschillen.push(lvl + ": ontbreekt nu"); return; }
      if (oud[lvl].aantal !== nu[lvl].aantal) {
        verschillen.push(lvl + ": aantal uitspraken " + oud[lvl].aantal + " -> " + nu[lvl].aantal);
      }
      oud[lvl].waar.forEach(function (k) { if (!b.has(k)) verschillen.push(lvl + ": WAS waar, nu niet -> " + k); });
      (nu[lvl].waar || []).forEach(function (k) { if (!a.has(k)) verschillen.push(lvl + ": is NU waar, was niet -> " + k); });
    });
    if (!verschillen.length) console.log("geen verschillen: de motor evalueert precies hetzelfde");
    else console.warn(verschillen.length + " verschillen:\n" + verschillen.slice(0, 60).join("\n"));
    return verschillen;
  }

  global.atoomRegressie = { leg: leg, vergelijk: vergelijk, meet: meet };
})(window);
