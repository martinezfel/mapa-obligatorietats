import json

with open("municipis.json", encoding="utf-8") as f:
    municipis = json.load(f)
with open("serveis.json", encoding="utf-8") as f:
    serveis = json.load(f)
with open("textos.json", encoding="utf-8") as f:
    textos = json.load(f)

MUNICIPIS_JSON = json.dumps(municipis, ensure_ascii=False)
SERVEIS_JSON = json.dumps(serveis, ensure_ascii=False)
TEXTOS_JSON = json.dumps(textos, ensure_ascii=False)

AMBIT_ORDER = [
    "Urbanisme, via pública i medi ambient",
    "Salut",
    "Cultura",
    "Serveis socials",
    "Seguretat i protecció",
    "Esports i lleure",
    "Educació i joventut",
    "Mobilitat i transport",
    "Comerç, ocupació i promoció econòmica",
    "Habitatge",
    "Organització interna i transparència",
]
AMBIT_ORDER_JSON = json.dumps(AMBIT_ORDER, ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mapa d'obligatorietats municipals — CASM</title>
<style>
  :root {
    --bg: #FFFFFF;
    --text: #1A1A1A;
    --text-body: #333333;
    --text-meta: #707070;
    --border: #D7DCE0;
    --accent: #935580;
    --accent-soft: #F5EFF2;
    --bloc-im: #6A8D8E;
    --bloc-im-soft: #EDF2F2;
    --pendent: #9D9D9D;
    --pendent-bg: #F3F3F3;
    --focus: #935580;
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    background: var(--bg);
    color: var(--text-body);
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  body { padding-bottom: 4rem; }
  a { color: var(--accent); }
  .wrap { max-width: 880px; margin: 0 auto; padding: 0 1.25rem; }
  svg.icon { width: 14px; height: 14px; flex-shrink: 0; vertical-align: -2px; }

  header.top { padding: 1.75rem 0 0; }
  header.top h1 { font-size: 1.5rem; font-weight: 700; margin: 0 0 0.4rem; color: var(--text); letter-spacing: -0.01em; }
  header.top p.subtitle { margin: 0; color: var(--text-meta); font-size: 0.92rem; line-height: 1.5; width: 100%; }

  .top-links { margin-top: 0.9rem; display: flex; gap: 1rem; flex-wrap: wrap; }
  .top-links button.link-btn { font-family: inherit; font-size: 0.8rem; color: var(--accent); background: none; border: none; padding: 0; cursor: pointer; text-decoration: underline; }

  .entrada { margin-top: 1.8rem; display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; }
  .entrada-card { border: 1px solid var(--border); border-radius: 8px; padding: 1.1rem 1.1rem 1.2rem; text-align: left; background: #fff; cursor: pointer; font-family: inherit; }
  .entrada-card .card-icon { margin-bottom: 0.6rem; }
  .entrada-card .card-icon svg { width: 26px; height: 26px; }
  .entrada-card h3 { margin: 0 0 0.35rem; font-size: 1rem; color: var(--text); }
  .entrada-card p { margin: 0; font-size: 0.82rem; color: var(--text-meta); line-height: 1.5; }
  @media (max-width: 560px) { .entrada { grid-template-columns: 1fr; } }

  .municipi-search-block { margin-top: 1.2rem; }
  .field { position: relative; flex: 1 1 220px; }
  input[type="text"], select {
    width: 100%; font-family: inherit; font-size: 0.88rem; padding: 0.55rem 0.7rem;
    border: 1px solid var(--border); border-radius: 4px; background: #fff; color: var(--text);
  }
  input[type="text"]:focus, select:focus, button:focus-visible { outline: 2px solid var(--focus); outline-offset: 1px; }
  label.field-label { display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--text-meta); margin-bottom: 0.3rem; }
  #municipi-suggestions {
    position: absolute; top: 100%; left: 0; right: 0; background: #fff; border: 1px solid var(--border);
    border-top: none; border-radius: 0 0 4px 4px; max-height: 220px; overflow-y: auto; z-index: 30; display: none;
  }
  #municipi-suggestions button {
    display: block; width: 100%; text-align: left; background: none; border: none; padding: 0.5rem 0.7rem;
    font-size: 0.85rem; cursor: pointer; font-family: inherit; color: var(--text-body);
  }
  #municipi-suggestions button:hover, #municipi-suggestions button:focus { background: var(--accent-soft); }

  .controls { position: sticky; top: 0; background: var(--bg); padding: 0.9rem 0; z-index: 20; border-bottom: 1px solid var(--border); }

  .municipi-context { padding: 0.65rem 0.8rem; background: #FAFAFA; border: 1px solid var(--border); border-radius: 6px; }
  .municipi-context .top-row { display: flex; align-items: center; justify-content: space-between; gap: 0.6rem; flex-wrap: wrap; }
  .municipi-context .name { font-size: 0.84rem; color: var(--text-body); }
  .municipi-context .name strong { color: var(--text); }
  button.clear-btn { display: inline-flex; align-items: center; gap: 0.3rem; border: none; background: none; color: var(--accent); font-family: inherit; font-size: 0.76rem; cursor: pointer; padding: 0; }
  button.clear-btn .x-icon { display: inline-flex; align-items: center; justify-content: center; width: 14px; height: 14px; border-radius: 50%; border: 1px solid var(--accent); font-size: 0.65rem; line-height: 1; }
  .municipi-context .explain { font-size: 0.76rem; color: var(--text-meta); margin: 0.5rem 0 0; }

  .type-toggles { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.8rem; }
  .type-toggle-chip { display: inline-flex; align-items: center; gap: 0.4rem; font-family: inherit; font-size: 0.8rem; padding: 0.4rem 0.7rem; border-radius: 100px; border: 1px solid var(--border); background: #fff; color: var(--text-meta); cursor: pointer; }
  .type-toggle-chip.on.obligatori { border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }
  .type-toggle-chip.on.interes { border-color: var(--bloc-im); color: var(--bloc-im); background: var(--bloc-im-soft); }
  .type-toggle-chip input { display: none; }

  details.filtre-panel { margin-top: 0.85rem; border: 1px solid var(--border); border-radius: 6px; }
  details.filtre-panel > summary { list-style: none; cursor: pointer; padding: 0.65rem 0.9rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; color: var(--text-body); }
  details.filtre-panel > summary::-webkit-details-marker { display: none; }
  details.filtre-panel > summary .filtre-count { color: var(--text-meta); }
  details.filtre-panel > summary .chev { color: var(--text-meta); transition: transform .15s ease; }
  details.filtre-panel[open] > summary .chev { transform: rotate(90deg); }
  .filtre-panel-body { padding: 0 0.9rem 0.8rem; border-top: 1px solid var(--border); }
  .search-filter-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.7rem; }

  main { padding-top: 1.3rem; }

  details.ambit { border: 1px solid var(--border); border-radius: 6px; margin-bottom: 0.6rem; overflow: hidden; }
  details.ambit > summary { list-style: none; cursor: pointer; padding: 0.7rem 0.9rem; font-weight: 700; font-size: 0.92rem; color: var(--text); background: #FAFAFA; display: flex; justify-content: space-between; align-items: center; }
  details.ambit > summary::-webkit-details-marker { display: none; }
  details.ambit > summary .count { font-weight: 400; color: var(--text-meta); font-size: 0.78rem; }
  details.ambit > summary .chev { transition: transform 0.15s ease; color: var(--text-meta); margin-left: 0.5rem; }
  details.ambit[open] > summary .chev { transform: rotate(90deg); }

  .servei-list { border-top: 1px solid var(--border); }
  details.servei { border-bottom: 1px solid var(--border); }
  details.servei:last-child { border-bottom: none; }
  details.servei > summary { list-style: none; cursor: pointer; padding: 0.7rem 0.9rem; display: flex; gap: 0.7rem; align-items: flex-start; justify-content: space-between; }
  details.servei > summary::-webkit-details-marker { display: none; }
  details.servei.pendent > summary { background: var(--pendent-bg); }
  .servei-name-wrap { flex: 1; min-width: 0; }
  .tipus-tag { display: inline-flex; align-items: center; gap: 0.3rem; font-size: 0.7rem; font-weight: 700; padding: 0.12rem 0.5rem 0.12rem 0.4rem; border-radius: 100px; margin-bottom: 0.3rem; }
  .tipus-tag.obligatori { background: var(--accent-soft); color: var(--accent); }
  .tipus-tag.interes { background: var(--bloc-im-soft); color: var(--bloc-im); }
  .servei-name { display: block; font-size: 0.9rem; font-weight: 600; color: var(--text); }
  .servei-resum { font-size: 0.82rem; color: var(--text-meta); margin: 0.3rem 0 0; line-height: 1.45; }
  .badges { display: flex; gap: 0.35rem; flex-wrap: wrap; flex-shrink: 0; align-items: center; }
  .badge { font-size: 0.7rem; padding: 0.2rem 0.5rem; border-radius: 100px; white-space: nowrap; border: 1px solid var(--border); color: var(--text-meta); background: #fff; }
  .badge.pendent { background: #EFEFEF; color: var(--pendent); border-color: transparent; }
  details.servei > summary .chev { color: var(--text-meta); margin-top: 0.15rem; transition: transform 0.15s ease; }
  details.servei[open] > summary .chev { transform: rotate(90deg); }

  .servei-detail { padding: 0 0.9rem 1rem; }
  .checklist-intro { font-size: 0.8rem; color: var(--text-meta); margin: 0.3rem 0 0.6rem; }
  .checklist-group-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--text-meta); font-weight: 700; margin: 0.9rem 0 0.4rem; }
  .checklist-group-label:first-child { margin-top: 0; }

  details.check-item { border-top: 1px solid var(--border); }
  .checklist-group-label + details.check-item { border-top: none; }
  details.check-item > summary { list-style: none; cursor: pointer; display: flex; gap: 0.6rem; padding: 0.55rem 0; align-items: flex-start; }
  details.check-item > summary::-webkit-details-marker { display: none; }
  .check-icon { flex-shrink: 0; color: var(--text-meta); padding-top: 0.1rem; }
  .check-content { flex: 1; }
  .check-question { font-size: 0.86rem; color: var(--text-body); margin: 0 0 0.2rem; line-height: 1.5; }
  .check-cita-row { display: flex; align-items: center; gap: 0.3rem; }
  .check-cita { font-size: 0.74rem; color: var(--accent); }
  .check-cita-chev { color: var(--accent); font-size: 0.65rem; transition: transform 0.15s ease; }
  details.check-item[open] .check-cita-chev { transform: rotate(90deg); }
  .check-item-detail { padding: 0 0 0.7rem 1.9rem; font-size: 0.8rem; line-height: 1.55; color: var(--text-body); }

  .servei-meta-row { display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.78rem; color: var(--text-meta); margin: 0.9rem 0 0.7rem; }
  .servei-meta-row span strong { color: var(--text-body); font-weight: 600; }

  .legal-toggle { font-family: inherit; font-size: 0.78rem; color: var(--accent); background: none; border: 1px solid var(--border); border-radius: 100px; padding: 0.35rem 0.75rem; cursor: pointer; }
  .legal-toggle:hover { background: var(--accent-soft); }
  .legal-box { margin-top: 0.7rem; padding: 0.75rem 0.9rem; background: #FAFAFA; border: 1px solid var(--border); border-radius: 6px; display: none; }
  .legal-box.open { display: block; }
  .legal-box ul { margin: 0; padding-left: 1.1rem; font-size: 0.82rem; line-height: 1.7; color: var(--text-body); }

  .pendent-note { font-size: 0.82rem; color: var(--text-meta); font-style: italic; margin: 0.3rem 0 0; }
  .empty-state { padding: 2rem 0; text-align: center; color: var(--text-meta); font-size: 0.88rem; }

  footer.site { margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--border); font-size: 0.76rem; color: var(--text-meta); line-height: 1.6; }
  footer.site p { margin: 0 0 0.4rem; }

  @media (max-width: 560px) {
    .search-filter-row { flex-direction: column; }
  }
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <h1 id="app-title"></h1>
    <p class="subtitle" id="app-subtitle"></p>
  </header>

  <div id="entrada-screen" class="entrada"></div>

  <div id="municipi-search-block" class="municipi-search-block" style="display:none;">
    <label class="field-label" for="municipi-input" id="municipi-input-label"></label>
    <div class="field">
      <input type="text" id="municipi-input" autocomplete="off">
      <div id="municipi-suggestions"></div>
    </div>
    <div class="top-links"><button type="button" class="link-btn" id="btn-torna-inici-1"></button></div>
  </div>

  <div id="app-controls" class="controls" style="display:none;">
    <div id="municipi-context" class="municipi-context" style="display:none;"></div>
    <div id="explora-header" style="display:none;">
      <div class="top-links">
        <button type="button" class="link-btn" id="btn-consulta-municipi"></button>
        <button type="button" class="link-btn" id="btn-torna-inici-2"></button>
      </div>
      <div class="type-toggles" id="type-toggles"></div>
    </div>
    <details class="filtre-panel" id="filtre-panel">
      <summary><span id="filtre-panel-title"></span><span class="filtre-count" id="filtre-panel-count"></span><span class="chev">&#9656;</span></summary>
      <div class="filtre-panel-body">
        <div class="search-filter-row">
          <div class="field"><input type="text" id="search-input"></div>
          <div class="field" style="flex: 0 1 240px;"><select id="ambit-select"></select></div>
        </div>
      </div>
    </details>
  </div>

  <main id="app"></main>

  <footer class="site" id="app-footer"></footer>
</div>

<script>
const MUNICIPIS = __MUNICIPIS_JSON__;
const SERVEIS = __SERVEIS_JSON__;
const AMBIT_ORDER = __AMBIT_ORDER_JSON__;
const T = __TEXTOS_JSON__;

function t(key, vars) {
  let s = T[key] || key;
  if (vars) Object.keys(vars).forEach(k => { s = s.split("{" + k + "}").join(vars[k]); });
  return s;
}

// Escut = obligació legal. Tick = servei d'interès municipal (a valorar).
const ICON_OBLIGATORI = '<svg class="icon" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 1.3L13.5 3.3V7.3C13.5 10.8 11.2 13.1 8 14.6C4.8 13.1 2.5 10.8 2.5 7.3V3.3L8 1.3Z" fill="currentColor"/></svg>';
const ICON_INTERES = '<svg class="icon" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="8" cy="8" r="6.8" stroke="currentColor" stroke-width="1.4"/><path d="M5 8.2L7 10.2L11 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const ICON_CHECKBOX = '<svg class="icon" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="12" height="12" rx="2.5" stroke="currentColor" stroke-width="1.4"/></svg>';
const ICON_MUNICIPI_LARGE = '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:var(--accent)"><path d="M4 21V9L12 3L20 9V21" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 21V13H15V21" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
const ICON_EXPLORA_LARGE = '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="color:var(--text-meta)"><rect x="3.5" y="3.5" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6"/><rect x="13.5" y="3.5" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6"/><rect x="13.5" y="13.5" width="7" height="7" rx="1" stroke="currentColor" stroke-width="1.6"/></svg>';

let state = {
  view: "entrada",             // entrada | cercaMunicipi | municipi | explora
  municipi: null,
  showObligatori: true,
  showInteres: true,
  search: "",
  ambit: "tots",
};

function normalize(str) {
  return (str || "").toString().toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
}

function tramLabel(servei) {
  if (servei.tram_base == null) return t("tram_tots");
  return t("tram_mes_de", { n: servei.tram_base.toLocaleString("ca-ES") });
}

function serveiApplies(servei, poblacio) {
  if (servei.tram_base == null) return true;
  return poblacio > servei.tram_base;
}

function itemApplies(itm, poblacio) {
  if (itm.pob_min != null) {
    if (itm.pob_min_strict ? !(poblacio > itm.pob_min) : !(poblacio >= itm.pob_min)) return false;
  }
  if (itm.pob_max != null) {
    if (itm.pob_max_strict ? !(poblacio < itm.pob_max) : !(poblacio <= itm.pob_max)) return false;
  }
  return true;
}

// Card-level inclusion in municipi view: if the fitxa has a validated checklist, use its
// per-item thresholds (more precise, can include obligations below the headline tram_base,
// e.g. comarcal support for libraries under 5.000 hab.). Fitxes pendents fall back to tram_base.
function cardAppliesForMunicipi(servei, poblacio) {
  if (servei.checklist && servei.checklist.length) {
    return servei.checklist.some(it => itemApplies(it, poblacio));
  }
  return serveiApplies(servei, poblacio);
}

function staticText() {
  document.getElementById("app-title").textContent = t("titol");
  document.getElementById("app-subtitle").textContent = t("subtitol");
  document.getElementById("municipi-input").placeholder = t("municipi_placeholder");
  document.getElementById("municipi-input-label").textContent = t("municipi_placeholder");
  document.getElementById("btn-torna-inici-1").textContent = t("torna_inici");
  document.getElementById("btn-torna-inici-2").textContent = t("torna_inici");
  document.getElementById("btn-consulta-municipi").textContent = t("municipi_canviar_des_explora");
  document.getElementById("search-input").placeholder = t("cerca_placeholder");
  document.getElementById("filtre-panel-title").textContent = t("cerca_filtra_titol");
  document.getElementById("ambit-select").innerHTML = '<option value="tots">' + t("ambit_select_default") + '</option>' +
    AMBIT_ORDER.map(a => '<option value="' + a + '">' + a + '</option>').join("");
  document.getElementById("app-footer").innerHTML =
    '<p>' + t("avis_revisio") + '</p><p>' + t("avis_general") + '</p><p>' + t("avis_organitzacio") + '</p>';
}

function renderEntrada() {
  const el = document.getElementById("entrada-screen");
  el.innerHTML =
    '<button type="button" class="entrada-card" id="entrada-municipi">' +
      '<div class="card-icon">' + ICON_MUNICIPI_LARGE + '</div>' +
      '<h3>' + t("entrada_opcio_municipi_titol") + '</h3><p>' + t("entrada_opcio_municipi_desc") + '</p>' +
    '</button>' +
    '<button type="button" class="entrada-card" id="entrada-explora">' +
      '<div class="card-icon">' + ICON_EXPLORA_LARGE + '</div>' +
      '<h3>' + t("entrada_opcio_explora_titol") + '</h3><p>' + t("entrada_opcio_explora_desc") + '</p>' +
    '</button>';
  document.getElementById("entrada-municipi").addEventListener("click", () => setView("cercaMunicipi"));
  document.getElementById("entrada-explora").addEventListener("click", () => setView("explora"));
}

function setView(view) {
  state.view = view;
  if (view === "explora") { state.showObligatori = true; state.showInteres = true; }
  updateVisibility();
}

function updateVisibility() {
  document.getElementById("entrada-screen").style.display = state.view === "entrada" ? "grid" : "none";
  document.getElementById("municipi-search-block").style.display = (state.view === "cercaMunicipi") ? "block" : "none";
  document.getElementById("app-controls").style.display = (state.view === "municipi" || state.view === "explora") ? "block" : "none";
  document.getElementById("app").style.display = (state.view === "municipi" || state.view === "explora") ? "block" : "none";

  document.getElementById("municipi-context").style.display = (state.view === "municipi") ? "block" : "none";
  document.getElementById("explora-header").style.display = (state.view === "explora") ? "block" : "none";

  if (state.view === "municipi") renderMunicipiContext();
  if (state.view === "explora") renderTypeToggles();
  if (state.view === "municipi" || state.view === "explora") render();
}

function renderTypeToggles() {
  const wrap = document.getElementById("type-toggles");
  wrap.innerHTML =
    '<label class="type-toggle-chip obligatori ' + (state.showObligatori ? "on" : "") + '">' +
      '<input type="checkbox" id="chk-obligatori" ' + (state.showObligatori ? "checked" : "") + '>' +
      ICON_OBLIGATORI + '<span>' + t("filtre_obligatoris_label") + '</span></label>' +
    '<label class="type-toggle-chip interes ' + (state.showInteres ? "on" : "") + '">' +
      '<input type="checkbox" id="chk-interes" ' + (state.showInteres ? "checked" : "") + '>' +
      ICON_INTERES + '<span>' + t("filtre_interes_label") + '</span></label>';
  document.getElementById("chk-obligatori").addEventListener("change", (e) => { state.showObligatori = e.target.checked; renderTypeToggles(); render(); });
  document.getElementById("chk-interes").addEventListener("change", (e) => { state.showInteres = e.target.checked; renderTypeToggles(); render(); });
}

function renderMunicipiContext() {
  const ctx = document.getElementById("municipi-context");
  const m = state.municipi;
  if (!m) return;
  ctx.innerHTML =
    '<div class="top-row"><span class="name">' + t("municipi_seleccionat_prefix") + ' <strong>' + m.nom + '</strong> (' + m.poblacio.toLocaleString("ca-ES") + ' hab., ' + m.comarca + ')</span>' +
    '<button type="button" class="clear-btn"><span class="x-icon">&#10005;</span>' + t("municipi_treure_seleccio") + '</button></div>' +
    '<p class="explain">' + t("municipi_explicacio") + '</p>';
  ctx.querySelector(".clear-btn").addEventListener("click", () => { state.municipi = null; setView("explora"); });
}

function setupMunicipiSearch() {
  const input = document.getElementById("municipi-input");
  const box = document.getElementById("municipi-suggestions");
  input.addEventListener("input", () => {
    const q = normalize(input.value);
    box.innerHTML = "";
    if (q.length < 2) { box.style.display = "none"; return; }
    const matches = MUNICIPIS.filter(m => normalize(m.nom).includes(q)).slice(0, 12);
    if (!matches.length) { box.style.display = "none"; return; }
    matches.forEach(m => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = m.nom + " · " + m.poblacio.toLocaleString("ca-ES") + " hab. (" + m.comarca + ")";
      btn.addEventListener("click", () => selectMunicipi(m));
      box.appendChild(btn);
    });
    box.style.display = "block";
  });
  document.addEventListener("click", (e) => {
    if (!box.contains(e.target) && e.target !== input) box.style.display = "none";
  });
}

function selectMunicipi(m) {
  state.municipi = m;
  document.getElementById("municipi-input").value = "";
  document.getElementById("municipi-suggestions").style.display = "none";
  setView("municipi");
}

function setupTopLinks() {
  document.getElementById("btn-torna-inici-1").addEventListener("click", () => setView("entrada"));
  document.getElementById("btn-torna-inici-2").addEventListener("click", () => setView("entrada"));
  document.getElementById("btn-consulta-municipi").addEventListener("click", () => setView("cercaMunicipi"));
}

function setupControls() {
  document.getElementById("search-input").addEventListener("input", (e) => { state.search = e.target.value; render(); });
  document.getElementById("ambit-select").addEventListener("change", (e) => { state.ambit = e.target.value; render(); });
}

function matchesSearch(servei, q) {
  if (!q) return true;
  const nq = normalize(q);
  if (normalize(servei.nom).includes(nq)) return true;
  if (servei.resum && normalize(servei.resum).includes(nq)) return true;
  if (servei.checklist && servei.checklist.some(it => normalize(it.pregunta).includes(nq) || normalize(it.llei_nom).includes(nq))) return true;
  return false;
}

function baseFilteredByView() {
  if (state.view === "municipi" && state.municipi) {
    return SERVEIS.filter(sv => sv.bloc === "obligatori" && cardAppliesForMunicipi(sv, state.municipi.poblacio));
  }
  if (state.view === "explora") {
    return SERVEIS.filter(sv => (sv.bloc === "obligatori" && state.showObligatori) || (sv.bloc === "interes_municipal" && state.showInteres));
  }
  return SERVEIS.slice();
}

function filteredServeis() {
  return baseFilteredByView().filter(sv => {
    if (state.ambit !== "tots" && sv.ambit !== state.ambit) return false;
    if (!matchesSearch(sv, state.search)) return false;
    return true;
  });
}

function groupedChecklist(sv) {
  // returns [{label, items}] — filtered by municipi population when in municipi view (no label shown),
  // otherwise all items grouped by llindar_label in original order.
  const poblacio = (state.view === "municipi" && state.municipi) ? state.municipi.poblacio : null;
  if (poblacio != null) {
    const items = sv.checklist.filter(it => itemApplies(it, poblacio));
    return items.length ? [{ label: null, items: items }] : [];
  }
  const groups = [];
  sv.checklist.forEach(it => {
    let g = groups.find(g => g.label === it.llindar_label);
    if (!g) { g = { label: it.llindar_label, items: [] }; groups.push(g); }
    g.items.push(it);
  });
  return groups;
}

function serveiCard(sv) {
  const pendent = sv.estat !== "validat";
  const tipusTag = sv.bloc === "obligatori"
    ? '<span class="tipus-tag obligatori">' + ICON_OBLIGATORI + t("distintiu_obligatori") + '</span>'
    : '<span class="tipus-tag interes">' + ICON_INTERES + t("distintiu_interes_municipal") + '</span>';

  let badges = "";
  if (sv.bloc === "obligatori") badges += '<span class="badge">' + tramLabel(sv) + '</span>';
  if (pendent) badges += '<span class="badge pendent">' + t("badge_pendent") + '</span>';

  let body = "";
  if (pendent) {
    body = '<p class="pendent-note">' + t("pendent_nota") + '</p>';
  } else {
    const groups = groupedChecklist(sv);
    body += '<p class="checklist-intro">' + t("checklist_intro") + '</p>';
    groups.forEach(g => {
      if (g.label) body += '<p class="checklist-group-label">' + g.label + '</p>';
      g.items.forEach(it => {
        const refLine = it.llei_nom + (it.article ? ", " + it.article : "");
        body += '<details class="check-item"><summary>' +
          '<span class="check-icon">' + ICON_CHECKBOX + '</span>' +
          '<div class="check-content"><p class="check-question">' + it.pregunta + '</p>' +
          '<span class="check-cita-row"><span class="check-cita">' + refLine + '</span><span class="check-cita-chev">&#9656;</span></span></div>' +
          '</summary>' +
          '<div class="check-item-detail">' + it.explicacio + '</div>' +
          '</details>';
      });
    });
    body += '<div class="servei-meta-row">';
    body += '<span><strong>' + t("meta_competencia_label") + '</strong> ' + capitalize(sv.competencia) + '</span>';
    body += '<span><strong>' + t("meta_actualitzacio_label") + '</strong> ' + formatDate(sv.data_actualitzacio) + '</span>';
    body += '</div>';

    const lleis = [];
    (sv.normativa_mare || []).forEach(l => { if (!lleis.includes(l)) lleis.push(l); });
    groups.forEach(g => g.items.forEach(it => { if (!lleis.includes(it.llei_nom)) lleis.push(it.llei_nom); }));
    body += '<button type="button" class="legal-toggle">' + t("normativa_mostra") + '</button>';
    body += '<div class="legal-box"><ul>' + lleis.map(l => '<li>' + l + '</li>').join("") + '</ul></div>';
  }

  const el = document.createElement("details");
  el.className = "servei" + (pendent ? " pendent" : "");
  el.innerHTML = '<summary><div class="servei-name-wrap">' + tipusTag +
    '<span class="servei-name">' + sv.nom + '</span>' +
    (sv.resum && !pendent ? '<p class="servei-resum">' + sv.resum + '</p>' : '') +
    '</div><div class="badges">' + badges + '<span class="chev">&#9656;</span></div></summary>' +
    '<div class="servei-detail">' + body + '</div>';

  if (!pendent) {
    const toggleBtn = el.querySelector(".legal-toggle");
    const legalBox = el.querySelector(".legal-box");
    toggleBtn.addEventListener("click", (e) => {
      e.preventDefault();
      legalBox.classList.toggle("open");
      toggleBtn.textContent = legalBox.classList.contains("open") ? t("normativa_amaga") : t("normativa_mostra");
    });
  }
  return el;
}

function capitalize(str) {
  if (!str) return "—";
  const map = { propia: "Pròpia", compartida: "Compartida", delegada: "Delegada", impropia: "Impròpia" };
  return map[str] || str;
}
function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleDateString("ca-ES", { day: "numeric", month: "long", year: "numeric" });
}

