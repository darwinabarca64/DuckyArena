# 🎨 AGENTE DIRECTOR DE ARTE & CHARACTER DESIGNER — DUCKY MULTIVERSE

## 1. ESPECIFICACIÓN TÉCNICA DEL CANVAS UNIVERSAL
- Resolución de Exportación: 512 x 512 px por capa en formato WebP transparente (lossless / alpha habilitado).
- Peso Máximo por Activo: Menor a 25 KB por capa para garantizar descarga instantánea en dispositivos móviles.
- Puntos de Anclaje Biomecánico del Pato:
  * Centro geométrico de la cabeza: (256, 160) px.
  * Línea de ojos y pico: (256, 185) px.
  * Centro del torso / pecho: (256, 320) px.
  * Base de apoyo / patas: (256, 450) px.

## 2. ORDEN ESTRICTO DE CAPAS (Z-INDEX)
- Capa 0 (z-index: 10): Cuerpo base del pato (renderizado completo sin ropa ni accesorios).
- Capa 1 (z-index: 20): Ropa, armaduras y túnicas de la civilización elegida (cuello y torso).
- Capa 2 (z-index: 30): Expresión facial (ojos, cejas y detalle de pico).
- Capa 3 (z-index: 40): Sombreros, yelmos, coronas y accesorios de cabeza.

## 3. CATÁLOGO CROMÁTICO INCLUSIVO (CUERPOS BASE)
1. body_yellow: Amarillo canario clásico (#FBBF24) con pico naranja (#F97316).
2. body_brown: Pardo chocolate silvestre (#78350F) con pico canela (#B45309).
3. body_black: Negro ónix carbón (#1E293B) con pico naranja eléctrico (#EA580C).
4. body_white: Blanco ártico níveo (#F8FAFC) con pico naranja dorado (#F59E0B).
5. body_pink: Rosa chicle pastel (#F472B6) con pico fresa (#FB7185).
6. body_blue: Azul cerúleo vibrante (#38BDF8) con pico ámbar (#F59E0B).
7. body_green: Verde esmeralda silvestre (#10B981) con pico dorado (#D97706).
8. body_lavender: Lavanda místico suave (#A78BFA) con pico coral (#FB923C).

## 4. MATRIZ DE CIVILIZACIONES Y ACCESORIOS (10 ÉPOCAS)
1. CAVERNÍCOLA:
   - Ropa: clothes_caveman (piel con patrón de manchas y hombro al descubierto).
   - Cabeza: head_caveman (cinta de cuero con hueso prehistórico).
2. EGIPTO:
   - Ropa: clothes_egypt (collar Usekh dorado y faldón de lino blanco).
   - Cabeza: head_egypt (tocado Nemes azul y oro con cobra erguida).
3. GRECIA:
   - Ropa: clothes_greek (quitón blanco drapeado con bordado helénico).
   - Cabeza: head_greek (corona de laurel dorada).
4. ROMA:
   - Ropa: clothes_roman (lorica segmentata de placas metálicas y capa roja).
   - Cabeza: head_roman (casco gálico de centurión con penacho escarlata).
5. VIKINGO:
   - Ropa: clothes_viking (túnica de cuero, cuello de piel nórdica y correajes).
   - Cabeza: head_viking (casco cónico de hierro con protector nasal).
6. SAMURÁI:
   - Ropa: clothes_samurai (armadura do-maru laqueada y cordones ceremoniales).
   - Cabeza: head_samurai (casco kabuto con medialuna dorada frontal).
7. MEDIEVAL:
   - Ropa: clothes_medieval (tabardo con emblema heráldico y cota de malla).
   - Cabeza: head_medieval (yelmo cerrado de caballero con penacho de torneo).
8. PIRATA:
   - Ropa: clothes_pirate (casaca azul marino con botones dorados y faja roja).
   - Cabeza: head_pirate (tricornio negro con calavera y parche de ojo).
9. STEAMPUNK:
   - Ropa: clothes_steampunk (chaleco con engranajes de bronce y corbata de lazo).
   - Cabeza: head_steampunk (chistera con gafas de aviador cobrizas).
10. CYBERPUNK 2099:
    - Ropa: clothes_cyberpunk (chaqueta táctica de cuello alto con tiras de neón).
    - Cabeza: head_cyberpunk (visor holográfico monocular AR).

## 5. MATRIZ DE EXPRESIONES FACIALES
1. face_focused: Cejas inclinadas hacia adentro y pupilas firmes.
2. face_confident: Ojo derecho guiñado y sonrisa de victoria.
3. face_surprised: Ojos redondos abiertos y pico entreabierto.
4. face_calm: Ojos en arco sereno y pico relajado.

## 6. PROTOCOLO DE AUTO-EVALUACIÓN Y CALIDAD
Antes de aprobar cualquier asset, el diseñador debe certificar:
- Alineación: El accesorio de cabeza se apoya con precisión en y=160 sin flotar.
- Alfa Limpio: Cero halos blancos en los bordes sobre fondos oscuros (#0F172A).
- Coherencia: Estilo vectorial plano con líneas limpias y sombras de oclusión suaves.
