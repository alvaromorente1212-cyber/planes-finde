"""Genera supabase/seed.sql con la carga inicial de planes (upsert por slug).
Uso: python3 supabase/seed.py > supabase/seed.sql
"""
import json

FINDE = [5, 6, 7]  # viernes, sábado, domingo
SD = [6, 7]
MAR_DOM = [2, 3, 4, 5, 6, 7]

P = []


def plan(**k):
    k.setdefault("tipo", "permanente")
    P.append(k)


# ---------------- PERMANENTES ----------------
plan(slug="vistas-reales", titulo="Vistas Reales: comer mientras los peques están en la granja",
     descripcion="Finca de más de 10 hectáreas con restaurante. Los niños dan de comer a los animales, ven vuelo de aves rapaces y hacen juegos de naturaleza con monitores mientras los padres comen. Pases: Explorador (11:00-14:45, 15 €/persona desde 2 años, comida aparte), Mediodía (13:00-17:30) y Aventura (11:00-17:30). Bautismo hípico 8 €.",
     categoria="restaurante", dias_semana=SD, horario="Pases de 11:00 a 17:30; restaurante turnos 13:00 y 15:00",
     edad_min=2, edad_max=12, entorno="exterior", precio="Pase Explorador 15 €; menores de 2 gratis; menú aparte",
     municipio="Soto del Real", direccion="Cañada de los Rancajales s/n, Soto del Real", lat=40.7395, lng=-3.7650,
     url="https://www.vistasreales.es/", fuente="okdiario / elblogdeceleste", ubicacion_aprox=True, reserva=True)

plan(slug="burrolandia", titulo="Burrolandia: dar de comer a burros rescatados",
     descripcion="Refugio de burros rescatados donde los niños pueden acariciarlos y darles de comer. Solo domingos, gratis con reserva (las plazas vuelan: se abren la noche del domingo anterior).",
     categoria="granja", dias_semana=[7], horario="Domingos 10:00-12:00 y 12:30-14:30",
     edad_min=0, edad_max=12, entorno="exterior", precio="Gratis (donativo recomendado)", gratis=True,
     municipio="Tres Cantos", direccion="Camino de la Moraleja 147, Tres Cantos", lat=40.5795, lng=-3.6830,
     url="https://burrolandiaoficial.es/", fuente="Time Out", ubicacion_aprox=True, reserva=True)

plan(slug="torreon-el-pardo", titulo="El Torreón de El Pardo: restaurante con parque y granjita",
     descripcion="Restaurante de El Pardo con parque infantil y una pequeña granja de animales. Buen plan de comida familiar combinado con paseo por el monte de El Pardo.",
     categoria="restaurante", horario="Horario de restaurante", edad_min=0, edad_max=10, entorno="mixto",
     precio="Precio de restaurante", municipio="Madrid (El Pardo)", direccion="Pista del Cristo de El Pardo 3, Madrid",
     lat=40.5245, lng=-3.7735, url=None, fuente="myfamilytime / gastroranking", ubicacion_aprox=True)

plan(slug="granja-de-los-cuentos-fuenlabrada", titulo="La Granja de los Cuentos",
     descripcion="Mañana de sábado en una granja urbana con animales, actividades y desayuno casero incluido. Sesión de 4 horas.",
     categoria="granja", dias_semana=[6], horario="Sábados 10:00-14:00",
     edad_min=1, edad_max=10, entorno="mixto", precio="Niños 25 €, adultos 27 €, bebés <12 meses gratis",
     municipio="Fuenlabrada", direccion="C/ Villa Claudia 2, Fuenlabrada", lat=40.2870, lng=-3.8085,
     url=None, fuente="Que Hacer con los Niños", ubicacion_aprox=True, reserva=True)

plan(slug="granja-esgaravita", titulo="Granja Escuela La Esgaravita: sábados en familia",
     descripcion="Granja escuela con 'sábados en familia': ordeñar, dar de comer a los animales y talleres de huerto.",
     categoria="granja", dias_semana=[6], horario="Sábados con reserva previa",
     edad_min=1, edad_max=10, entorno="exterior", precio="15 €/persona (desde 1 año)",
     municipio="Alcalá de Henares", direccion="La Esgaravita, Alcalá de Henares", lat=40.5260, lng=-3.3450,
     url=None, fuente="Picuco", ubicacion_aprox=True, reserva=True)

plan(slug="granja-escuela-el-alamo", titulo="Granja Escuela El Álamo",
     descripcion="Granja escuela con animales, huerto y talleres. Visitas de día completo para familias con reserva.",
     categoria="granja", dias_semana=SD, horario="Aprox. 10:00-17:00 según actividad",
     edad_min=2, edad_max=12, entorno="exterior", precio="Consultar",
     municipio="Brunete", direccion="Paseo Boadilla del Monte km 14,5, Brunete", lat=40.4030, lng=-3.9780,
     url=None, fuente="Que Hacer con los Niños", ubicacion_aprox=True, reserva=True)