function render() {
  const app = document.getElementById("app");
  app.innerHTML = "";
  const filtered = filteredServeis();
  const total = baseFilteredByView().length;

  document.getElementById("filtre-panel-count").textContent = t("comptador_resultats", { n: filtered.length, total: total });

  if (!filtered.length) {
    app.innerHTML = '<div class="empty-state">' + t("cap_resultat") + '</div>';
    return;
  }

  AMBIT_ORDER.forEach(ambit => {
    const ambitServeis = filtered.filter(sv => sv.ambit === ambit)
      .sort((a, b) => {
        const aFilled = a.estat === "validat" ? 0 : 1;
        const bFilled = b.estat === "validat" ? 0 : 1;
        if (aFilled !== bFilled) return aFilled - bFilled;
        return a.nom.localeCompare(b.nom, "ca");
      });
    if (!ambitServeis.length) return;
    const det = document.createElement("details");
    det.className = "ambit";
    det.open = true;
    const summary = document.createElement("summary");
    summary.innerHTML = '<span>' + ambit + ' <span class="count">(' + ambitServeis.length + ')</span></span><span class="chev">&#9656;</span>';
    det.appendChild(summary);
    const list = document.createElement("div");
    list.className = "servei-list";
    ambitServeis.forEach(sv => list.appendChild(serveiCard(sv)));
    det.appendChild(list);
    app.appendChild(det);
  });
}

staticText();
renderEntrada();
setupMunicipiSearch();
setupTopLinks();
setupControls();
updateVisibility();
</script>
</body>
</html>
"""

html = html.replace("__MUNICIPIS_JSON__", MUNICIPIS_JSON)
html = html.replace("__SERVEIS_JSON__", SERVEIS_JSON)
html = html.replace("__AMBIT_ORDER_JSON__", AMBIT_ORDER_JSON)
html = html.replace("__TEXTOS_JSON__", TEXTOS_JSON)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML generat:", len(html), "caràcters")
