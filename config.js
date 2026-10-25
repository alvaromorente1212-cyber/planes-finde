// Configuración pública (la clave publicable de Supabase es segura en el navegador; la seguridad la dan las políticas RLS)
window.PF_CONFIG = {
  supabaseUrl: "https://xefnuudfxyisaogadnmp.supabase.co",
  supabaseKey: "sb_publishable_aZZqdtt-x6gjEmF1kxW0ng_lDATB4I7",
  // Punto de partida para distancias y previsión del tiempo
  origen: { nombre: "Rivas-Vaciamadrid", lat: 40.3580, lng: -3.5320 },
  // Festivos (Comunidad de Madrid + Madrid capital). Se tratan como domingo a efectos de horarios.
  festivos: {
    "2026-11-02": "Todos los Santos (trasladado)",
    "2026-11-09": "La Almudena (Madrid capital)",
    "2026-12-07": "Constitución (trasladado)",
    "2026-12-08": "Inmaculada",
    "2026-12-25": "Navidad",
    "2027-01-01": "Año Nuevo",
    "2027-01-06": "Reyes",
  },
};