plan(slug="canada-real-peralejo", titulo="Centro de Naturaleza Cañada Real",
     descripcion="Centro de recuperación de fauna con animales autóctonos (lobos, ciervos, rapaces, granja). Visitable todo el año salvo con calor extremo.",
     categoria="granja", dias_semana=SD, horario="Fines de semana con reserva",
     edad_min=2, edad_max=12, entorno="exterior", precio="Consultar",
     municipio="Peralejo (El Escorial)", direccion="Peralejo, El Escorial", lat=40.5560, lng=-4.1190,
     url=None, fuente="Picuco", ubicacion_aprox=True, reserva=True)

plan(slug="faunia", titulo="Faunia",
     descripcion="Parque de naturaleza con ecosistemas cubiertos (jungla, polos, nocturno) y granja. Muy buena opción para días de lluvia gracias a las zonas interiores.",
     categoria="zoo", dias_semana=SD, horario="Oct-nov: fines de semana; consultar calendario",
     edad_min=0, edad_max=12, entorno="mixto", precio="Desde ~25 €; menores de 3 gratis",
     municipio="Madrid (Valdebernardo)", direccion="Av. de las Comunidades 28, Madrid", lat=40.3989, lng=-3.6141,
     url="https://www.faunia.es/", fuente="esMadrid")

plan(slug="zoo-aquarium-madrid", titulo="Zoo Aquarium de Madrid",
     descripcion="Zoo y acuario en la Casa de Campo, con delfinario y exhibición de aves. Abierto todos los días.",
     categoria="zoo", horario="Todos los días", edad_min=0, edad_max=12, entorno="mixto",
     precio="Desde ~30 €; menores de 3 gratis", municipio="Madrid (Casa de Campo)",
     direccion="Casa de Campo s/n, Madrid", lat=40.4093, lng=-3.7613, url="https://www.zoomadrid.com/", fuente="esMadrid")

plan(slug="safari-madrid", titulo="Safari Madrid",
     descripcion="Safari en coche entre animales en semilibertad, con exhibiciones de aves y reptiles. Ideal para los más pequeños porque se ve casi todo desde el coche.",
     categoria="zoo", horario="Todos los días", edad_min=0, edad_max=12, entorno="exterior",
     precio="Consultar", municipio="Aldea del Fresno", direccion="Finca El Venado, Aldea del Fresno",
     lat=40.3310, lng=-4.2040, url="https://www.safarimadrid.es/", fuente="conocido", ubicacion_aprox=True)

plan(slug="atlantis-aquarium", titulo="Atlantis Aquarium (Xanadú)",
     descripcion="Acuario cubierto en el centro comercial Xanadú: túnel de tiburones y pozas táctiles. Plan perfecto para días de lluvia.",
     categoria="cubierto", horario="Todos los días", edad_min=0, edad_max=12, entorno="interior",
     precio="Consultar", municipio="Arroyomolinos", direccion="C.C. Xanadú, Arroyomolinos",
     lat=40.2963, lng=-3.9350, url=None, fuente="esMadrid")

plan(slug="parque-europa", titulo="Parque Europa",
     descripcion="Parque con réplicas de monumentos europeos, lago, barcas y zona infantil 'Diversión en la Granja'. Entrada gratis; atracciones ~3 €/viaje.",
     categoria="parque", horario="Todos los días", edad_min=0, edad_max=12, entorno="exterior",
     precio="Gratis (atracciones de pago)", gratis=True, municipio="Torrejón de Ardoz",
     direccion="Paseo de la Ermita, Torrejón de Ardoz", lat=40.4646, lng=-3.4521,
     url=None, fuente="planenfamilia")

plan(slug="museo-ferrocarril", titulo="Museo del Ferrocarril",
     descripcion="Locomotoras y vagones reales en la antigua estación de Delicias. Se puede subir a algunos trenes y hay tren en miniatura. Cubierto.",
     categoria="museo", dias_semana=MAR_DOM, horario="Martes a domingo", edad_min=1, edad_max=12, entorno="interior",
     precio="Entrada económica; consultar", municipio="Madrid (Delicias)", direccion="Paseo de las Delicias 61, Madrid",
     lat=40.3966, lng=-3.6936, url="https://www.museodelferrocarril.org/", fuente="esMadrid")

plan(slug="cosmocaixa", titulo="CosmoCaixa Alcobendas",
     descripcion="Museo de ciencia con espacios para los más pequeños y exposiciones interactivas. Cubierto.",
     categoria="museo", dias_semana=MAR_DOM, horario="Martes a domingo", edad_min=2, edad_max=12, entorno="interior",
     precio="Consultar", municipio="Alcobendas", direccion="C/ Pintor Murillo 2, Alcobendas",
     lat=40.5367, lng=-3.6420, url=None, fuente="conocido", ubicacion_aprox=True)

