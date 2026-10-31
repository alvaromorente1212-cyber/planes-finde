# Planes Finde

Web para encontrar planes de fin de semana con peques (0-6 años) desde Rivas-Vaciamadrid: Madrid y alrededores, hasta ~1h30 en coche.

- **Planes**: eliges la edad (o varias, si tienes más de un peque), el día en el calendario y ves los planes de ese día separados en *Solo estos días* (con fecha de fin) y *Cualquier finde* (siempre disponibles). Muestra la previsión del tiempo en Rivas y, si llueve, sube los planes a cubierto.
- **Mapa**: todos los planes en un mapa (OpenStreetMap), con las opiniones del grupo.
- **Opiniones**: cada amigo se identifica con su nombre y puntúa del 0 al 10 los planes que ha hecho.

## Cómo funciona

| Pieza | Dónde |
|---|---|
| Web estática | GitHub Pages (`index.html`, `app.js`, `styles.css`) |
| Datos | Supabase, proyecto `tablero-equipo`, tablas `pf_planes` y `pf_valoraciones` |
| Tiempo | Open-Meteo (gratis, sin clave), hasta 16 días vista |
| Carga semanal | Tarea programada de Claude cada lunes por la mañana (ver `docs/tarea-semanal.md`) |

Librerías servidas desde `vendor/`: Leaflet 1.9.4 y supabase-js 2.

## Datos

- `pf_planes`: `tipo` = `temporal` (con `fecha_inicio`/`fecha_fin`) o `permanente`. `dias_semana` (1=lunes … 7=domingo; null = todos). Los festivos de `config.js` cuentan como domingo. `edad_min`/`edad_max`, `entorno` (interior/exterior/mixto), `ubicacion_aprox` si las coordenadas son aproximadas. Las rutas (`categoria` = `ruta`) llevan `carrito` (`si` / `dificil` / `no`) y `distancia_km`; la app las muestra en su propia sección *Rutas y paseos* y tiene filtros *Rutas y paseos*, *Con carrito* y *Sin carrito*. Los sitios para comer llevan `comer_jugando` (`monitores` / `parque` / `animales` / `espacio_libre`) y salen en la sección *Comer con peques*, con filtros *Comer mientras juegan* y *Con monitores*. El mapa tiene sus propios selectores de edad y filtros (compartidos con la pestaña Planes) y una fila de *Temáticas* para mostrar solo las categorías elegidas. Categoría `navidad` para belenes, mercadillos, alumbrados, parques navideños y cabalgatas.
- `pf_valoraciones`: nombre, nota 0-10, comentario. Cualquiera con el enlace puede leer y escribir; cada persona puede borrar solo lo suyo desde el mismo navegador (token guardado en local).
- `supabase/seed.py` genera la carga inicial (`seed.sql`) con upsert por `slug`.
