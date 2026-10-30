-- Restaurantes donde los peques juegan mientras se come
alter table public.pf_planes add column if not exists comer_jugando text;
alter table public.pf_planes add constraint pf_comer_jugando check (comer_jugando is null or comer_jugando in ('monitores','parque','animales','espacio_libre'));
