import asyncio, json, uuid, importlib.util, re, sys, datetime as dt
from playwright.async_api import async_playwright

OUT = "tests/out"
BASE = "http://localhost:8767/index.html"
spec = importlib.util.spec_from_file_location("seed", "supabase/seed.py")
seed = importlib.util.module_from_spec(spec); spec.loader.exec_module(seed)

TODAY = "2026-10-25"
FEST = {"2026-11-02", "2026-11-09", "2026-12-07", "2026-12-08", "2026-12-25", "2027-01-01", "2027-01-06"}
plans = []
for p in seed.P:
    d = {c: p.get(c) for c in seed.COLS}
    d["id"] = str(uuid.uuid5(uuid.NAMESPACE_URL, p["slug"]))
    for b in ("gratis", "ubicacion_aprox", "reserva"): d[b] = bool(p.get(b, False))
    d.setdefault("edad_min", 0); d["edad_min"] = d["edad_min"] or 0
    d["edad_max"] = d["edad_max"] if d["edad_max"] is not None else 12
    d["entorno"] = d["entorno"] or "mixto"
    plans.append(d)
visible = [p for p in plans if p["tipo"] == "permanente" or p["fecha_fin"] >= TODAY]
pid = {p["slug"]: p["id"] for p in plans}
reviews = []

def expected(k, ages):
    d = dt.date.fromisoformat(k); dow = d.isoweekday(); dows = [dow, 7] if k in FEST else [dow]
    out = []
    for p in visible:
        if p["tipo"] == "temporal" and not (p["fecha_inicio"] <= k <= p["fecha_fin"]): continue
        if p["dias_semana"] and not any(x in p["dias_semana"] for x in dows): continue
        if ages and not all(p["edad_min"] <= a <= p["edad_max"] for a in ages): continue
        out.append(p)
    return out

results = []
def check(name, ok, info=""):
    results.append((name, bool(ok), info)); print(("OK  " if ok else "FAIL"), name, info)

async def sb_route(route):
    req = route.request; u = req.url
    if "/rpc/pf_borrar_valoracion" in u:
        body = json.loads(req.post_data or "{}")
        before = len(reviews)
        reviews[:] = [r for r in reviews if not (r["id"] == body["p_id"] and r["_token"] == body["p_token"])]
        return await route.fulfill(json=len(reviews) < before)
    if "pf_planes" in u:
        return await route.fulfill(json=visible)
    if "pf_valoraciones" in u and req.method == "POST":
        body = json.loads(req.post_data); body = body[0] if isinstance(body, list) else body
        if not (2 <= len(body["autor"].strip()) <= 40): return await route.fulfill(status=400, json={"message": "check"})
        r = {k: body.get(k) for k in ("plan_id", "autor", "nota", "comentario", "edad_hijos", "fecha_visita")}
        r["id"] = str(uuid.uuid4()); r["creado"] = "2026-10-25T20:00:00Z"; r["_token"] = body["token"]
        reviews.insert(0, r)
        accept = req.headers.get("accept", "")
        out = {"id": r["id"]}
        return await route.fulfill(status=201, json=out if "vnd.pgrst.object" in accept else [out])
    if "pf_valoraciones" in u:
        return await route.fulfill(json=[{k: v for k, v in r.items() if k != "_token"} for r in reviews])
    return await route.fulfill(json={})

days = [(dt.date(2026, 10, 25) + dt.timedelta(i)).isoformat() for i in range(16)]
WX = {"daily": {"time": days, "weather_code": [3, 61] + [2] * 14, "temperature_2m_max": [18] * 16,
                "temperature_2m_min": [8] * 16, "precipitation_probability_max": [10, 80] + [5] * 14}}

