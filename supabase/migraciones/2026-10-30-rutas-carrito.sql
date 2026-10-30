-- Rutas y paseos: categoría 'ruta', si se puede ir con carrito y distancia del recorrido
alter table public.pf_planes add column if not exists carrito text, add column if not exists distancia_km numeric(5,1);
alter table public.pf_planes add constraint pf_carrito check (carrito is null or carrito in ('si','dificil','no'));
alter table public.pf_planes add constraint pf_distancia check (distancia_km is null or (distancia_km > 0 and distancia_km <= 50));
alter table public.pf_planes drop constraint pf_categoria;
alter table public.pf_planes add constraint pf_categoria check (categoria = any (array['granja','zoo','restaurante','parque','naturaleza','museo','cubierto','espectaculo','fiesta','feria','taller','evento','ruta','otros']));
