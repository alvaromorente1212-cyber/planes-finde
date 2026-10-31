-- Categoría navidad
alter table public.pf_planes drop constraint pf_categoria;
alter table public.pf_planes add constraint pf_categoria check (categoria = any (array['granja','zoo','restaurante','parque','naturaleza','museo','cubierto','espectaculo','fiesta','feria','taller','evento','ruta','navidad','otros']));