plan(slug="ciencias-naturales", titulo="Museo Nacional de Ciencias Naturales",
     descripcion="Esqueletos de dinosaurios, animales y minerales. Les encanta a partir de los 3 años.",
     categoria="museo", dias_semana=MAR_DOM, horario="Martes a domingo", edad_min=3, edad_max=12, entorno="interior",
     precio="Consultar", municipio="Madrid", direccion="C/ José Gutiérrez Abascal 2, Madrid",
     lat=40.4407, lng=-3.6898, url="https://www.mncn.csic.es/", fuente="planenfamilia")

plan(slug="planetario-madrid", titulo="Planetario de Madrid",
     descripcion="Proyecciones bajo la cúpula, algunas pensadas para los más pequeños. Dentro del Parque Tierno Galván.",
     categoria="museo", dias_semana=MAR_DOM, horario="Martes a domingo", edad_min=3, edad_max=12, entorno="interior",
     precio="Económico", municipio="Madrid (Arganzuela)", direccion="Parque Tierno Galván, Madrid",
     lat=40.3943, lng=-3.6867, url=None, fuente="esMadrid")

plan(slug="marpa-alcala", titulo="Museo Arqueológico Regional (MARPA)",
     descripcion="Mamuts, dientes de sable y arqueología, gratis. Se combina muy bien con un paseo por el centro de Alcalá.",
     categoria="museo", dias_semana=MAR_DOM, horario="Martes a domingo", edad_min=3, edad_max=12, entorno="interior",
     precio="Gratis", gratis=True, municipio="Alcalá de Henares", direccion="Plaza de las Bernardas s/n, Alcalá de Henares",
     lat=40.4810, lng=-3.3640, url=None, fuente="planenfamilia")

plan(slug="tren-juan-carlos-i", titulo="Tren gratuito del Parque Juan Carlos I",
     descripcion="Trenecito gratuito de 30 minutos entre esculturas gigantes, el lago y el olivar. Parque enorme para correr y montar en bici.",
     categoria="parque", dias_semana=SD, horario="Fines de semana y festivos",
     edad_min=0, edad_max=12, entorno="exterior", precio="Gratis", gratis=True, municipio="Madrid (Barajas)",
     direccion="Av. de Logroño / Glorieta S. Juan Carlos I, Madrid", lat=40.4626, lng=-3.6094, url=None, fuente="planenfamilia")

plan(slug="capricho", titulo="Parque El Capricho",
     descripcion="Jardín histórico con laberinto, estanque con patos y cisnes. Solo abre sábados, domingos y festivos.",
     categoria="naturaleza", dias_semana=SD, horario="Sábados, domingos y festivos",
     edad_min=0, edad_max=12, entorno="exterior", precio="Gratis", gratis=True, municipio="Madrid (Barajas)",
     direccion="Paseo de la Alameda de Osuna 25, Madrid", lat=40.4580, lng=-3.6005, url=None, fuente="conocido")

plan(slug="madrid-rio-parques", titulo="Parques infantiles de Madrid Río",
     descripcion="17 áreas de juego con toboganes gigantes, lianas y puentes colgantes a lo largo del Manzanares.",
     categoria="parque", edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Madrid", direccion="Paseo de la Ermita del Santo, Madrid", lat=40.4110, lng=-3.7230,
     url=None, fuente="elDiario.es")

plan(slug="parque-la-gavia", titulo="Parque La Gavia y Mundos Mágicos de Vallecas",
     descripcion="Cohete, toboganes en la colina, tirolinas, camas elásticas e instrumentos musicales. Cerca están Mundárbol, Maremundo y Mundaire, con zonas para los más pequeños.",
     categoria="parque", edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Madrid (Ensanche de Vallecas)", direccion="Av. del Mayorazgo 26, Madrid", lat=40.3705, lng=-3.6150,
     url=None, fuente="elDiario.es", ubicacion_aprox=True)

plan(slug="parque-felipe-vi", titulo="Parque Forestal Felipe VI (Valdebebas)",
     descripcion="Toboganes largos en la ladera, zona de juegos de agua (tornillos de Arquímedes, norias) y mucho espacio.",
     categoria="parque", edad_min=2, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Madrid (Valdebebas)", direccion="Av. de las Fuerzas Armadas 11, Madrid", lat=40.4800, lng=-3.6180,
     url=None, fuente="elDiario.es", ubicacion_aprox=True)

plan(slug="parque-benedicto-xvi", titulo="Nuevo parque Benedicto XVI",
     descripcion="Parque nuevo (abierto en octubre de 2026) con más de 2.000 m² de juegos infantiles, tirolina, toboganes y camas elásticas.",
     categoria="parque", edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Madrid (San Blas-Canillejas)", direccion="Av. de Luis Aragonés con glorieta de Carlos Llamas, Madrid",
     lat=40.4395, lng=-3.5990, url=None, fuente="madrid.es", ubicacion_aprox=True)

