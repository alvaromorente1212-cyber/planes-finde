/* Planes Finde — app estática (GitHub Pages) que lee de Supabase */
(() => {
  "use strict";

  const CFG = window.PF_CONFIG;
  const sb = window.supabase.createClient(CFG.supabaseUrl, CFG.supabaseKey, {
    auth: { persistSession: false },
  });

  // ---------- Utilidades ----------
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* sin almacenamiento */ } },
  };
  const pad = (n) => String(n).padStart(2, "0");
  const keyOf = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const fromKey = (k) => { const [y, m, d] = k.split("-").map(Number); return new Date(y, m - 1, d); };
  const isoDow = (d) => ((d.getDay() + 6) % 7) + 1; // 1 = lunes ... 7 = domingo
  const MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
  const MES_C = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
  const DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
  const DIAS_PL = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábados", "domingos"];
  function diasTxt(ds) {
    const s = [...ds].sort((a, b) => a - b);
    if (s.join() === "6,7") return "sábados, domingos y festivos";
    if (s.join() === "7") return "domingos y festivos";
    if (s.join() === "2,3,4,5,6,7") return "de martes a domingo";
    if (s.join() === "5,6,7") return "de viernes a domingo";
    const n = s.map((d) => DIAS_PL[d - 1]);
    return n.length > 1 ? `${n.slice(0, -1).join(", ")} y ${n[n.length - 1]}` : n[0];
  }
  const safeUrl = (u) => (/^https?:\/\//i.test(u || "") ? u : null);
  const shortDate = (k) => { const d = fromKey(k); return `${d.getDate()} ${MES_C[d.getMonth()]}`; };
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const TODAY = keyOf(today);

  function km(a, b) {
    const R = 6371, t = Math.PI / 180;
    const dLat = (b.lat - a.lat) * t, dLng = (b.lng - a.lng) * t;
    const x = Math.sin(dLat / 2) ** 2 + Math.cos(a.lat * t) * Math.cos(b.lat * t) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(x));
  }

  const CAT = {
    granja: { e: "🐐", n: "Granja y animales" },
    zoo: { e: "🦒", n: "Zoo y acuario" },
    restaurante: { e: "🍽️", n: "Comer con peques" },
    parque: { e: "🛝", n: "Parque infantil" },
    naturaleza: { e: "🌳", n: "Naturaleza" },
    museo: { e: "🦕", n: "Museo" },
    cubierto: { e: "🧸", n: "Ocio cubierto" },
    espectaculo: { e: "🎭", n: "Teatro y espectáculos" },
    fiesta: { e: "🎃", n: "Fiesta" },
    feria: { e: "🏰", n: "Feria y mercado" },
    taller: { e: "✂️", n: "Taller" },
    evento: { e: "🎪", n: "Evento" },
    ruta: { e: "🥾", n: "Ruta y paseo" },
    otros: { e: "📍", n: "Plan" },
  };
  const cat = (p) => CAT[p.categoria] || CAT.otros;
  const isRuta = (p) => p.categoria === "ruta";
  const CARRITO = {
    si: { tag: "Con carrito", txt: "Se puede hacer con carrito normal" },
    dificil: { tag: "Carrito todoterreno", txt: "Solo con carrito de ruedas grandes o todoterreno; algún tramo complicado" },
    no: { tag: "Sin carrito", txt: "Sin carrito: mejor mochila portabebés o peques que ya caminen" },
  };
  const COMER = {
    monitores: { tag: "Con monitores", txt: "Mientras coméis, hay monitores o animación que se ocupan de los peques" },
    parque: { tag: "Parque infantil", txt: "Tiene parque de bolas o zona de juegos a la vista mientras coméis" },
    animales: { tag: "Con animales", txt: "Los peques ven animales o una granja mientras coméis" },
    espacio_libre: { tag: "Espacio para correr", txt: "Recinto o jardín donde los peques corren a sus anchas mientras coméis" },
  };
  const isComer = (p) => p.categoria === "restaurante" || !!p.comer_jugando;
  const kmTxt = (n) => `${String(Number(n)).replace(".", ",")} km`;

  const FILTERS = [
    { id: "gratis", label: "Gratis", test: (p) => p.gratis },
    { id: "cubierto", label: "A cubierto", test: (p) => p.entorno !== "exterior" },
    { id: "animales", label: "Con animales", test: (p) => ["granja", "zoo"].includes(p.categoria) || /granja|animal/i.test(p.descripcion || "") },
    { id: "comer", label: "Para comer", test: (p) => isComer(p) },
    { id: "comerjuego", label: "Comer mientras juegan", test: (p) => !!p.comer_jugando },
    { id: "monitores", label: "Con monitores", test: (p) => p.comer_jugando === "monitores" },
    { id: "rutas", label: "Rutas y paseos", test: (p) => isRuta(p) },
    { id: "carrito", label: "Con carrito", test: (p) => p.carrito === "si" },
    { id: "sincarrito", label: "Sin carrito", test: (p) => p.carrito === "no" },
    { id: "cerca", label: "A menos de 25 km", test: (p) => p._km != null && p._km <= 25 },
    { id: "opiniones", label: "Con opiniones", test: (p) => (state.revByPlan[p.id] || []).length > 0 },
  ];

  // ---------- Estado ----------
  const state = {
    plans: [],
    reviews: [],
    revByPlan: {},
    weather: {},
    weatherOk: false,
    ages: store.get("pf_ages", []),
    filters: new Set(),
    date: null,
    month: null,
    name: store.get("pf_name", ""),
    tokens: store.get("pf_tokens", {}),
    tab: "planes",
    mapMode: "dia",
    showAllPerm: false,
    showAllRutas: false,
    showAllComer: false,
    feedPerson: null,
    loaded: false,
  };

  function defaultDate() {
    const d = new Date(today);
    const dow = isoDow(d);
    if (dow < 6) d.setDate(d.getDate() + (6 - dow)); // próximo sábado
    return keyOf(d);
  }
  state.date = defaultDate();
  state.month = (() => { const d = fromKey(state.date); return new Date(d.getFullYear(), d.getMonth(), 1); })();

  // ---------- Lógica de planes ----------
  function effectiveDows(k) {
    const d = isoDow(fromKey(k));
    return CFG.festivos[k] ? [d, 7] : [d];
  }
  function dayOk(p, k) {
    if (!p.dias_semana || !p.dias_semana.length) return true;
    return effectiveDows(k).some((x) => p.dias_semana.includes(x));
  }
  function ageOk(p) {
    if (!state.ages.length) return true;
    return state.ages.every((a) => a >= p.edad_min && a <= p.edad_max);
  }
  function filtersOk(p) {
    for (const f of FILTERS) if (state.filters.has(f.id) && !f.test(p)) return false;
    return true;
  }
  function availableOn(p, k) {
    if (p.tipo === "temporal") {
      if (!(p.fecha_inicio <= k && k <= p.fecha_fin)) return false;
    }
    return dayOk(p, k);
  }
  function plansFor(k) {
    return state.plans.filter((p) => availableOn(p, k) && ageOk(p) && filtersOk(p));
  }
  function avg(planId) {
    const r = state.revByPlan[planId] || [];
    if (!r.length) return null;
    return Math.round((r.reduce((s, x) => s + x.nota, 0) / r.length) * 10) / 10;
  }
  function isRainy(k) {
    const w = state.weather[k];
    return !!w && (w.prob >= 50 || [61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99].includes(w.code));
  }
  function sortPlans(list, k) {
    const rainy = isRainy(k);
    return list.slice().sort((a, b) => {
      if (rainy) {
        const ra = a.entorno === "exterior" ? 1 : 0, rb = b.entorno === "exterior" ? 1 : 0;
        if (ra !== rb) return ra - rb;
      }
      if (a.tipo === "temporal" && b.tipo === "temporal" && a.fecha_fin !== b.fecha_fin) {
        return a.fecha_fin < b.fecha_fin ? -1 : 1;
      }
      const sa = avg(a.id) ?? -1, sb2 = avg(b.id) ?? -1;
      if (sa !== sb2) return sb2 - sa;
      return (a._km ?? 999) - (b._km ?? 999);
    });
  }

  // ---------- Carga de datos ----------
  async function loadData() {
    const [pRes, rRes] = await Promise.all([
      sb.from("pf_planes").select("*").or(`tipo.eq.permanente,fecha_fin.gte.${TODAY}`),
      sb.from("pf_valoraciones").select("id,plan_id,autor,nota,comentario,edad_hijos,fecha_visita,creado").order("creado", { ascending: false }),
    ]);
    if (pRes.error) throw pRes.error;
    if (rRes.error) throw rRes.error;
    state.plans = pRes.data.map((p) => ({ ...p, _km: p.lat != null ? Math.round(km(CFG.origen, p)) : null }));
    setReviews(rRes.data);
  }
  function setReviews(list) {
    state.reviews = list;
    state.revByPlan = {};
    for (const r of list) (state.revByPlan[r.plan_id] ||= []).push(r);
  }
  async function reloadReviews() {
    const { data, error } = await sb.from("pf_valoraciones").select("id,plan_id,autor,nota,comentario,edad_hijos,fecha_visita,creado").order("creado", { ascending: false });
    if (!error) setReviews(data);
  }
  async function loadWeather() {
    try {
      const u = `https://api.open-meteo.com/v1/forecast?latitude=${CFG.origen.lat}&longitude=${CFG.origen.lng}` +
        `&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FMadrid&forecast_days=16`;
      const r = await fetch(u);
      const j = await r.json();
      j.daily.time.forEach((t, i) => {
        state.weather[t] = {
          code: j.daily.weather_code[i],
          max: Math.round(j.daily.temperature_2m_max[i]),
          min: Math.round(j.daily.temperature_2m_min[i]),
          prob: j.daily.precipitation_probability_max[i] ?? 0,
        };
      });
      state.weatherOk = true;
    } catch { /* sin previsión: la app funciona igual */ }
  }
  function wxIcon(code) {
    if (code === 0) return "☀️";
    if (code <= 2) return "🌤️";
    if (code === 3) return "☁️";
    if (code === 45 || code === 48) return "🌫️";
    if (code >= 51 && code <= 57) return "🌦️";
    if ((code >= 61 && code <= 67) || (code >= 80 && code <= 82)) return "🌧️";
    if (code >= 71 && code <= 77) return "❄️";
    if (code >= 95) return "⛈️";
    return "🌤️";
  }
  function wxText(code) {
    if (code === 0) return "Despejado";
    if (code <= 2) return "Algunas nubes";
    if (code === 3) return "Nublado";
    if (code === 45 || code === 48) return "Niebla";
    if (code >= 51 && code <= 57) return "Llovizna";
    if ((code >= 61 && code <= 67) || (code >= 80 && code <= 82)) return "Lluvia";
    if (code >= 71 && code <= 77) return "Nieve";
    if (code >= 95) return "Tormenta";
    return "Variable";
  }

  // ---------- Render: edades ----------
  function renderAges() {
    const opts = [0, 1, 2, 3, 4, 5, 6];
    const html = opts.map((a) => {
      const on = state.ages.includes(a);
      const lab = a === 0 ? "bebé" : a === 6 ? "o más" : a === 1 ? "año" : "años";
      const txt = a === 6 ? "6+" : String(a);
      return `<button type="button" class="age" data-age="${a}" aria-pressed="${on}" aria-label="${a === 0 ? "Menos de 1 año" : a + " años"}">${txt}<small>${lab}</small></button>`;
    }).join("");
    document.querySelectorAll("[data-ages]").forEach((el) => { el.innerHTML = html; });
    const hint = $("#agesHint");
    if (!state.ages.length) hint.textContent = "Elige una o varias edades. Si tienes dos peques, marca las dos.";
    else {
      const s = state.ages.slice().sort((a, b) => a - b).map((a) => (a === 0 ? "bebé" : a === 6 ? "6+" : a)).join(" y ");
      hint.textContent = state.ages.length > 1 ? `Planes que valen para ${s} a la vez.` : `Planes que valen para ${s}${state.ages[0] > 0 && state.ages[0] < 6 ? " años" : ""}.`;
    }
  }

  // ---------- Render: calendario ----------
  function renderCalendar() {
    const m = state.month;
    const first = new Date(m.getFullYear(), m.getMonth(), 1);
    const daysIn = new Date(m.getFullYear(), m.getMonth() + 1, 0).getDate();
    const lead = isoDow(first) - 1;
    const canPrev = first > new Date(today.getFullYear(), today.getMonth(), 1);
    let cells = "";
    ["L", "M", "X", "J", "V", "S", "D"].forEach((d, i) => { cells += `<div class="cal-dow${i >= 5 ? " we" : ""}">${d}</div>`; });
    for (let i = 0; i < lead; i++) cells += `<div class="cal-day empty" aria-hidden="true"></div>`;
    for (let d = 1; d <= daysIn; d++) {
      const date = new Date(m.getFullYear(), m.getMonth(), d);
      const k = keyOf(date);
      const dow = isoDow(date);
      const past = k < TODAY;
      const cls = ["cal-day"];
      if (dow >= 6) cls.push("we");
      if (CFG.festivos[k]) cls.push("fest");
      if (k === TODAY) cls.push("today");
      if (past) cls.push("past");
      if (k === state.date) cls.push("sel");
      let dots = "";
      if (!past) {
        const n = state.plans.filter((p) => p.tipo === "temporal" && availableOn(p, k) && ageOk(p)).length;
        dots = n ? `<span class="dots">${"<i></i>".repeat(Math.min(3, n))}</span>` : `<span class="dots"></span>`;
      }
      const label = `${DIAS[dow - 1]} ${d} de ${MESES[m.getMonth()]}${CFG.festivos[k] ? ", festivo" : ""}`;
      cells += `<button type="button" class="${cls.join(" ")}" data-date="${k}" ${past ? "disabled" : ""} aria-label="${label}" aria-pressed="${k === state.date}">${d}${dots}</button>`;
    }
    $("#calendar").innerHTML = `
      <div class="cal-head">
        <h2>${MESES[m.getMonth()]} ${m.getFullYear()}</h2>
        <div class="cal-nav">
          <button type="button" class="icon-btn" data-cal="-1" ${canPrev ? "" : "disabled"} aria-label="Mes anterior">‹</button>
          <button type="button" class="icon-btn" data-cal="1" aria-label="Mes siguiente">›</button>
        </div>
      </div>
      <div class="cal-grid">${cells}</div>
      <div class="cal-foot">
        <span><i style="background:var(--park-tint)"></i>Fin de semana</span>
        <span><i style="background:var(--slide-tint)"></i>Festivo</span>
        <span><i style="background:var(--slide);border-radius:50%"></i>Hay planes de temporada</span>
      </div>`;
  }

  // ---------- Render: cabecera del día ----------
  function renderDayHead() {
    const d = fromKey(state.date);
    const dow = isoDow(d);
    const fest = CFG.festivos[state.date];
    const w = state.weather[state.date];
    const rainy = isRainy(state.date);
    const el = $("#dayHead");
    el.classList.toggle("rainy", rainy);
    let wx = "";
    if (w) {
      let tip = "";
      if (rainy) tip = "Pinta a lluvia: arriba te salen primero los planes a cubierto.";
      else if (w.max <= 10) tip = "Día fresco: abrigo y gorro si vais al aire libre.";
      else if (w.max >= 32) tip = "Mucho calor: mejor mañana temprano o a cubierto.";
      wx = `<div class="wx">
          <div class="wx-icon" aria-hidden="true">${wxIcon(w.code)}</div>
          <div><div class="wx-temp">${w.min}° / ${w.max}°</div>
          <div class="wx-detail">${wxText(w.code)} en Rivas, ${w.prob}% de probabilidad de lluvia</div></div>
        </div>${tip ? `<div class="wx-tip">${tip}</div>` : ""}`;
    } else {
      wx = `<div class="wx-tip">${state.weatherOk ? "La previsión del tiempo aparece cuando falten menos de 16 días." : "No se ha podido cargar la previsión del tiempo."}</div>`;
    }
    el.innerHTML = `
      <div class="day-name">${DIAS[dow - 1]} ${d.getDate()}</div>
      <div class="day-sub">${d.getDate()} de ${MESES[d.getMonth()]}${fest ? `, festivo: ${esc(fest)}` : ""}</div>
      ${wx}`;
  }

  // ---------- Render: filtros ----------
  function renderFilters() {
    const html = FILTERS.map((f) => `<button type="button" class="chip" data-filter="${f.id}" aria-pressed="${state.filters.has(f.id)}">${f.label}</button>`).join("");
    document.querySelectorAll("[data-filters]").forEach((el) => { el.innerHTML = html; });
  }

  // ---------- Render: tarjetas ----------
  function whenTag(p, k) {
    if (p.tipo !== "temporal") return "";
    if (p.fecha_inicio === p.fecha_fin) return `<span class="tag when">Solo este día</span>`;
    if (p.fecha_fin === k) return `<span class="tag when">Último día</span>`;
    return `<span class="tag when">Hasta el ${shortDate(p.fecha_fin)}</span>`;
  }
  function revLine(p) {
    const r = state.revByPlan[p.id] || [];
    if (!r.length) return "";
    const a = avg(p.id);
    const names = [...new Set(r.map((x) => x.autor.split(" ")[0]))];
    const who = names.length <= 2 ? names.join(" y ") : `${names.slice(0, 2).join(", ")} y ${names.length - 2} más`;
    return `<div class="card-rev"><span class="score">${a}</span><span>${esc(who)} ${names.length === 1 ? "ya ha ido" : "ya han ido"}</span></div>`;
  }
  function ageShort(p) {
    if (p.edad_min === 0 && p.edad_max >= 12) return "Todas las edades";
    if (p.edad_min === 0) return `Hasta ${p.edad_max} años`;
    return `${p.edad_min}–${p.edad_max}${p.edad_max >= 12 ? "+" : ""} años`;
  }
  function card(p, k) {
    const c = cat(p);
    const rainy = k && isRainy(k) && p.entorno === "exterior";
    const tags = [
      whenTag(p, k),
      p.gratis ? `<span class="tag free">Gratis</span>` : "",
      rainy ? `<span class="tag rain">Al aire libre</span>` : p.entorno === "interior" ? `<span class="tag">A cubierto</span>` : "",
      p.comer_jugando ? `<span class="tag play">${COMER[p.comer_jugando].tag}</span>` : "",
      p.carrito ? `<span class="tag stroller ${p.carrito}">${CARRITO[p.carrito].tag}</span>` : "",
      p.distancia_km ? `<span class="tag">${kmTxt(p.distancia_km)}</span>` : "",
      isRuta(p) ? "" : `<span class="tag">${ageShort(p)}</span>`,
      p.reserva ? `<span class="tag warn">Reserva</span>` : "",
    ].join("");
    return `<button type="button" class="card ${p.tipo}" data-plan="${p.id}">
      <span class="card-emoji" aria-hidden="true">${c.e}</span>
      <span class="card-main">
        <span class="card-title">${esc(p.titulo)}</span>
        <span class="card-place">${esc(p.municipio || "")}${p._km != null ? `, a ${p._km} km` : ""}</span>
        <span class="tags">${tags}</span>
        ${revLine(p)}
      </span>
    </button>`;
  }

  function renderLists() {
    const k = state.date;
    const all = plansFor(k);
    const temp = sortPlans(all.filter((p) => p.tipo === "temporal"), k);
    const perm = sortPlans(all.filter((p) => p.tipo === "permanente" && !isRuta(p) && !isComer(p)), k);
    const comer = sortPlans(all.filter((p) => p.tipo === "permanente" && isComer(p)), k);
    const comerShown = state.showAllComer ? comer : comer.slice(0, 10);
    const rutas = sortPlans(all.filter((p) => p.tipo === "permanente" && isRuta(p)), k);
    const LIMIT = 10;
    const permShown = state.showAllPerm ? perm : perm.slice(0, LIMIT);
    const rutasShown = state.showAllRutas ? rutas : rutas.slice(0, LIMIT);
    const noMatch = `<div class="empty"><strong>Nada con estos filtros</strong>Prueba a quitar algún filtro o a cambiar de edad.</div>`;
    $("#lists").innerHTML = `
      <div class="list-head"><h2>Solo estos días</h2><span class="count">${temp.length}</span></div>
      <p class="list-sub">Ferias, fiestas y espectáculos con fecha de fin.</p>
      <div class="cards">${temp.length ? temp.map((p) => card(p, k)).join("") : `<div class="empty"><strong>No hay planes de temporada este día</strong>Cada lunes se cargan los de los dos findes siguientes.</div>`}</div>
      <div class="list-head"><h2>Cualquier finde</h2><span class="count">${perm.length}</span></div>
      <p class="list-sub">Granjas, parques, museos, parques de bolas y sitios cubiertos que están siempre.</p>
      <div class="cards">${perm.length ? permShown.map((p) => card(p, k)).join("") : noMatch}</div>
      ${perm.length > LIMIT && !state.showAllPerm ? `<button type="button" class="btn more-btn" data-more="perm">Ver ${perm.length - LIMIT} más</button>` : ""}
      <div class="list-head"><h2>Comer con peques</h2><span class="count">${comer.length}</span></div>
      <p class="list-sub">Restaurantes donde los peques juegan mientras coméis: con monitores, parque de bolas, animales o espacio para correr.</p>
      <div class="cards">${comer.length ? comerShown.map((p) => card(p, k)).join("") : noMatch}</div>
      ${comer.length > 10 && !state.showAllComer ? `<button type="button" class="btn more-btn" data-more="comer">Ver ${comer.length - 10} más</button>` : ""}
      <div class="list-head"><h2>Rutas y paseos</h2><span class="count">${rutas.length}</span></div>
      <p class="list-sub">Con carrito, con carrito todoterreno o con mochila. Usa los filtros de arriba para ver solo las de carrito.</p>
      <div class="cards">${rutas.length ? rutasShown.map((p) => card(p, k)).join("") : noMatch}</div>
      ${rutas.length > LIMIT && !state.showAllRutas ? `<button type="button" class="btn more-btn" data-more="rutas">Ver ${rutas.length - LIMIT} más</button>` : ""}
      <p class="stale">Los horarios y precios pueden cambiar: confirma en la web antes de ir.</p>`;
  }

  function renderPlanes() {
    renderAges();
    renderCalendar();
    renderDayHead();
    renderFilters();
    renderLists();
  }

  // ---------- Ficha del plan ----------
  let lastFocus = null;
  function openPlan(id, fromHistory = false) {
    if (!state.loaded) return; // al terminar la carga se abre el plan del enlace
    const p = state.plans.find((x) => x.id === id || x.slug === id);
    if (!p) {
      toast("Ese plan ya no está disponible");
      if (location.hash) history.replaceState(null, "", location.pathname + location.search);
      return;
    }
    const wasOpen = !$("#sheet").hidden;
    if (!wasOpen) lastFocus = document.activeElement;
    if (map) map.closePopup();
    renderSheet(p);
    $("#sheetBackdrop").hidden = false;
    $("#sheet").hidden = false;
    $("#sheetBody").scrollTop = 0;
    document.body.style.overflow = "hidden";
    if (!wasOpen) $("#sheetClose").focus({ preventScroll: true });
    if (!fromHistory) {
      const url = `${location.pathname}${location.search}#plan=${p.slug}`;
      if (wasOpen && history.state && history.state.pfSheet) history.replaceState({ pfSheet: true }, "", url);
      else history.pushState({ pfSheet: true }, "", url);
    }
  }
  function hideSheet() {
    if ($("#sheet").hidden) return;
    $("#sheet").hidden = true;
    $("#sheetBackdrop").hidden = true;
    document.body.style.overflow = "";
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus({ preventScroll: true });
  }
  function closePlan() {
    if (history.state && history.state.pfSheet) { history.back(); return; } // popstate la cierra
    hideSheet();
    history.replaceState(null, "", location.pathname + location.search);
  }
  window.addEventListener("popstate", () => {
    const m = location.hash.match(/plan=([\w-]+)/);
    if (m) openPlan(m[1], true); else hideSheet();
  });
  window.addEventListener("hashchange", () => {
    const m = location.hash.match(/plan=([\w-]+)/);
    if (m) openPlan(m[1], true);
  });
  function dirUrl(p) {
    if (p.lat != null && !p.ubicacion_aprox) return `https://www.google.com/maps/dir/?api=1&destination=${p.lat},${p.lng}`;
    return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(`${p.titulo.split(":")[0]}, ${p.direccion || p.municipio || ""}`)}`;
  }
  function reviewHtml(r, withPlan) {
    const p = withPlan ? state.plans.find((x) => x.id === r.plan_id) : null;
    const mine = !!state.tokens[r.id];
    const initial = esc((r.autor.trim()[0] || "?").toUpperCase());
    const hue = [...r.autor].reduce((h, c) => (h * 31 + c.charCodeAt(0)) % 360, 7);
    const meta = [r.fecha_visita ? `Fue el ${shortDate(r.fecha_visita)}` : `Escrito el ${shortDate(r.creado.slice(0, 10))}`, r.edad_hijos ? `peques de ${esc(r.edad_hijos)}` : ""].filter(Boolean).join(", ");
    return `<article class="review">
      <div class="review-top">
        <span class="avatar" style="background:hsl(${hue} 45% 38%)" aria-hidden="true">${initial}</span>
        <div class="review-who"><strong>${esc(r.autor)}</strong><span>${meta}</span></div>
        <div class="review-score">${r.nota}<small>/10</small></div>
      </div>
      ${r.comentario ? `<p class="review-text">${esc(r.comentario)}</p>` : ""}
      ${p ? `<button type="button" class="review-plan" data-plan="${p.id}">${cat(p).e} ${esc(p.titulo)}</button>` : ""}
      ${mine ? `<button type="button" class="review-del" data-del="${r.id}">Borrar mi opinión</button>` : ""}
    </article>`;
  }
  function renderSheet(p) {
    const c = cat(p);
    const revs = state.revByPlan[p.id] || [];
    const a = avg(p.id);
    const when = p.tipo === "temporal"
      ? (p.fecha_inicio === p.fecha_fin ? `Solo el ${shortDate(p.fecha_inicio)}` : `Del ${shortDate(p.fecha_inicio)} al ${shortDate(p.fecha_fin)}`)
      : (p.dias_semana && p.dias_semana.length && p.dias_semana.length < 7 ? `Abre: ${diasTxt(p.dias_semana)}` : "Abierto todos los días");
    const whenDays = p.tipo === "temporal" && p.dias_semana && p.dias_semana.length ? `<br><small>Solo ${diasTxt(p.dias_semana)}</small>` : "";
    const env = { interior: "A cubierto", exterior: "Al aire libre", mixto: "Parte a cubierto, parte al aire libre" }[p.entorno];
    const ageTxt = p.edad_min === 0 ? `Desde bebés hasta ${p.edad_max}${p.edad_max >= 12 ? "+" : ""} años` : `De ${p.edad_min} a ${p.edad_max}${p.edad_max >= 12 ? "+" : ""} años`;
    const visitDefault = state.date <= TODAY ? state.date : TODAY;
    $("#sheetBody").innerHTML = `
      <div class="sheet-hero">
        <span class="card-emoji" aria-hidden="true">${c.e}</span>
        <div>
          <h2 id="sheetTitle">${esc(p.titulo)}</h2>
          <p class="sheet-place">${esc(p.municipio || "")}${p._km != null ? `, a ${p._km} km de ${CFG.origen.nombre.split("-")[0]}` : ""}</p>
        </div>
      </div>
      <div class="facts">
        <div class="fact"><span>🕑</span><span>${when}${whenDays}${p.horario ? `<br><small>${esc(p.horario)}</small>` : ""}</span></div>
        <div class="fact"><span>👶</span><span>${ageTxt}</span></div>
        <div class="fact"><span>💶</span><span>${esc(p.precio || (p.gratis ? "Gratis" : "Consultar"))}</span></div>
        <div class="fact"><span>${p.entorno === "exterior" ? "🌤️" : "🏠"}</span><span>${env}</span></div>
        ${p.comer_jugando ? `<div class="fact"><span>🍽️</span><span>${COMER[p.comer_jugando].txt}</span></div>` : ""}
        ${p.carrito ? `<div class="fact"><span>${p.carrito === "no" ? "🎒" : "🚼"}</span><span>${CARRITO[p.carrito].txt}</span></div>` : ""}
        ${p.distancia_km ? `<div class="fact"><span>🥾</span><span>Recorrido de ${kmTxt(p.distancia_km)}</span></div>` : ""}
        ${p.reserva ? `<div class="fact"><span>🎟️</span><span>Hay que reservar antes</span></div>` : ""}
        ${p.direccion ? `<div class="fact"><span>📍</span><span>${esc(p.direccion)}${p.ubicacion_aprox ? `<br><small>En el mapa la ubicación es aproximada</small>` : ""}</span></div>` : ""}
        ${a != null ? `<div class="fact"><span>⭐</span><span><strong>${a}</strong> de media con ${revs.length} ${revs.length === 1 ? "opinión" : "opiniones"} del grupo</span></div>` : ""}
      </div>
      ${p.descripcion ? `<p class="sheet-desc">${esc(p.descripcion)}</p>` : ""}
      <div class="actions">
        <a class="btn btn-primary" href="${dirUrl(p)}" target="_blank" rel="noopener">Cómo llegar</a>
        ${safeUrl(p.url) ? `<a class="btn" href="${esc(safeUrl(p.url))}" target="_blank" rel="noopener">Ver la web</a>`
          : `<a class="btn" href="https://www.google.com/search?q=${encodeURIComponent(p.titulo + " " + (p.municipio || ""))}" target="_blank" rel="noopener">Buscar en Google</a>`}
        <button type="button" class="btn btn-ghost" data-share="${p.slug}">Compartir</button>
        <button type="button" class="btn btn-ghost" data-showmap="${p.id}">Ver en el mapa</button>
      </div>

      <h3 class="section-title">Opiniones del grupo</h3>
      ${revs.length ? revs.map((r) => reviewHtml(r, false)).join("") : `<div class="empty"><strong>Nadie ha ido todavía</strong>Si vais, contad qué tal para el resto.</div>`}

      <h3 class="section-title">¿Habéis ido?</h3>
      <form class="rate-form" id="rateForm" data-plan="${p.id}" novalidate>
        <label id="lblNota">Nota del 0 al 10</label>
        <div class="scale" role="group" aria-labelledby="lblNota">
          ${Array.from({ length: 11 }, (_, i) => `<button type="button" data-nota="${i}" aria-pressed="false">${i}</button>`).join("")}
        </div>
        <label for="rComment">Comentario</label>
        <textarea id="rComment" maxlength="1000" placeholder="Qué os gustó, qué mejoraríais, consejos (aparcamiento, comida, cuánto tiempo estuvisteis…)"></textarea>
        <div class="row2">
          <div><label for="rDate">Fecha de la visita</label><input id="rDate" type="date" value="${visitDefault}" max="${TODAY}"></div>
          <div><label for="rAges">Edad de los peques</label><input id="rAges" maxlength="40" placeholder="Ej.: 1 y 2 años" value="${esc(state.ages.length ? state.ages.slice().sort((x, y) => x - y).map((x) => (x === 0 ? "bebé" : x)).join(" y ") + (state.ages.some((x) => x > 0) ? " años" : "") : "")}"></div>
        </div>
        <button type="submit" class="btn btn-primary">Publicar como ${esc(state.name || "…")}</button>
        <p class="note">Tu opinión la ven todos los que tienen el enlace.</p>
      </form>`;
  }

  async function submitReview(form) {
    const nota = form.dataset.nota;
    if (nota === undefined) { toast("Elige una nota del 0 al 10"); return; }
    const fv = $("#rDate").value;
    if (fv && fv > TODAY) { toast("La fecha de la visita no puede ser futura"); return; }
    if (!state.name) {
      await askName();
      if (!state.name) { toast("Pon tu nombre para publicar la opinión"); return; }
    }
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    const token = crypto.getRandomValues(new Uint32Array(4)).reduce((s, n) => s + n.toString(16).padStart(8, "0"), "");
    const row = {
      plan_id: form.dataset.plan,
      autor: state.name,
      nota: Number(nota),
      comentario: $("#rComment").value.trim() || null,
      fecha_visita: $("#rDate").value || null,
      edad_hijos: $("#rAges").value.trim() || null,
      token,
    };
    const { data, error } = await sb.from("pf_valoraciones").insert(row).select("id").single();
    btn.disabled = false;
    if (error) { toast("No se ha podido publicar. Revisa la conexión e inténtalo otra vez."); return; }
    state.tokens[data.id] = token;
    store.set("pf_tokens", state.tokens);
    await reloadReviews();
    const p = state.plans.find((x) => x.id === row.plan_id);
    renderSheet(p);
    refreshAll();
    toast("Opinión publicada");
  }
  async function deleteReview(id) {
    if (!confirm("¿Borrar tu opinión?")) return;
    const { data, error } = await sb.rpc("pf_borrar_valoracion", { p_id: id, p_token: state.tokens[id] });
    if (error || !data) { toast("No se ha podido borrar"); return; }
    delete state.tokens[id];
    store.set("pf_tokens", state.tokens);
    await reloadReviews();
    if (!$("#sheet").hidden) {
      const pid = $("#rateForm")?.dataset.plan;
      const p = state.plans.find((x) => x.id === pid);
      if (p) renderSheet(p);
    }
    refreshAll();
    toast("Opinión borrada");
  }

  // ---------- Nombre ----------
  function renderWho() {
    $("#whoBtn").textContent = state.name ? `Hola, ${state.name.split(" ")[0]}` : "¿Quién eres?";
  }
  function askName() {
    return new Promise((resolve) => {
      const dlg = $("#nameDialog");
      $("#nameInput").value = state.name;
      const done = () => { dlg.removeEventListener("close", done); resolve(); };
      dlg.addEventListener("close", done);
      dlg.showModal();
    });
  }
  $("#nameForm").addEventListener("submit", () => {
    const v = $("#nameInput").value.trim().replace(/\s+/g, " ");
    if (v.length >= 2) {
      state.name = v;
      store.set("pf_name", v);
      renderWho();
      const f = $("#rateForm");
      if (f) f.querySelector('button[type="submit"]').textContent = `Publicar como ${v}`;
    }
  });

  // ---------- Mapa ----------
  let map = null, layer = null;
  function initMap() {
    if (map) return;
    map = L.map("map", { zoomControl: false, attributionControl: true }).setView([CFG.origen.lat, CFG.origen.lng], 9);
    L.control.zoom({ position: "bottomright" }).addTo(map);
    map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
    L.marker([CFG.origen.lat, CFG.origen.lng], {
      icon: L.divIcon({ className: "", html: '<div class="pin-origin"></div>', iconSize: [18, 18], iconAnchor: [9, 9] }),
      title: "Rivas (punto de partida)",
    }).addTo(map).bindTooltip("Casa (Rivas)");
    layer = L.markerClusterGroup({
      showCoverageOnHover: false,
      maxClusterRadius: 44,
      spiderfyDistanceMultiplier: 1.6,
      iconCreateFunction: (c) => L.divIcon({
        className: "",
        html: `<div class="cluster"><span>${c.getChildCount()}</span></div>`,
        iconSize: [42, 42], iconAnchor: [21, 21],
      }),
    }).addTo(map);
  }
  function renderMap(focusId) {
    initMap();
    const k = state.date;
    const list = state.mapMode === "dia" ? plansFor(k) : state.plans.filter((p) => ageOk(p) && filtersOk(p));
    if (focusId && !list.some((p) => p.id === focusId)) {
      const fp = state.plans.find((p) => p.id === focusId);
      if (fp) list.push(fp);
    }
    $("#mapDay").textContent = state.mapMode === "dia" ? `${DIAS[isoDow(fromKey(k)) - 1]} ${fromKey(k).getDate()} de ${MESES[fromKey(k).getMonth()]}, ${list.length} planes` : `${list.length} planes`;
    layer.clearLayers();
    const bounds = [];
    let focusMarker = null;
    for (const p of list) {
      if (p.lat == null) continue;
      const revs = state.revByPlan[p.id] || [];
      const icon = L.divIcon({
        className: "",
        html: `<div class="pin ${p.tipo === "temporal" ? "temp" : "perm"}${revs.length ? " rev" : ""}"><span>${cat(p).e}</span></div>`,
        iconSize: [36, 36], iconAnchor: [18, 36], popupAnchor: [0, -34],
      });
      const a = avg(p.id);
      const revHtml = revs.slice(0, 2).map((r) => `<p><strong>${esc(r.autor)}</strong> ${r.nota}/10${r.comentario ? `: ${esc(r.comentario.length > 90 ? r.comentario.slice(0, 90) + "…" : r.comentario)}` : ""}</p>`).join("");
      const html = `<p class="pop-title">${esc(p.titulo)}</p>
        <p class="pop-place">${esc(p.municipio || "")}${p._km != null ? `, a ${p._km} km` : ""}${p.tipo === "temporal" ? `<br>Hasta el ${shortDate(p.fecha_fin)}` : ""}${p.ubicacion_aprox ? `<br><small>Ubicación aproximada</small>` : ""}</p>
        ${revs.length ? `<div class="pop-rev"><p><span class="score">${a}</span> ${revs.length} ${revs.length === 1 ? "opinión" : "opiniones"}</p>${revHtml}</div>` : ""}
        <button type="button" class="btn btn-primary pop-btn" data-plan="${p.id}">Ver plan</button>`;
      const mk = L.marker([p.lat, p.lng], { icon, title: p.titulo }).bindPopup(html, { maxWidth: 260 });
      mk.addTo(layer);
      bounds.push([p.lat, p.lng]);
      if (focusId && p.id === focusId) focusMarker = mk;
    }
    setTimeout(() => {
      map.invalidateSize();
      if (focusMarker) layer.zoomToShowLayer(focusMarker, () => focusMarker.openPopup());
      else if (bounds.length) map.fitBounds([[CFG.origen.lat, CFG.origen.lng], ...bounds], { padding: [30, 30], maxZoom: 12 });
    }, 50);
  }

  // ---------- Opiniones ----------
  function renderFeed() {
    const people = [...new Set(state.reviews.map((r) => r.autor))].sort((a, b) => a.localeCompare(b, "es"));
    if (state.feedPerson && !people.includes(state.feedPerson)) state.feedPerson = null;
    $("#peopleFilter").innerHTML = people.length
      ? [`<button type="button" class="chip" data-person="" aria-pressed="${!state.feedPerson}">Todos</button>`,
         ...people.map((n) => `<button type="button" class="chip" data-person="${esc(n)}" aria-pressed="${state.feedPerson === n}">${esc(n)}</button>`)].join("")
      : "";
    const list = state.reviews.filter((r) => !state.feedPerson || r.autor === state.feedPerson);
    $("#feed").innerHTML = list.length
      ? list.map((r) => reviewHtml(r, true)).join("")
      : `<div class="empty"><strong>Todavía no hay opiniones</strong>Abre un plan que hayáis hecho y puntúalo del 0 al 10.</div>`;
  }

  // ---------- Navegación ----------
  function setTab(t, focusId) {
    state.tab = t;
    document.querySelectorAll(".tabs button").forEach((b) => b.classList.toggle("on", b.dataset.tab === t));
    ["planes", "mapa", "opiniones"].forEach((v) => { $(`#view-${v}`).hidden = v !== t; });
    if (t === "mapa") renderMap(focusId);
    if (t === "opiniones") renderFeed();
    window.scrollTo({ top: 0 });
  }
  function refreshAll() {
    renderPlanes();
    if (state.tab === "mapa") renderMap();
    if (state.tab === "opiniones") renderFeed();
  }

  let toastT = null;
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toastT);
    toastT = setTimeout(() => t.classList.remove("show"), 2600);
  }

  // ---------- Eventos ----------
  document.addEventListener("click", (e) => {
    const t = e.target.closest("button, a");
    if (!t) return;
    if (t.dataset.age !== undefined) {
      const a = Number(t.dataset.age);
      state.ages = state.ages.includes(a) ? state.ages.filter((x) => x !== a) : [...state.ages, a];
      store.set("pf_ages", state.ages);
      state.showAllPerm = false; state.showAllRutas = false; state.showAllComer = false;
      renderPlanes();
      if (state.tab === "mapa") renderMap();
    } else if (t.dataset.date) {
      state.date = t.dataset.date;
      state.showAllPerm = false; state.showAllRutas = false; state.showAllComer = false;
      renderCalendar(); renderDayHead(); renderLists();
      $("#dayHead").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    } else if (t.dataset.cal) {
      state.month = new Date(state.month.getFullYear(), state.month.getMonth() + Number(t.dataset.cal), 1);
      renderCalendar();
    } else if (t.dataset.filter) {
      const f = t.dataset.filter;
      state.filters.has(f) ? state.filters.delete(f) : state.filters.add(f);
      renderFilters(); renderLists();
      if (state.tab === "mapa") renderMap();
    } else if (t.dataset.more !== undefined) {
      if (t.dataset.more === "rutas") state.showAllRutas = true;
      else if (t.dataset.more === "comer") state.showAllComer = true;
      else state.showAllPerm = true;
      renderLists();
    } else if (t.dataset.plan && !t.closest("form")) {
      openPlan(t.dataset.plan);
    } else if (t.dataset.tab) {
      setTab(t.dataset.tab);
    } else if (t.dataset.mapmode) {
      state.mapMode = t.dataset.mapmode;
      document.querySelectorAll("[data-mapmode]").forEach((b) => b.classList.toggle("on", b === t));
      renderMap();
    } else if (t.dataset.person !== undefined) {
      state.feedPerson = t.dataset.person || null; renderFeed();
    } else if (t.dataset.nota !== undefined) {
      const f = t.closest("form");
      f.dataset.nota = t.dataset.nota;
      f.querySelectorAll("[data-nota]").forEach((b) => b.setAttribute("aria-pressed", String(b === t)));
    } else if (t.dataset.del) {
      deleteReview(t.dataset.del);
    } else if (t.dataset.share) {
      const url = `${location.origin}${location.pathname}#plan=${t.dataset.share}`;
      const p = state.plans.find((x) => x.slug === t.dataset.share);
      if (navigator.share) navigator.share({ title: p?.titulo, text: `Mira este plan: ${p?.titulo}`, url }).catch(() => {});
      else if (navigator.clipboard) navigator.clipboard.writeText(url).then(() => toast("Enlace copiado"), () => prompt("Copia el enlace:", url));
      else prompt("Copia el enlace:", url);
    } else if (t.dataset.showmap) {
      const id = t.dataset.showmap;
      closePlan();
      state.mapMode = "todos";
      document.querySelectorAll("[data-mapmode]").forEach((b) => b.classList.toggle("on", b.dataset.mapmode === "todos"));
      setTab("mapa", id);
    }
  });
  document.addEventListener("submit", (e) => {
    if (e.target.id === "rateForm") { e.preventDefault(); submitReview(e.target); }
  });
  $("#sheetClose").addEventListener("click", closePlan);
  $("#sheetBackdrop").addEventListener("click", closePlan);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !$("#sheet").hidden && !$("#nameDialog").open) closePlan(); });
  $("#whoBtn").addEventListener("click", () => askName());
  // Deslizar hacia abajo para cerrar la ficha
  (() => {
    const sheet = $("#sheet"); let y0 = null;
    sheet.addEventListener("touchstart", (e) => { if ($("#sheetBody").scrollTop <= 0) y0 = e.touches[0].clientY; }, { passive: true });
    sheet.addEventListener("touchend", (e) => { if (y0 != null && e.changedTouches[0].clientY - y0 > 90) closePlan(); y0 = null; }, { passive: true });
  })();

  // ---------- Arranque ----------
  async function start() {
    renderWho();
    $("#lists").innerHTML = `<div class="loading">Cargando planes…</div>`;
    renderAges();
    try {
      await Promise.all([loadData(), loadWeather()]);
    } catch (err) {
      $("#lists").innerHTML = `<div class="empty"><strong>No se han podido cargar los planes</strong>Comprueba la conexión y recarga la página.</div>`;
      console.error(err);
      return;
    }
    state.loaded = true;
    refreshAll();
    const m = location.hash.match(/plan=([\w-]+)/);
    if (m) {
      // Deja una entrada "sin ficha" debajo para que Atrás cierre la ficha
      history.replaceState(null, "", location.pathname + location.search);
      openPlan(m[1]);
    }
  }
  start();
})();