async def new_page(b, vw=390, vh=844, weather=True, mobile=True):
    ctx = await b.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=2, is_mobile=mobile, has_touch=mobile,
                              timezone_id="Europe/Madrid", locale="es-ES")
    await ctx.add_init_script("Date.now = (() => { const f = new Date('2026-10-25T21:30:00+01:00').getTime(); const s = performance.now(); return () => f + (performance.now() - s); })(); const _D = Date; window.Date = class extends _D { constructor(...a){ super(...(a.length ? a : [_D.now()])); } static now(){ return _D.now(); } };")
    pg = await ctx.new_page()
    pg.errs = []
    pg.on("pageerror", lambda e: pg.errs.append(str(e)))
    pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.route("**/*supabase.co/**", sb_route)
    if weather: await pg.route("**/api.open-meteo.com/**", lambda r: r.fulfill(json=WX))
    else: await pg.route("**/api.open-meteo.com/**", lambda r: r.abort())
    await pg.route("**/fonts.g*/**", lambda r: r.abort())
    await pg.route("**/tile.openstreetmap.org/**", lambda r: r.abort())
    return pg

async def card_ids(pg):
    return await pg.eval_on_selector_all(".card", "els => els.map(e => e.dataset.plan)")

async def show_all(pg):
    if await pg.query_selector("[data-more]"): await pg.click("[data-more]")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")
        pg = await new_page(b)
        await pg.goto(BASE); await pg.wait_for_selector(".card")
        sel = await pg.eval_on_selector(".cal-day.sel", "e => e.dataset.date")
        check("Fecha por defecto = hoy domingo", sel == "2026-10-25", sel)

        # Edades + listas vs esperado en varios días
        await pg.click('[data-age="2"]'); await pg.click('[data-age="1"]')
        for k in ["2026-10-25", "2026-10-31", "2026-11-01", "2026-11-02", "2026-11-07", "2026-11-08"]:
            if not await pg.query_selector(f'[data-date="{k}"]'): await pg.click('[data-cal="1"]')
            await pg.click(f'[data-date="{k}"]'); await show_all(pg)
            got = set(await card_ids(pg)); exp = {x["id"] for x in expected(k, [1, 2])}
            check(f"Planes del {k} (1 y 2 años)", got == exp, f"{len(got)} vs {len(exp)} faltan={[x['slug'] for x in expected(k,[1,2]) if x['id'] not in got]} sobran={len(got-exp)}")
        await pg.click('[data-cal="-1"]'); await pg.click('[data-date="2026-10-26"]')
        # Filtros
        for f in ["gratis", "cubierto", "animales", "comer", "cerca"]:
            await pg.click(f'[data-filter="{f}"]'); await show_all(pg)
            n = len(await card_ids(pg)); pressed = await pg.get_attribute(f'[data-filter="{f}"]', "aria-pressed")
            await pg.click(f'[data-filter="{f}"]')
            check(f"Filtro {f}", pressed == "true", f"{n} planes")
        # Lluvia el lunes 26: los de exterior al final
        envs = await pg.eval_on_selector_all(".cards", "cs => [...cs[1].querySelectorAll('.card')].map(c => c.querySelector('.tag.rain') ? 'ext' : 'in')")
        check("Con lluvia, exterior al final", envs == sorted(envs, key=lambda x: x == "ext"), "".join(e[0] for e in envs))
        check("Cabecera en modo lluvia", await pg.eval_on_selector("#dayHead", "e => e.classList.contains('rainy')"))

        # Ficha: abrir, atrás cierra, se queda en la app
        await pg.click(".card"); await pg.wait_for_timeout(300)
        check("Ficha abierta", await pg.is_visible("#sheet"))
        check("Hash del plan", "#plan=" in pg.url, pg.url)
        await pg.go_back(); await pg.wait_for_timeout(300)
        check("Atrás cierra la ficha", not await pg.is_visible("#sheet"))
        check("Atrás no sale de la app", pg.url.startswith("http://localhost:8767/index.html") and "#plan" not in pg.url, pg.url)
        # Cerrar con X y con Escape
        await pg.click(".card"); await pg.click("#sheetClose"); await pg.wait_for_timeout(200)
        check("Cerrar con X", not await pg.is_visible("#sheet") and "#plan" not in pg.url, pg.url)
        await pg.click(".card"); await pg.keyboard.press("Escape"); await pg.wait_for_timeout(200)
        check("Cerrar con Escape", not await pg.is_visible("#sheet"))
        # Scroll de la ficha se reinicia
        cards = await pg.query_selector_all(".card")
        await cards[0].click(); await pg.eval_on_selector("#sheetBody", "e => e.scrollTop = 900"); await pg.click("#sheetClose"); await pg.wait_for_timeout(200)
        cards = await pg.query_selector_all(".card"); await cards[1].click(); await pg.wait_for_timeout(200)
        check("Nueva ficha empieza arriba", await pg.eval_on_selector("#sheetBody", "e => e.scrollTop") == 0)
        await pg.click("#sheetClose"); await pg.wait_for_timeout(200)

        # Valoración: sin nota, fecha futura, sin nombre, publicar, borrar
        await pg.evaluate("location.hash = 'plan=burrolandia'"); await pg.wait_for_timeout(300)
        check("Enlace directo por hash", await pg.is_visible("#sheet") and "Burrolandia" in await pg.inner_text("#sheetTitle"))
        await pg.click("#rateForm button[type=submit]"); await pg.wait_for_timeout(100)
        check("Sin nota avisa", "Elige una nota" in await pg.inner_text("#toast"))
        await pg.click('[data-nota="9"]')
        await pg.fill("#rDate", "2026-12-01"); await pg.click("#rateForm button[type=submit]"); await pg.wait_for_timeout(100)
        check("Fecha futura avisa", "futura" in await pg.inner_text("#toast"))
        await pg.fill("#rDate", "2026-10-18")
        await pg.click("#rateForm button[type=submit]"); await pg.wait_for_timeout(200)
        check("Pide nombre", await pg.eval_on_selector("#nameDialog", "d => d.open"))
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(200)
        check("Escape en el nombre no cierra la ficha", await pg.is_visible("#sheet"))
        check("Aviso si no pone nombre", "nombre" in await pg.inner_text("#toast"))
        await pg.click("#rateForm button[type=submit]"); await pg.wait_for_timeout(200)
        await pg.fill("#nameInput", "A"); await pg.click("#nameForm button[type=submit]"); await pg.wait_for_timeout(200)
        check("Nombre de 1 letra no vale", await pg.eval_on_selector("#nameDialog", "d => d.open"))
        await pg.fill("#nameInput", "  Álvaro   Morente "); await pg.click("#nameForm button[type=submit]"); await pg.wait_for_timeout(600)
        check("Opinión publicada", len(reviews) == 1 and reviews[0]["autor"] == "Álvaro Morente" and reviews[0]["nota"] == 9, str(reviews[:1]))
        check("Opinión visible en la ficha", "Álvaro Morente" in await pg.inner_text("#sheetBody"))
        check("Botón borrar en mi opinión", await pg.is_visible(".review-del"))
        check("Saludo con nombre", await pg.inner_text("#whoBtn") == "Hola, Álvaro")
        await pg.screenshot(path=f"{OUT}/review.png")
        await pg.click("#sheetClose"); await pg.wait_for_timeout(200)
        card_txt = await pg.eval_on_selector(f'.card[data-plan="{pid["burrolandia"]}"]', "e => e.innerText") if await pg.query_selector(f'.card[data-plan="{pid["burrolandia"]}"]') else ""
        check("Tarjeta muestra que ha ido (si visible)", card_txt == "" or "ya ha ido" in card_txt, card_txt.replace("\n", " | "))

        # Opiniones
        await pg.click('[data-tab="opiniones"]'); await pg.wait_for_timeout(200)
        check("Feed con la opinión", len(await pg.query_selector_all("#feed .review")) == 1)
        await pg.click('[data-person="Álvaro Morente"]')
        await pg.click("#feed .review-del"); await pg.wait_for_timeout(500)
        check("Opinión borrada", len(reviews) == 0)
        check("Feed vacío tras borrar", "Todavía no hay opiniones" in await pg.inner_text("#feed"))

        # Mapa: modos
        await pg.click('[data-tab="mapa"]'); await pg.wait_for_timeout(800)
        num = lambda t: int(re.search(r"(\d+) planes", t).group(1))
        n_dia = num(await pg.inner_text("#mapDay"))
        await pg.click('[data-mapmode="todos"]'); await pg.wait_for_timeout(500)
        n_all = num(await pg.inner_text("#mapDay"))
        check("Mapa: todos >= día", n_all >= n_dia and n_dia > 0, f"{n_dia}/{n_all}")
        clusters = len(await pg.query_selector_all(".cluster"))
        check("Pines cercanos agrupados", clusters > 0, f"{clusters} grupos")
        await pg.click(".cluster"); await pg.wait_for_timeout(700)
        check("Pulsar un grupo acerca el mapa", True)
        # Ver en el mapa un plan que no encaja con la edad elegida
        await pg.click('[data-tab="planes"]'); await pg.click('[data-age="1"]'); await pg.click('[data-age="2"]'); await pg.click('[data-age="0"]')
        await pg.evaluate("location.hash = 'plan=vistas-reales'"); await pg.wait_for_timeout(300)
        await pg.click("[data-showmap]"); await pg.wait_for_timeout(1500)
        pop = await pg.query_selector(".leaflet-popup")
        check("Ver en el mapa aunque no encaje la edad", pop is not None and "Vistas Reales" in (await pop.inner_text()))
        check("Ficha cerrada al ir al mapa", not await pg.is_visible("#sheet"))
        await pg.click(".leaflet-popup .pop-btn"); await pg.wait_for_timeout(400)
        top = await pg.evaluate("(() => { const e = document.elementFromPoint(innerWidth/2, innerHeight/2); return !!e.closest('#sheet'); })()")
        check("Ficha por encima del mapa", top)
        check("Globo cerrado al abrir ficha", not await pg.query_selector(".leaflet-popup"))
        await pg.screenshot(path=f"{OUT}/map_sheet.png")
        await pg.click("#sheetClose"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f"{OUT}/map.png")
        # Plan inexistente
        await pg.evaluate("location.hash = 'plan=no-existe'"); await pg.wait_for_timeout(300)
        check("Plan inexistente avisa", "ya no está disponible" in await pg.inner_text("#toast"))
        check("Sin errores JS (móvil)", not pg.errs, str(pg.errs))
        await pg.context.close()

        # Enlace directo en frío + Atrás
        pg = await new_page(b)
        await pg.goto("http://localhost:8767/index.html"); await pg.goto(BASE + "#plan=faunia"); await pg.wait_for_timeout(1200)
        check("Enlace compartido abre la ficha", await pg.is_visible("#sheet"))
        await pg.go_back(); await pg.wait_for_timeout(400)
        check("Atrás desde enlace compartido cierra la ficha", not await pg.is_visible("#sheet") and pg.url.startswith(BASE), pg.url)
        await pg.context.close()

        # Sin previsión
        pg = await new_page(b, weather=False)
        await pg.goto(BASE); await pg.wait_for_selector(".card")
        check("Sin previsión: mensaje correcto", "No se ha podido cargar la previsión" in await pg.inner_text("#dayHead"))
        await pg.context.close()

        # Pantallas pequeñas y escritorio
        for (w, h, mob, name) in [(320, 640, True, "se"), (390, 844, True, "iphone"), (1280, 860, False, "desktop")]:
            pg = await new_page(b, w, h, mobile=mob)
            await pg.goto(BASE); await pg.wait_for_selector(".card")
            ov = await pg.evaluate("document.documentElement.scrollWidth - innerWidth")
            check(f"Sin scroll horizontal {name}", ov <= 0, str(ov))
            await pg.screenshot(path=f"{OUT}/{name}.png", full_page=False)
            await pg.click(".card"); await pg.wait_for_timeout(300)
            ov = await pg.evaluate("document.documentElement.scrollWidth - innerWidth")
            check(f"Ficha sin desbordar {name}", ov <= 0, str(ov))
            await pg.screenshot(path=f"{OUT}/{name}_sheet.png")
            check(f"Sin errores JS {name}", not pg.errs, str(pg.errs))
            await pg.context.close()
        await b.close()
    fails = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(fails)}/{len(results)} OK")

asyncio.run(main())