plan(slug="ciudad-de-los-ninos-tres-cantos", titulo="Ciudad de los Niños (Tres Cantos)",
     descripcion="Parque infantil gratuito de 12.000 m² con torre de redes, toboganes y fuente interactiva. Junto al Parque Central de Tres Cantos.",
     categoria="parque", edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Tres Cantos", direccion="Barrio Nuevo Tres Cantos, Tres Cantos", lat=40.6110, lng=-3.7130,
     url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="parque-paris-las-rozas", titulo="Parque París (Las Rozas)",
     descripcion="Avión gigante para trepar, colchonetas hinchables integradas en el suelo y tirolinas.",
     categoria="parque", edad_min=2, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Las Rozas", direccion="Parque París, Las Rozas de Madrid", lat=40.5005, lng=-3.8770,
     url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="parque-osa-menor-leganes", titulo="Parque Infantil de la Osa Menor (Leganés)",
     descripcion="Castillo de madera con tirolina, toboganes y camas elásticas.",
     categoria="parque", edad_min=2, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Leganés", direccion="Leganés", lat=40.3330, lng=-3.7720, url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="hormiguero-atomico", titulo="Parque El Hormiguero Atómico (Alcobendas)",
     descripcion="Hormiguero gigante para trepar y explorar.",
     categoria="parque", edad_min=3, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Alcobendas", direccion="Alcobendas", lat=40.5440, lng=-3.6340, url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="parque-tempranales", titulo="Parque infantil Tempranales (San Sebastián de los Reyes)",
     descripcion="Parque con camas elásticas y colchonetas hinchables integradas en el suelo.",
     categoria="parque", edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="San Sebastián de los Reyes", direccion="Av. de Sierra Nevada 8", lat=40.5560, lng=-3.6420,
     url=None, fuente="decide.madrid.es", ubicacion_aprox=True)

plan(slug="animales-gigantes-majadahonda", titulo="Parque de los Animales Gigantes (Majadahonda)",
     descripcion="Toboganes dentro de figuras gigantes de madera: león, búho y gorrión.",
     categoria="parque", edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Majadahonda", direccion="Parque Cerro del Aire, Majadahonda", lat=40.4590, lng=-3.8790,
     url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="dragon-usera", titulo="Parque del Dragón (Usera)",
     descripcion="Dragón gigante de 19 metros con redes, tobogán y rocódromo.",
     categoria="parque", edad_min=2, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Madrid (Usera)", direccion="Usera, Madrid", lat=40.3800, lng=-3.7080, url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="lago-loranca", titulo="Parque del Lago de Loranca",
     descripcion="Lago con patos, tortugas y pavos reales en libertad. Paseo tranquilo con carrito.",
     categoria="naturaleza", edad_min=0, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Fuenlabrada", direccion="Loranca, Fuenlabrada", lat=40.2980, lng=-3.8330, url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="senda-magica-arroyomolinos", titulo="La Senda Mágica (Arroyomolinos)",
     descripcion="Paseo de 1,5 km por el bosque buscando gnomos y hadas de madera escondidos.",
     categoria="naturaleza", edad_min=2, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Arroyomolinos", direccion="Arroyomolinos", lat=40.2720, lng=-3.9130, url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="bosque-finlandes", titulo="Bosque Finlandés (Rascafría)",
     descripcion="Paseo llano y corto alrededor de una laguna entre pinos, apto para carrito. Muy bonito en otoño.",
     categoria="naturaleza", edad_min=0, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Rascafría", direccion="Rascafría", lat=40.8890, lng=-3.8790, url=None, fuente="conocido", ubicacion_aprox=True)

plan(slug="laguna-campillo", titulo="Laguna de El Campillo (Parque Regional del Sureste)",
     descripcion="Al lado de Rivas: paseo junto a la laguna para ver patos y aves, con centro de educación ambiental.",
     categoria="naturaleza", edad_min=0, edad_max=12, entorno="exterior", precio="Gratis", gratis=True,
     municipio="Rivas-Vaciamadrid", direccion="Laguna de El Campillo, Rivas-Vaciamadrid", lat=40.3165, lng=-3.4990,
     url=None, fuente="conocido", ubicacion_aprox=True)

plan(slug="lego-fan-factory-rivas", titulo="LEGO Fan Factory (C.C. H2O)",
     descripcion="Ludoteca de LEGO con zona DUPLO para los pequeños y una hora diaria gratis. Cubierto.",
     categoria="cubierto", edad_min=1, edad_max=12, entorno="interior", precio="Una hora gratis al día", gratis=True,
     municipio="Rivas-Vaciamadrid", direccion="C.C. H2O, Rivas-Vaciamadrid", lat=40.3480, lng=-3.5390,
     url=None, fuente="planenfamilia", ubicacion_aprox=True)

plan(slug="lamucca-plaza-espana", titulo="Lamucca Plaza de España (con parque cubierto)",
     descripcion="Restaurante con zona de juegos interior en la planta baja. Buena opción de comida con lluvia.",
     categoria="restaurante", edad_min=1, edad_max=8, entorno="interior", precio="Precio de restaurante",
     municipio="Madrid (centro)", direccion="Plaza de España, Madrid", lat=40.4234, lng=-3.7128, url=None, fuente="myfamilytime", ubicacion_aprox=True)

plan(slug="la-burguesita-boadilla", titulo="La Burguesita (Boadilla)",
     descripcion="Restaurante con piscina de bolas y ludoteca con cristalera para ver a los niños mientras comes.",
     categoria="restaurante", edad_min=1, edad_max=10, entorno="interior", precio="Precio de restaurante",
     municipio="Boadilla del Monte", direccion="Boadilla del Monte", lat=40.4050, lng=-3.8760, url=None, fuente="myfamilytime", ubicacion_aprox=True)

plan(slug="cambio-guardia-palacio-real", titulo="Cambio de guardia en el Palacio Real",
     descripcion="Relevo con guardias a caballo y a pie. Los caballos suelen encantar a los peques.",
     categoria="evento", dias_semana=[3, 6], horario="Miércoles y sábados por la mañana",
     edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True, municipio="Madrid (centro)",
     direccion="Palacio Real, Madrid", lat=40.4179, lng=-3.7143, url=None, fuente="esMadrid")

plan(slug="jardines-aranjuez", titulo="Jardines del Príncipe y Chiquitren (Aranjuez)",
     descripcion="Jardines enormes junto al Tajo con patos y pavos reales, y trenecito turístico por la ciudad.",
     categoria="naturaleza", edad_min=0, edad_max=12, entorno="exterior", precio="Jardines gratis",
     gratis=True, municipio="Aranjuez", direccion="Jardín del Príncipe, Aranjuez", lat=40.0378, lng=-3.5960,
     url=None, fuente="conocido", ubicacion_aprox=True)

plan(slug="micropolix", titulo="Micropolix",
     descripcion="Ciudad a escala donde los niños 'trabajan' de bomberos, médicos, etc. Mejor a partir de 3-4 años. Cubierto.",
     categoria="cubierto", dias_semana=SD, horario="Fines de semana; consultar", edad_min=3, edad_max=12,
     entorno="interior", precio="Consultar", municipio="San Sebastián de los Reyes",
     direccion="Av. de la Sierra, San Sebastián de los Reyes", lat=40.5490, lng=-3.6230, url=None, fuente="conocido", ubicacion_aprox=True)

# ---------------- TEMPORALES ----------------
def temp(**k):
    k["tipo"] = "temporal"
    P.append(k)


temp(slug="halloween-faunia-2026", titulo="Halloween en Faunia",
     descripcion="Faunia se viste de Halloween con actividades, caramelos y decoración temática.",
     categoria="fiesta", fecha_inicio="2026-10-03", fecha_fin="2026-11-02", dias_semana=[6, 7],
     horario="Sábados, domingos y festivos 12:00-19:00", edad_min=1, edad_max=12, entorno="mixto",
     precio="Entrada de Faunia", municipio="Madrid (Valdebernardo)", direccion="Av. de las Comunidades 28, Madrid",
     lat=40.3989, lng=-3.6141, url="https://www.faunia.es/", fuente="dondego")

temp(slug="monstrudisco-san-martin-vega-2026", titulo="Monstrudisco y concurso infantil de disfraces",
     descripcion="Fiesta de Halloween al aire libre con concurso de disfraces por edades (1-4, 5-8, 9-12) y premios. Muy cerca de Rivas.",
     categoria="fiesta", fecha_inicio="2026-10-31", fecha_fin="2026-10-31", horario="Sábado 31 a las 18:00",
     edad_min=1, edad_max=12, entorno="exterior", precio="Gratis", gratis=True, municipio="San Martín de la Vega",
     direccion="Plaza de la Constitución, San Martín de la Vega", lat=40.2085, lng=-3.5715,
     url="https://ayto-smv.es/2026/10/15/halloween-llega-a-san-martin-cargado-de-planes-para-todas-las-edades/", fuente="Madrid Información", ubicacion_aprox=True)

temp(slug="halloween-divertilandia-sanse-2026", titulo="Halloween para bebés en Divertilandia",
     descripcion="Sesiones de Halloween para niños de 9 meses a 3 años con un adulto. Reserva prioritaria para empadronados; plazas sobrantes desde el 29 de octubre.",
     categoria="fiesta", fecha_inicio="2026-10-31", fecha_fin="2026-10-31", horario="Sesiones 17:00, 18:00 y 19:00",
     edad_min=0, edad_max=3, entorno="interior", precio="Con reserva", municipio="San Sebastián de los Reyes",
     direccion="Centro de Actividades para la Infancia Divertilandia, San Sebastián de los Reyes", lat=40.5470, lng=-3.6260,
     url="https://transparencia.ssreyes.org/es/web/la-plaza-de-sanse/-/pintacaras-recetas-y-sustos-para-vivir-un-halloween-de-miedo",
     fuente="Madrid Información", ubicacion_aprox=True, reserva=True)

temp(slug="halloween-villanueva-canada-2026", titulo="Fiesta de Halloween en Santiago Apóstol",
     descripcion="Fiesta familiar de Halloween en pabellón cubierto.",
     categoria="fiesta", fecha_inicio="2026-10-31", fecha_fin="2026-10-31", horario="Sábado 31 a las 17:00",
     edad_min=2, edad_max=12, entorno="interior", precio="4 €", municipio="Villanueva de la Cañada",
     direccion="Complejo Deportivo Santiago Apóstol, Villanueva de la Cañada", lat=40.4470, lng=-3.9990,
     url="https://www.ayto-villacanada.es/agenda-y-actividades/fiesta-halloween/", fuente="Madrid Información", ubicacion_aprox=True)

temp(slug="monstruos-reciclados-boadilla-2026", titulo="Monstruos reciclados: taller familiar de Halloween",
     descripcion="Taller familiar de decoración de Halloween con materiales reciclados.",
     categoria="taller", fecha_inicio="2026-10-31", fecha_fin="2026-10-31", horario="Sábado 31, 10:30-12:30",
     edad_min=3, edad_max=12, entorno="interior", precio="Inscripción previa", municipio="Boadilla del Monte",
     direccion="Aula Medioambiental, Av. Adolfo Suárez 35, Boadilla del Monte", lat=40.4100, lng=-3.8900,
     url="https://aulanaturalezaboadilla.es/events/taller-de-decoracion-de-halloween-con-elementos-reciclados-2/",
     fuente="Madrid Información", ubicacion_aprox=True, reserva=True)

temp(slug="monstruos-a-la-obra-alcala-2026", titulo="Monstruos a la obra: crea tus criaturas de Halloween",
     descripcion="Taller gratuito para niños de 3 a 5 años, con inscripción y plazas limitadas.",
     categoria="taller", fecha_inicio="2026-11-01", fecha_fin="2026-11-01", horario="Domingo 1, 12:00-13:00",
     edad_min=3, edad_max=5, entorno="interior", precio="Gratis con inscripción", gratis=True, municipio="Alcalá de Henares",
     direccion="Junta Municipal Distrito II, Av. Reyes Católicos 9, Alcalá de Henares", lat=40.4900, lng=-3.3540,
     url="https://inscripciones.ayto-alcaladehenares.es/eventos/categoria/talleres-octubre-noviembre-y-diciembre-2026-distrito-ii/dia/2026-11-01/",
     fuente="Madrid Información", ubicacion_aprox=True, reserva=True)

temp(slug="tren-de-la-fresa-otono-2026", titulo="Tren de la Fresa",
     descripcion="Tren histórico de época del Museo del Ferrocarril a Aranjuez, con azafatas que reparten fresones. Últimos fines de semana de la temporada de otoño.",
     categoria="evento", fecha_inicio="2026-10-03", fecha_fin="2026-11-08", dias_semana=[6, 7],
     horario="Sábados y domingos, salida 10:00", edad_min=2, edad_max=12, entorno="mixto", precio="Consultar",
     municipio="Madrid → Aranjuez", direccion="Museo del Ferrocarril, Paseo de las Delicias 61, Madrid",
     lat=40.3966, lng=-3.6936, url="https://www.museodelferrocarril.org/", fuente="dondego", reserva=True)

temp(slug="pumpkin-patch-aranjuez-2026", titulo="Pumpkin Patch en La Huerta de Aranjuez",
     descripcion="Campo de calabazas para elegir la tuya, laberinto de maíz, carreras de sacos y paseo en tractor.",
     categoria="fiesta", fecha_inicio="2026-10-03", fecha_fin="2026-11-07", dias_semana=[6, 7],
     horario="Fines de semana; consultar", edad_min=1, edad_max=12, entorno="exterior", precio="Consultar",
     municipio="Aranjuez", direccion="La Huerta de Aranjuez, Aranjuez", lat=40.0420, lng=-3.5800,
     url=None, fuente="dondego", ubicacion_aprox=True, reserva=True)

temp(slug="halloween-parque-atracciones-2026", titulo="Halloween en el Parque de Atracciones",
     descripcion="Temporada de Halloween con zona infantil y decoración temática (los pasajes del terror no son para pequeños).",
     categoria="fiesta", fecha_inicio="2026-09-26", fecha_fin="2026-11-01", horario="Consultar calendario",
     edad_min=2, edad_max=12, entorno="exterior", precio="Entrada del parque", municipio="Madrid (Casa de Campo)",
     direccion="Casa de Campo, Madrid", lat=40.4113, lng=-3.7500, url="https://www.parquedeatracciones.es/", fuente="esMadrid")

temp(slug="feria-artesania-otono-2026", titulo="Feria de Artesanía de Otoño",
     descripcion="Casetas de artesanos en el Paseo de Recoletos. Paseo tranquilo con carrito.",
     categoria="feria", fecha_inicio="2026-10-19", fecha_fin="2026-11-02", horario="Todos los días",
     edad_min=0, edad_max=12, entorno="exterior", precio="Gratis", gratis=True, municipio="Madrid (centro)",
     direccion="Paseo de Recoletos, Madrid", lat=40.4220, lng=-3.6925, url=None, fuente="Agenda Medieval")

temp(slug="halloween-canciones-sanpol-2026", titulo="Halloween, canciones de miedo y risa",
     descripcion="Espectáculo musical familiar de Halloween.",
     categoria="espectaculo", fecha_inicio="2026-10-31", fecha_fin="2026-11-01", horario="12:00",
     edad_min=2, edad_max=10, entorno="interior", precio="Consultar", municipio="Madrid",
     direccion="Teatro Sanpol, Plaza San Pol de Mar 1, Madrid", lat=40.4365, lng=-3.7230,
     url="https://dondego.es/madrid/event/espectaculo-halloween-canciones-de-miedo-y-risa/", fuente="dondego", ubicacion_aprox=True)

temp(slug="mago-de-oz-sanpol-2026", titulo="Musical El Mago de Oz",
     descripcion="Musical familiar en el Teatro Sanpol.",
     categoria="espectaculo", fecha_inicio="2026-10-31", fecha_fin="2026-11-09", dias_semana=[6, 7],
     horario="17:30 (el lunes 2 también a las 12:00)", edad_min=3, edad_max=12, entorno="interior", precio="Consultar",
     municipio="Madrid", direccion="Teatro Sanpol, Madrid", lat=40.4365, lng=-3.7230,
     url="https://dondego.es/madrid/event/espectculo-el-mago-de-oz/", fuente="dondego", ubicacion_aprox=True)

temp(slug="una-rana-en-el-mar-2026", titulo="Una rana en el mar (para bebés)",
     descripcion="Espectáculo para primera infancia, apto desde 0 años. Última función.",
     categoria="espectaculo", fecha_inicio="2026-11-01", fecha_fin="2026-11-01", horario="Domingo 11:15",
     edad_min=0, edad_max=4, entorno="interior", precio="Consultar", municipio="Madrid",
     direccion="Teatros Luchana, C/ Luchana 38, Madrid", lat=40.4310, lng=-3.6990,
     url="https://dondego.es/madrid/event/espectculo-una-rana-en-el-mar/", fuente="dondego", ubicacion_aprox=True)

temp(slug="tres-cerditos-soho-2026", titulo="Los tres cerditos",
     descripcion="Teatro infantil de La Curvatura Teatro, los domingos.",
     categoria="espectaculo", fecha_inicio="2026-09-20", fecha_fin="2026-11-29", dias_semana=[7], horario="Domingos",
     edad_min=2, edad_max=8, entorno="interior", precio="Consultar", municipio="Madrid",
     direccion="Teatro Soho Madrid", lat=40.4280, lng=-3.6640,
     url="https://www.esmadrid.com/agenda/tres-cerditos-teatro-soho-madrid", fuente="esMadrid", ubicacion_aprox=True)

temp(slug="101-dalmatas-show-2026", titulo="101 Dálmatas, The Show",
     descripcion="Musical familiar en el Gran Teatro CaixaBank Príncipe Pío.",
     categoria="espectaculo", fecha_inicio="2026-10-18", fecha_fin="2026-12-27", dias_semana=[6, 7], horario="Fines de semana",
     edad_min=3, edad_max=12, entorno="interior", precio="Consultar", municipio="Madrid",
     direccion="Gran Teatro CaixaBank Príncipe Pío, Madrid", lat=40.4210, lng=-3.7200,
     url="https://www.esmadrid.com/agenda/101-dalmatas-show-gran-teatro-caixabank-principe-pio", fuente="esMadrid", ubicacion_aprox=True)

temp(slug="pica-pica-halloween-2026", titulo="Pica Pica: Operación Halloween",
     descripcion="Concierto-espectáculo de Pica Pica con canciones para los más pequeños.",
     categoria="espectaculo", fecha_inicio="2026-10-31", fecha_fin="2026-11-07", dias_semana=[6, 7], horario="Consultar sesiones",
     edad_min=1, edad_max=7, entorno="interior", precio="Consultar", municipio="Madrid (Gran Vía)",
     direccion="Teatro Capitol Gran Vía, Madrid", lat=40.4205, lng=-3.7065,
     url="https://www.esmadrid.com/agenda/pica-pica-operacion-halloween-capitol-gran-via", fuente="esMadrid")

temp(slug="circo-del-agua-2026", titulo="Gran Circo del Agua (Circo Alegría)",
     descripcion="Circo con espectáculo acuático bajo carpa, junto al Palacio de Hielo.",
     categoria="espectaculo", fecha_inicio="2026-10-09", fecha_fin="2027-02-07", dias_semana=[5, 6, 7], horario="Viernes a domingo",
     edad_min=2, edad_max=12, entorno="interior", precio="Consultar", municipio="Madrid (Hortaleza)",
     direccion="Carpa junto al C.C. Palacio de Hielo, Madrid", lat=40.4505, lng=-3.6380,
     url="https://www.esmadrid.com/agenda/circo-alegria-gran-circo-agua-gran-carpa-junto-palacio-hielo", fuente="esMadrid", ubicacion_aprox=True)

temp(slug="valle-de-la-navidad-2026", titulo="El Valle de la Navidad",
     descripcion="Experiencia navideña inmersiva: misión con pruebas y personajes para convertirse en ayudantes de Papá Noel, con encuentro con Papá Noel o el Rey Melchor. Dura 2-2,5 h.",
     categoria="fiesta", fecha_inicio="2026-11-06", fecha_fin="2027-01-05",
     horario="Pases 10:00, 12:00, 16:00 y 18:00 según día", edad_min=2, edad_max=12, entorno="mixto",
     precio="Desde 20 € (L-J) / 23 € (V-D y festivos)", municipio="Bustarviejo",
     direccion="Albergue Valle Abedules, M-610 km 15, Bustarviejo", lat=40.8350, lng=-3.7260,
     url="https://vallenavidad.com/", fuente="Madrid Happy People", ubicacion_aprox=True, reserva=True)

temp(slug="voa-rivas-2026", titulo="¡Voa! (Gata Japonesa) — teatro familiar en Rivas",
     descripcion="Espectáculo para todos los públicos de la temporada familiar de otoño de Rivas.",
     categoria="espectaculo", fecha_inicio="2026-11-08", fecha_fin="2026-11-08", horario="Domingo 8 a las 18:00",
     edad_min=2, edad_max=12, entorno="interior", precio="Niños 3 €, adultos 6 €", municipio="Rivas-Vaciamadrid",
     direccion="La Casa+Grande, Rivas-Vaciamadrid", lat=40.3560, lng=-3.5250,
     url="https://entradas.rivasciudad.es/", fuente="El Resurgir de Madrid", ubicacion_aprox=True)

temp(slug="bruja-rechinadientes-rivas-2026", titulo="La bruja rechinadientes — teatro familiar en Rivas",
     descripcion="Temporada familiar de otoño de Rivas.",
     categoria="espectaculo", fecha_inicio="2026-11-15", fecha_fin="2026-11-15", horario="Domingo 15 a las 18:00",
     edad_min=3, edad_max=12, entorno="interior", precio="Niños 3 €, adultos 6 €", municipio="Rivas-Vaciamadrid",
     direccion="Auditorio Pilar Bardem, Rivas-Vaciamadrid", lat=40.3540, lng=-3.5320,
     url="https://entradas.rivasciudad.es/", fuente="El Resurgir de Madrid", ubicacion_aprox=True)

temp(slug="spin-oz-infanta-isabel-2026", titulo="Spin Oz",
     descripcion="Espectáculo familiar los domingos.",
     categoria="espectaculo", fecha_inicio="2026-11-08", fecha_fin="2026-12-13", dias_semana=[7], horario="Domingos",
     edad_min=3, edad_max=12, entorno="interior", precio="Consultar", municipio="Madrid",
     direccion="Teatro Infanta Isabel, C/ Barquillo 24, Madrid", lat=40.4205, lng=-3.6965,
     url="https://www.esmadrid.com/agenda/spin-oz-teatro-infanta-isabel", fuente="esMadrid", ubicacion_aprox=True)

temp(slug="mercado-renacentista-humanes-2026", titulo="Mercado Renacentista de Humanes",
     descripcion="Mercado de época con puestos, artesanía y animación.",
     categoria="feria", fecha_inicio="2026-11-13", fecha_fin="2026-11-15", horario="Viernes a domingo",
     edad_min=0, edad_max=12, entorno="exterior", precio="Gratis", gratis=True, municipio="Humanes de Madrid",
     direccion="Plaza de la Constitución, Humanes de Madrid", lat=40.2550, lng=-3.8290,
     url="https://agendamedieval.com/madrid/", fuente="Agenda Medieval", ubicacion_aprox=True)


COLS = ["slug", "titulo", "descripcion", "tipo", "categoria", "fecha_inicio", "fecha_fin", "dias_semana", "horario",
        "edad_min", "edad_max", "entorno", "precio", "gratis", "municipio", "direccion", "lat", "lng", "url", "fuente",
        "ubicacion_aprox", "reserva"]


def lit(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, list):
        return "array[" + ",".join(str(int(x)) for x in v) + "]::int[]"
    return "'" + str(v).replace("'", "''") + "'"


def sql():
    rows = []
    for p in P:
        d = {c: p.get(c) for c in COLS}
        d["gratis"] = bool(p.get("gratis", False))
        d["ubicacion_aprox"] = bool(p.get("ubicacion_aprox", False))
        d["reserva"] = bool(p.get("reserva", False))
        rows.append("(" + ", ".join(lit(d[c]) for c in COLS) + ")")
    upd = ", ".join(f"{c} = excluded.{c}" for c in COLS if c != "slug")
    return (f"insert into public.pf_planes ({', '.join(COLS)}) values\n" + ",\n".join(rows) +
            f"\non conflict (slug) do update set {upd}, actualizado = now();\n")


if __name__ == "__main__":
    print(sql())
