import os
import json
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AVATARS_DIR = os.path.join(BASE_DIR, 'static', 'quiz_games', 'avatars')
AVATARS_DIR = os.path.abspath(AVATARS_DIR)

BODIES_DIR = os.path.join(AVATARS_DIR, 'bodies')
CLOTHES_DIR = os.path.join(AVATARS_DIR, 'clothes')
HEADS_DIR = os.path.join(AVATARS_DIR, 'heads')
FACES_DIR = os.path.join(AVATARS_DIR, 'faces')

for d in [BODIES_DIR, CLOTHES_DIR, HEADS_DIR, FACES_DIR]:
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. GENERATE BODIES (8 inclusivos)
# ---------------------------------------------------------------------------
BODY_PALETTES = {
    'body_yellow': {
        'name': 'Amarillo Canario',
        'main': '#FBBF24', 'shadow': '#D97706', 'highlight': '#FDE68A', 'outline': '#B45309',
        'beak': '#F97316', 'beak_shadow': '#EA580C', 'feet': '#F97316', 'feet_shadow': '#C2410C'
    },
    'body_brown': {
        'name': 'Pardo Chocolate',
        'main': '#78350F', 'shadow': '#451A03', 'highlight': '#92400E', 'outline': '#291003',
        'beak': '#B45309', 'beak_shadow': '#78350F', 'feet': '#B45309', 'feet_shadow': '#78350F'
    },
    'body_black': {
        'name': 'Negro Ónix',
        'main': '#1E293B', 'shadow': '#0F172A', 'highlight': '#334155', 'outline': '#020617',
        'beak': '#EA580C', 'beak_shadow': '#C2410C', 'feet': '#EA580C', 'feet_shadow': '#9A3412'
    },
    'body_white': {
        'name': 'Blanco Ártico',
        'main': '#F8FAFC', 'shadow': '#CBD5E1', 'highlight': '#FFFFFF', 'outline': '#94A3B8',
        'beak': '#F59E0B', 'beak_shadow': '#D97706', 'feet': '#F59E0B', 'feet_shadow': '#B45309'
    },
    'body_pink': {
        'name': 'Rosa Chicle',
        'main': '#F472B6', 'shadow': '#DB2777', 'highlight': '#FBCFE8', 'outline': '#BE185D',
        'beak': '#FB7185', 'beak_shadow': '#E11D48', 'feet': '#FB7185', 'feet_shadow': '#E11D48'
    },
    'body_blue': {
        'name': 'Azul Cerúleo',
        'main': '#38BDF8', 'shadow': '#0284C7', 'highlight': '#BAE6FD', 'outline': '#0369A1',
        'beak': '#F59E0B', 'beak_shadow': '#D97706', 'feet': '#F59E0B', 'feet_shadow': '#B45309'
    },
    'body_green': {
        'name': 'Verde Esmeralda',
        'main': '#10B981', 'shadow': '#059669', 'highlight': '#A7F3D0', 'outline': '#047857',
        'beak': '#D97706', 'beak_shadow': '#B45309', 'feet': '#D97706', 'feet_shadow': '#92400E'
    },
    'body_lavender': {
        'name': 'Lavanda Místico',
        'main': '#A78BFA', 'shadow': '#7C3AED', 'highlight': '#DDD6FE', 'outline': '#6D28D9',
        'beak': '#FB923C', 'beak_shadow': '#EA580C', 'feet': '#FB923C', 'feet_shadow': '#C2410C'
    }
}

for body_id, colors in BODY_PALETTES.items():
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <radialGradient id="bodyGrad_{body_id}" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{colors['highlight']}" />
      <stop offset="60%" stop-color="{colors['main']}" />
      <stop offset="100%" stop-color="{colors['shadow']}" />
    </radialGradient>
    <radialGradient id="headGrad_{body_id}" cx="40%" cy="30%" r="60%">
      <stop offset="0%" stop-color="{colors['highlight']}" />
      <stop offset="65%" stop-color="{colors['main']}" />
      <stop offset="100%" stop-color="{colors['shadow']}" />
    </radialGradient>
    <linearGradient id="beakGrad_{body_id}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{colors['beak']}" />
      <stop offset="100%" stop-color="{colors['beak_shadow']}" />
    </linearGradient>
    <filter id="dropShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- CAPA 0: CUERPO BASE (Z-INDEX 10) -->
  <g id="ducky-body-base" filter="url(#dropShadow)">
    
    <!-- PATAS / PIES (Anclaje y=450) -->
    <!-- Pata Izquierda -->
    <g id="left-foot">
      <path d="M 180 435 C 160 450, 150 465, 170 472 C 185 478, 195 470, 205 460 C 215 472, 230 472, 235 460 C 240 450, 230 435, 215 432 Z" 
            fill="{colors['feet']}" stroke="{colors['feet_shadow']}" stroke-width="4" stroke-linejoin="round" />
      <path d="M 175 460 Q 190 450 200 440" stroke="{colors['feet_shadow']}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 215 462 Q 220 450 220 438" stroke="{colors['feet_shadow']}" stroke-width="3" fill="none" stroke-linecap="round"/>
    </g>

    <!-- Pata Derecha -->
    <g id="right-foot">
      <path d="M 332 435 C 352 450, 362 465, 342 472 C 327 478, 317 470, 307 460 C 297 472, 282 472, 277 460 C 272 450, 282 435, 297 432 Z" 
            fill="{colors['feet']}" stroke="{colors['feet_shadow']}" stroke-width="4" stroke-linejoin="round" />
      <path d="M 337 460 Q 322 450 312 440" stroke="{colors['feet_shadow']}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M 297 462 Q 292 450 292 438" stroke="{colors['feet_shadow']}" stroke-width="3" fill="none" stroke-linecap="round"/>
    </g>

    <!-- COLA DEL PATO (Izquierda trasera) -->
    <path d="M 170 340 C 120 325, 100 300, 115 285 C 135 270, 160 305, 185 315 Z" 
          fill="{colors['shadow']}" stroke="{colors['outline']}" stroke-width="4" />
    <path d="M 180 325 C 140 310, 125 290, 135 280 C 150 270, 175 295, 195 308 Z" 
          fill="{colors['main']}" />

    <!-- TORSO / PECHO (Centro anclaje y=320) -->
    <ellipse cx="256" cy="325" rx="108" ry="92" 
             fill="url(#bodyGrad_{body_id})" stroke="{colors['outline']}" stroke-width="5" />
    
    <!-- SOMBRA ABDOMINAL / VOLUMEN -->
    <path d="M 175 350 C 200 405, 312 405, 337 350 C 315 385, 197 385, 175 350 Z" 
          fill="{colors['shadow']}" opacity="0.35" />

    <!-- ALA IZQUIERDA -->
    <path d="M 155 280 C 130 300, 130 355, 155 375 C 170 388, 190 370, 185 340 C 180 305, 170 285, 155 280 Z" 
          fill="url(#bodyGrad_{body_id})" stroke="{colors['outline']}" stroke-width="4" />
    <path d="M 148 315 C 145 340, 160 360, 172 365" 
          stroke="{colors['shadow']}" stroke-width="3" fill="none" stroke-linecap="round" />

    <!-- ALA DERECHA -->
    <path d="M 357 280 C 382 300, 382 355, 357 375 C 342 388, 322 370, 327 340 C 332 305, 342 285, 357 280 Z" 
          fill="url(#bodyGrad_{body_id})" stroke="{colors['outline']}" stroke-width="4" />
    <path d="M 364 315 C 367 340, 352 360, 340 365" 
          stroke="{colors['shadow']}" stroke-width="3" fill="none" stroke-linecap="round" />

    <!-- CUELLO INTEGRADO -->
    <path d="M 215 220 C 215 255, 297 255, 297 220 Z" 
          fill="{colors['main']}" />

    <!-- MECHÓN DE PLUMAS EN LA CABEZA (y=75) -->
    <path d="M 256 88 C 248 65, 235 55, 245 45 C 255 52, 258 70, 260 85 Z" 
          fill="{colors['main']}" stroke="{colors['outline']}" stroke-width="3"/>
    <path d="M 260 88 C 265 62, 278 52, 270 42 C 260 50, 255 68, 254 85 Z" 
          fill="{colors['highlight']}" stroke="{colors['outline']}" stroke-width="3"/>

    <!-- CABEZA (Centro anclaje y=160, radio=80) -->
    <circle cx="256" cy="160" r="82" 
            fill="url(#headGrad_{body_id})" stroke="{colors['outline']}" stroke-width="5" />
    
    <!-- MEJILLAS BRILLO / HIGHLIGHT -->
    <ellipse cx="205" cy="180" rx="14" ry="9" fill="{colors['highlight']}" opacity="0.4"/>
    <ellipse cx="307" cy="180" rx="14" ry="9" fill="{colors['highlight']}" opacity="0.4"/>

    <!-- PICO BASE (Anclaje y=185 - y=205) -->
    <g id="beak-base">
      <ellipse cx="256" cy="198" rx="44" ry="22" 
               fill="url(#beakGrad_{body_id})" stroke="{colors['beak_shadow']}" stroke-width="4" />
      <path d="M 220 196 Q 256 208 292 196" 
            stroke="{colors['beak_shadow']}" stroke-width="3" fill="none" stroke-linecap="round"/>
      <!-- Fosas nasales -->
      <ellipse cx="247" cy="188" rx="2.5" ry="3.5" fill="{colors['beak_shadow']}"/>
      <ellipse cx="265" cy="188" rx="2.5" ry="3.5" fill="{colors['beak_shadow']}"/>
    </g>

  </g>
</svg>'''
    with open(os.path.join(BODIES_DIR, f'{body_id}.svg'), 'w', encoding='utf-8') as f:
        f.write(svg_content)

print("Bodies generated successfully.")

# ---------------------------------------------------------------------------
# 2. GENERATE CLOTHES (10 civilizaciones)
# ---------------------------------------------------------------------------
CLOTHES_ITEMS = [
    {
        'id': 'clothes_caveman', 'name': 'Piel Prehistórica', 'civ': 'Cavernícola',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - CAVERNICOLA -->
  <g id="clothes-caveman" filter="url(#clothShadow)">
    <!-- Túnica asimétrica de piel de leopardo / tigre dientes de sable -->
    <path d="M 205 235 L 295 260 L 330 380 L 305 400 L 285 385 L 265 405 L 245 385 L 225 405 L 205 385 L 180 395 L 175 320 Z" 
          fill="#D97706" stroke="#78350F" stroke-width="4" stroke-linejoin="round"/>
    <!-- Manchas de piel animal -->
    <circle cx="230" cy="300" r="7" fill="#78350F"/>
    <circle cx="270" cy="315" r="9" fill="#78350F"/>
    <circle cx="240" cy="350" r="8" fill="#78350F"/>
    <circle cx="290" cy="360" r="6" fill="#78350F"/>
    <circle cx="205" cy="340" r="7" fill="#78350F"/>
    <circle cx="260" cy="275" r="6" fill="#78350F"/>
    <!-- Correa de cuero cruzada al hombro -->
    <path d="M 205 235 L 235 230 L 310 350 L 285 365 Z" 
          fill="#92400E" stroke="#451A03" stroke-width="3"/>
    <!-- Cinto de cuerda y huesito colgante -->
    <path d="M 185 360 Q 256 375 325 360" stroke="#FEF3C7" stroke-width="6" fill="none" stroke-linecap="round"/>
    <g transform="translate(256, 375) rotate(15)">
      <rect x="-12" y="-4" width="24" height="8" rx="4" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5"/>
      <circle cx="-12" cy="-4" r="4" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1"/>
      <circle cx="-12" cy="4" r="4" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1"/>
      <circle cx="12" cy="-4" r="4" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1"/>
      <circle cx="12" cy="4" r="4" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1"/>
    </g>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_egypt', 'name': 'Túnica de Faraón y Usekh', 'civ': 'Egipto',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - EGIPTO -->
  <g id="clothes-egypt" filter="url(#clothShadow)">
    <!-- Faldellín Shendyt de lino blanco -->
    <path d="M 180 320 L 332 320 L 325 400 L 285 410 L 256 390 L 227 410 L 187 400 Z" 
          fill="#F8FAFC" stroke="#CBD5E1" stroke-width="4"/>
    <!-- Cinturón de oro real y banda central -->
    <path d="M 180 320 Q 256 335 332 320 L 332 338 Q 256 353 180 338 Z" 
          fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <path d="M 240 335 L 272 335 L 268 405 L 244 405 Z" 
          fill="#FBBF24" stroke="#D97706" stroke-width="2"/>
    <rect x="246" y="348" width="20" height="6" fill="#0284C7"/>
    <rect x="246" y="362" width="20" height="6" fill="#DC2626"/>
    <rect x="246" y="376" width="20" height="6" fill="#0284C7"/>
    <!-- Collar Usekh circular ceremonial -->
    <path d="M 195 230 C 190 295, 322 295, 317 230 C 295 260, 217 260, 195 230 Z" 
          fill="#F59E0B" stroke="#B45309" stroke-width="3"/>
    <path d="M 205 240 C 205 285, 307 285, 307 240" 
          stroke="#0284C7" stroke-width="5" fill="none"/>
    <path d="M 215 248 C 215 278, 297 278, 297 248" 
          stroke="#DC2626" stroke-width="4" fill="none"/>
    <circle cx="256" cy="275" r="5" fill="#10B981" stroke="#047857" stroke-width="1"/>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_greek', 'name': 'Quitón Helénico', 'civ': 'Grecia',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - GRECIA -->
  <g id="clothes-greek" filter="url(#clothShadow)">
    <!-- Túnica blanca drapeada (Quitón) -->
    <path d="M 205 230 L 307 235 L 340 395 C 310 408, 200 408, 172 395 Z" 
          fill="#FFFFFF" stroke="#E2E8F0" stroke-width="4"/>
    <!-- Pliegues y sombras del drapeado -->
    <path d="M 220 235 Q 235 320 230 398" stroke="#CBD5E1" stroke-width="3" fill="none"/>
    <path d="M 256 240 Q 260 325 258 402" stroke="#CBD5E1" stroke-width="3" fill="none"/>
    <path d="M 292 238 Q 280 320 286 398" stroke="#CBD5E1" stroke-width="3" fill="none"/>
    <!-- Greca / Cenefa griega dorada y azul en el borde inferior -->
    <path d="M 176 385 C 220 398, 290 398, 336 385" stroke="#F59E0B" stroke-width="8" fill="none"/>
    <path d="M 176 385 C 220 398, 290 398, 336 385" stroke="#0284C7" stroke-width="3" stroke-dasharray="6,4" fill="none"/>
    <!-- Fíbula dorada en hombro -->
    <circle cx="210" cy="235" r="7" fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <circle cx="210" cy="235" r="3" fill="#38BDF8"/>
    <!-- Cinturón cordón dorado (Zostra) -->
    <path d="M 185 330 Q 256 345 327 330" stroke="#F59E0B" stroke-width="4" fill="none"/>
    <path d="M 245 338 L 240 375" stroke="#F59E0B" stroke-width="3" fill="none"/>
    <path d="M 252 338 L 250 370" stroke="#F59E0B" stroke-width="3" fill="none"/>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_roman', 'name': 'Lorica Segmentata y Capa', 'civ': 'Roma',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - ROMA -->
  <g id="clothes-roman" filter="url(#clothShadow)">
    <!-- Capa imperial roja lateral/trasera -->
    <path d="M 195 240 L 160 380 Q 170 410 200 405 L 205 320 Z" 
          fill="#DC2626" stroke="#991B1B" stroke-width="3"/>
    <!-- Armadura Lorica Segmentata (Placas metálicas) -->
    <path d="M 190 250 L 322 250 L 335 345 L 177 345 Z" 
          fill="#94A3B8" stroke="#475569" stroke-width="4"/>
    <!-- Bandas/Placas horizontales con remaches -->
    <path d="M 185 275 L 327 275" stroke="#334155" stroke-width="3"/>
    <path d="M 180 300 L 332 300" stroke="#334155" stroke-width="3"/>
    <path d="M 178 325 L 334 325" stroke="#334155" stroke-width="3"/>
    <circle cx="210" cy="262" r="3" fill="#F8FAFC"/>
    <circle cx="302" cy="262" r="3" fill="#F8FAFC"/>
    <circle cx="210" cy="287" r="3" fill="#F8FAFC"/>
    <circle cx="302" cy="287" r="3" fill="#F8FAFC"/>
    <!-- Medallón Águila / Sol dorado central -->
    <circle cx="256" cy="285" r="14" fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <polygon points="256,275 259,282 266,285 259,288 256,295 253,288 246,285 253,282" fill="#FEF3C7"/>
    <!-- Pteruges (Tiras de cuero militar con tachuelas) -->
    <g fill="#78350F" stroke="#451A03" stroke-width="2">
      <rect x="195" y="345" width="16" height="50" rx="3"/>
      <rect x="220" y="345" width="16" height="55" rx="3"/>
      <rect x="248" y="345" width="16" height="58" rx="3"/>
      <rect x="276" y="345" width="16" height="55" rx="3"/>
      <rect x="301" y="345" width="16" height="50" rx="3"/>
    </g>
    <!-- Tachuelas de bronce en pteruges -->
    <circle cx="203" cy="385" r="3" fill="#F59E0B"/>
    <circle cx="228" cy="390" r="3" fill="#F59E0B"/>
    <circle cx="256" cy="393" r="3" fill="#F59E0B"/>
    <circle cx="284" cy="390" r="3" fill="#F59E0B"/>
    <circle cx="309" cy="385" r="3" fill="#F59E0B"/>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_viking', 'name': 'Túnica y Cuello Nórdico', 'civ': 'Vikingo',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - VIKINGO -->
  <g id="clothes-viking" filter="url(#clothShadow)">
    <!-- Túnica de lana azul nórdico oscuro -->
    <path d="M 180 260 L 332 260 L 335 400 L 177 400 Z" 
          fill="#1E3A8A" stroke="#172554" stroke-width="4"/>
    <!-- Ribetes bordados geométricos -->
    <path d="M 177 392 L 335 392" stroke="#F59E0B" stroke-width="6"/>
    <!-- Correajes de cuero en X -->
    <path d="M 195 260 L 317 355" stroke="#78350F" stroke-width="8" stroke-linecap="round"/>
    <path d="M 317 260 L 195 355" stroke="#78350F" stroke-width="8" stroke-linecap="round"/>
    <circle cx="256" cy="307" r="8" fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <!-- Cuello / Manto de piel nórdica alrededor del cuello -->
    <path d="M 180 230 C 170 280, 210 295, 256 290 C 302 295, 342 280, 332 230 C 305 248, 207 248, 180 230 Z" 
          fill="#713F12" stroke="#451A03" stroke-width="3"/>
    <path d="M 190 240 C 185 275, 215 285, 256 280 C 297 285, 327 275, 322 240 C 300 252, 212 252, 190 240 Z" 
          fill="#A16207"/>
    <!-- Broche circular vikingo -->
    <circle cx="285" cy="255" r="7" fill="#E2E8F0" stroke="#475569" stroke-width="2"/>
    <!-- Cinturón ancho de cuero con hebilla de hierro -->
    <rect x="175" y="350" width="162" height="18" fill="#451A03" stroke="#291003" stroke-width="2"/>
    <rect x="244" y="346" width="24" height="26" rx="3" fill="#E2E8F0" stroke="#475569" stroke-width="2"/>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_samurai', 'name': 'Armadura Do-Maru', 'civ': 'Samurái',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - SAMURAI -->
  <g id="clothes-samurai" filter="url(#clothShadow)">
    <!-- Hombreras Sode laminadas -->
    <!-- Sode Izquierda -->
    <g transform="translate(145, 250) rotate(-10)">
      <rect x="0" y="0" width="38" height="14" rx="2" fill="#DC2626" stroke="#000" stroke-width="2"/>
      <rect x="0" y="14" width="38" height="14" rx="2" fill="#1E293B" stroke="#000" stroke-width="2"/>
      <rect x="0" y="28" width="38" height="14" rx="2" fill="#DC2626" stroke="#000" stroke-width="2"/>
      <rect x="0" y="42" width="38" height="14" rx="2" fill="#1E293B" stroke="#000" stroke-width="2"/>
      <path d="M 8 0 L 8 56 M 19 0 L 19 56 M 30 0 L 30 56" stroke="#F59E0B" stroke-width="2"/>
    </g>
    <!-- Sode Derecha -->
    <g transform="translate(329, 245) rotate(10)">
      <rect x="0" y="0" width="38" height="14" rx="2" fill="#DC2626" stroke="#000" stroke-width="2"/>
      <rect x="0" y="14" width="38" height="14" rx="2" fill="#1E293B" stroke="#000" stroke-width="2"/>
      <rect x="0" y="28" width="38" height="14" rx="2" fill="#DC2626" stroke="#000" stroke-width="2"/>
      <rect x="0" y="42" width="38" height="14" rx="2" fill="#1E293B" stroke="#000" stroke-width="2"/>
      <path d="M 8 0 L 8 56 M 19 0 L 19 56 M 30 0 L 30 56" stroke="#F59E0B" stroke-width="2"/>
    </g>
    <!-- Pechera Do-Maru laqueada -->
    <path d="M 185 245 L 327 245 L 335 375 L 177 375 Z" 
          fill="#0F172A" stroke="#000" stroke-width="4"/>
    <!-- Placas y cordones de seda carmesí y oro (Odoshi) -->
    <rect x="187" y="255" width="138" height="22" rx="3" fill="#991B1B" stroke="#F59E0B" stroke-width="2"/>
    <rect x="187" y="285" width="138" height="22" rx="3" fill="#991B1B" stroke="#F59E0B" stroke-width="2"/>
    <rect x="187" y="315" width="138" height="22" rx="3" fill="#991B1B" stroke="#F59E0B" stroke-width="2"/>
    <!-- Faja Obi dorado con nudo ceremonial -->
    <rect x="175" y="348" width="162" height="22" fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <circle cx="256" cy="359" r="7" fill="#DC2626" stroke="#991B1B" stroke-width="2"/>
    <!-- Falda Kusazuri de placas inferiores -->
    <rect x="188" y="375" width="30" height="28" fill="#1E293B" stroke="#000" stroke-width="2"/>
    <rect x="224" y="375" width="30" height="30" fill="#991B1B" stroke="#000" stroke-width="2"/>
    <rect x="258" y="375" width="30" height="30" fill="#991B1B" stroke="#000" stroke-width="2"/>
    <rect x="294" y="375" width="30" height="28" fill="#1E293B" stroke="#000" stroke-width="2"/>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_medieval', 'name': 'Tabardo Heráldico y Malla', 'civ': 'Medieval',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
    <pattern id="chainmail" width="8" height="8" patternUnits="userSpaceOnUse">
      <circle cx="4" cy="4" r="3" fill="none" stroke="#64748B" stroke-width="1.2"/>
    </pattern>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - MEDIEVAL -->
  <g id="clothes-medieval" filter="url(#clothShadow)">
    <!-- Cota de malla en cuello y base -->
    <path d="M 175 240 L 337 240 L 340 405 L 172 405 Z" fill="url(#chainmail)" stroke="#475569" stroke-width="3"/>
    <!-- Tabardo partido (Mitad Azul Real, Mitad Rojo Escarlata) -->
    <!-- Mitad Izquierda (Azul) -->
    <path d="M 190 235 L 256 235 L 256 395 L 185 395 Z" 
          fill="#1D4ED8" stroke="#1E3A8A" stroke-width="3"/>
    <!-- Mitad Derecha (Rojo) -->
    <path d="M 256 235 L 322 235 L 327 395 L 256 395 Z" 
          fill="#DC2626" stroke="#991B1B" stroke-width="3"/>
    <!-- Emblema Heráldico Central: Cruz Dorada Paté -->
    <g transform="translate(256, 305)">
      <path d="M -6 -24 L 6 -24 L 4 -6 L 24 -4 L 24 6 L 4 4 L 6 24 L -6 24 L -4 4 L -24 6 L -24 -4 L -4 -6 Z" 
            fill="#FBBF24" stroke="#D97706" stroke-width="2"/>
      <circle cx="0" cy="0" r="4" fill="#FFFFFF"/>
    </g>
    <!-- Cinturón de caballero con tachas de acero -->
    <rect x="180" y="345" width="152" height="16" fill="#334155" stroke="#1E293B" stroke-width="2"/>
    <circle cx="256" cy="353" r="6" fill="#FBBF24" stroke="#B45309" stroke-width="2"/>
    <!-- Caída del cinturón -->
    <rect x="251" y="353" width="10" height="35" fill="#334155" stroke="#1E293B" stroke-width="2"/>
    <polygon points="251,388 261,388 256,396" fill="#FBBF24"/>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_pirate', 'name': 'Casaca de Capitán Pirata', 'civ': 'Pirata',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - PIRATA -->
  <g id="clothes-pirate" filter="url(#clothShadow)">
    <!-- Camisa blanca de chorrera interior -->
    <path d="M 225 235 L 287 235 L 280 340 L 232 340 Z" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
    <!-- Pliegues de la chorrera -->
    <path d="M 235 245 Q 256 260 277 245" stroke="#CBD5E1" stroke-width="3" fill="none"/>
    <path d="M 238 265 Q 256 280 274 265" stroke="#CBD5E1" stroke-width="3" fill="none"/>
    <path d="M 242 285 Q 256 295 270 285" stroke="#CBD5E1" stroke-width="3" fill="none"/>
    <!-- Faja roja de seda pirata -->
    <path d="M 180 330 Q 256 345 332 330 L 332 360 Q 256 375 180 360 Z" 
          fill="#DC2626" stroke="#991B1B" stroke-width="2"/>
    <path d="M 210 355 L 205 400 L 225 395 L 222 355 Z" fill="#DC2626" stroke="#991B1B" stroke-width="1.5"/>
    <!-- Casaca Azul Marino / Solapas -->
    <!-- Lado Izquierdo -->
    <path d="M 180 240 L 230 240 L 218 335 L 175 395 Z" 
          fill="#0F172A" stroke="#F59E0B" stroke-width="3"/>
    <!-- Lado Derecho -->
    <path d="M 332 240 L 282 240 L 294 335 L 337 395 Z" 
          fill="#0F172A" stroke="#F59E0B" stroke-width="3"/>
    <!-- Botones dorados y ojales de gala -->
    <circle cx="218" cy="265" r="4" fill="#FBBF24" stroke="#D97706" stroke-width="1"/>
    <line x1="205" y1="265" x2="218" y2="265" stroke="#FBBF24" stroke-width="2"/>
    <circle cx="214" cy="290" r="4" fill="#FBBF24" stroke="#D97706" stroke-width="1"/>
    <line x1="200" y1="290" x2="214" y2="290" stroke="#FBBF24" stroke-width="2"/>
    <circle cx="210" cy="315" r="4" fill="#FBBF24" stroke="#D97706" stroke-width="1"/>
    <line x1="195" y1="315" x2="210" y2="315" stroke="#FBBF24" stroke-width="2"/>

    <circle cx="294" cy="265" r="4" fill="#FBBF24" stroke="#D97706" stroke-width="1"/>
    <line x1="294" y1="265" x2="307" y2="265" stroke="#FBBF24" stroke-width="2"/>
    <circle cx="298" cy="290" r="4" fill="#FBBF24" stroke="#D97706" stroke-width="1"/>
    <line x1="298" y1="290" x2="312" y2="290" stroke="#FBBF24" stroke-width="2"/>
    <circle cx="302" cy="315" r="4" fill="#FBBF24" stroke="#D97706" stroke-width="1"/>
    <line x1="302" y1="315" x2="317" y2="315" stroke="#FBBF24" stroke-width="2"/>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_steampunk', 'name': 'Chaleco de Engranajes Steampunk', 'civ': 'Steampunk',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - STEAMPUNK -->
  <g id="clothes-steampunk" filter="url(#clothShadow)">
    <!-- Camisa marfil / cuello alto -->
    <path d="M 215 230 L 297 230 L 290 320 L 222 320 Z" fill="#FEF3C7" stroke="#FDE68A" stroke-width="2"/>
    <!-- Corbata de lazo / Plastrón de terciopelo burdeos -->
    <polygon points="256,245 240,265 272,265" fill="#881337"/>
    <circle cx="256" cy="245" r="4" fill="#D97706"/>
    <polygon points="256,245 245,290 256,285 267,290" fill="#9F1239" stroke="#881337" stroke-width="1.5"/>
    <!-- Chaleco de cuero marrón victoriano -->
    <path d="M 180 240 L 235 240 L 245 340 L 256 370 L 267 340 L 277 240 L 332 240 L 335 385 L 256 405 L 177 385 Z" 
          fill="#78350F" stroke="#451A03" stroke-width="4"/>
    <!-- Solapas con ribete de bronce -->
    <path d="M 180 240 L 235 290 L 210 365" stroke="#D97706" stroke-width="3" fill="none"/>
    <path d="M 332 240 L 277 290 L 302 365" stroke="#D97706" stroke-width="3" fill="none"/>
    <!-- Cadena de reloj de bolsillo leontina dorada -->
    <path d="M 215 320 Q 240 350 256 335" stroke="#F59E0B" stroke-width="3" fill="none" stroke-linecap="round"/>
    <!-- Manómetro de vapor miniatura en el pecho -->
    <circle cx="295" cy="305" r="12" fill="#FEF3C7" stroke="#B45309" stroke-width="3"/>
    <line x1="295" y1="305" x2="302" y2="298" stroke="#DC2626" stroke-width="2" stroke-linecap="round"/>
    <circle cx="295" cy="305" r="2" fill="#000"/>
    <!-- Engranajes de bronce decorativos -->
    <g transform="translate(205, 335) scale(0.6)">
      <circle cx="0" cy="0" r="10" fill="#D97706" stroke="#92400E" stroke-width="2"/>
      <circle cx="0" cy="0" r="4" fill="#78350F"/>
    </g>
  </g>
</svg>'''
    },
    {
        'id': 'clothes_cyberpunk', 'name': 'Chaqueta Táctica Neón 2099', 'civ': 'Cyberpunk 2099',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#06B6D4" flood-opacity="0.9"/>
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#EC4899" flood-opacity="0.7"/>
    </filter>
    <filter id="clothShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <!-- CAPA 1: ROPA (Z-INDEX 20) - CYBERPUNK 2099 -->
  <g id="clothes-cyberpunk" filter="url(#clothShadow)">
    <!-- Chaqueta Techwear oscura de fibra de carbono -->
    <path d="M 180 230 L 210 215 L 256 240 L 302 215 L 332 230 L 340 395 L 256 410 L 172 395 Z" 
          fill="#090D16" stroke="#1E293B" stroke-width="4"/>
    <!-- Cuello alto táctico asimétrico -->
    <path d="M 205 215 L 215 250 L 297 250 L 307 215 Z" fill="#1E293B" stroke="#0F172A" stroke-width="2"/>
    <!-- Tiras lumínicas LED de Neón Cian -->
    <g filter="url(#neonGlow)">
      <path d="M 195 240 L 235 340 L 235 390" stroke="#06B6D4" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M 317 240 L 277 340 L 277 390" stroke="#EC4899" stroke-width="4" fill="none" stroke-linecap="round"/>
      <line x1="210" y1="280" x2="245" y2="280" stroke="#06B6D4" stroke-width="3"/>
      <line x1="302" y1="280" x2="267" y2="280" stroke="#EC4899" stroke-width="3"/>
    </g>
    <!-- Módulo de energía central / Arc Core triangular -->
    <polygon points="256,290 268,312 244,312" fill="#06B6D4" filter="url(#neonGlow)"/>
    <polygon points="256,295 264,309 248,309" fill="#E0F2FE"/>
    <!-- Bolsillos tácticos modulares -->
    <rect x="185" y="335" width="35" height="30" rx="3" fill="#1E293B" stroke="#334155" stroke-width="2"/>
    <rect x="292" y="335" width="35" height="30" rx="3" fill="#1E293B" stroke="#334155" stroke-width="2"/>
    <line x1="185" y1="345" x2="220" y2="345" stroke="#06B6D4" stroke-width="2"/>
    <line x1="292" y1="345" x2="327" y2="345" stroke="#EC4899" stroke-width="2"/>
  </g>
</svg>'''
    }
]

for item in CLOTHES_ITEMS:
    with open(os.path.join(CLOTHES_DIR, f"{item['id']}.svg"), 'w', encoding='utf-8') as f:
        f.write(item['svg'])

print("Clothes generated successfully.")

# ---------------------------------------------------------------------------
# 3. GENERATE HEADS (10 accesorios de cabeza / sombreros)
# ---------------------------------------------------------------------------
HEAD_ITEMS = [
    {
        'id': 'head_caveman', 'name': 'Cinta de Cuero y Hueso', 'civ': 'Cavernícola',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#000" flood-opacity="0.35"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - CAVERNICOLA -->
  <g id="head-caveman" filter="url(#headShadow)">
    <!-- Cinta de cuero rústica rodeando la frente (y=125-135) -->
    <path d="M 175 130 C 210 115, 302 115, 337 130 L 335 145 C 300 130, 210 130, 177 145 Z" 
          fill="#78350F" stroke="#451A03" stroke-width="3"/>
    <!-- Costuras de tendón -->
    <line x1="200" y1="125" x2="204" y2="137" stroke="#FEF3C7" stroke-width="2"/>
    <line x1="230" y1="122" x2="234" y2="134" stroke="#FEF3C7" stroke-width="2"/>
    <line x1="280" y1="122" x2="284" y2="134" stroke="#FEF3C7" stroke-width="2"/>
    <line x1="310" y1="125" x2="314" y2="137" stroke="#FEF3C7" stroke-width="2"/>
    <!-- Gran hueso prehistórico atado al centro (inclinado) -->
    <g transform="translate(256, 115) rotate(-12)">
      <rect x="-35" y="-8" width="70" height="16" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="3"/>
      <!-- Nódulos de articulación del hueso -->
      <circle cx="-35" cy="-8" r="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
      <circle cx="-35" cy="8" r="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
      <circle cx="35" cy="-8" r="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
      <circle cx="35" cy="8" r="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2"/>
      <!-- Amarre de cuerda cruzada en X -->
      <line x1="-12" y1="-9" x2="12" y2="9" stroke="#78350F" stroke-width="3"/>
      <line x1="-12" y1="9" x2="12" y2="-9" stroke="#78350F" stroke-width="3"/>
    </g>
  </g>
</svg>'''
    },
    {
        'id': 'head_egypt', 'name': 'Tocado Nemes de Faraón', 'civ': 'Egipto',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - EGIPTO -->
  <g id="head-egypt" filter="url(#headShadow)">
    <!-- Tocado Nemes superior y aletas laterales cayendo sobre hombros -->
    <!-- Aleta Izquierda -->
    <path d="M 180 120 L 155 220 L 190 215 L 200 140 Z" fill="#0284C7" stroke="#0369A1" stroke-width="3"/>
    <path d="M 163 150 L 197 150 M 158 180 L 193 180" stroke="#F59E0B" stroke-width="6"/>
    <!-- Aleta Derecha -->
    <path d="M 332 120 L 357 220 L 322 215 L 312 140 Z" fill="#0284C7" stroke="#0369A1" stroke-width="3"/>
    <path d="M 315 150 L 349 150 M 319 180 L 354 180" stroke="#F59E0B" stroke-width="6"/>
    <!-- Corona Nemes Principal arqueada -->
    <path d="M 175 130 C 170 55, 342 55, 337 130 C 300 110, 212 110, 175 130 Z" 
          fill="#0284C7" stroke="#0369A1" stroke-width="4"/>
    <!-- Franjas doradas radiantes -->
    <path d="M 210 75 Q 220 115 220 115" stroke="#F59E0B" stroke-width="8" fill="none"/>
    <path d="M 240 65 Q 244 112 244 112" stroke="#F59E0B" stroke-width="8" fill="none"/>
    <path d="M 272 65 Q 268 112 268 112" stroke="#F59E0B" stroke-width="8" fill="none"/>
    <path d="M 302 75 Q 292 115 292 115" stroke="#F59E0B" stroke-width="8" fill="none"/>
    <!-- Banda frontal dorada -->
    <path d="M 175 125 C 210 110, 302 110, 337 125 L 335 140 C 300 125, 210 125, 177 140 Z" 
          fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <!-- Uraeus (Cobra sagrada erguida frontal) -->
    <g transform="translate(256, 105)">
      <path d="M 0 15 Q -10 5 -5 -8 Q 0 -18 5 -8 Q 10 5 0 15 Z" fill="#FBBF24" stroke="#B45309" stroke-width="2"/>
      <circle cx="0" cy="-12" r="5" fill="#DC2626" stroke="#B45309" stroke-width="1.5"/>
      <circle cx="-1.5" cy="-13" r="1" fill="#000"/>
      <circle cx="1.5" cy="-13" r="1" fill="#000"/>
    </g>
  </g>
</svg>'''
    },
    {
        'id': 'head_greek', 'name': 'Corona de Laurel Helénica', 'civ': 'Grecia',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - GRECIA -->
  <g id="head-greek" filter="url(#headShadow)">
    <!-- Rama izquierda de hojas de laurel doradas -->
    <path d="M 180 135 C 190 90, 240 85, 252 88" stroke="#D97706" stroke-width="3" fill="none"/>
    <!-- Hojas izquierda -->
    <g fill="#FBBF24" stroke="#B45309" stroke-width="1.5">
      <path d="M 185 130 Q 170 120 180 110 Q 192 120 185 130 Z"/>
      <path d="M 198 115 Q 185 100 200 95 Q 208 108 198 115 Z"/>
      <path d="M 215 102 Q 205 85 220 80 Q 228 95 215 102 Z"/>
      <path d="M 235 94 Q 230 75 245 74 Q 248 88 235 94 Z"/>
    </g>
    <!-- Rama derecha de hojas de laurel doradas -->
    <path d="M 332 135 C 322 90, 272 85, 260 88" stroke="#D97706" stroke-width="3" fill="none"/>
    <!-- Hojas derecha -->
    <g fill="#FBBF24" stroke="#B45309" stroke-width="1.5">
      <path d="M 327 130 Q 342 120 332 110 Q 320 120 327 130 Z"/>
      <path d="M 314 115 Q 327 100 312 95 Q 304 108 314 115 Z"/>
      <path d="M 297 102 Q 307 85 292 80 Q 284 95 297 102 Z"/>
      <path d="M 277 94 Q 282 75 267 74 Q 264 88 277 94 Z"/>
    </g>
    <!-- Broche / Lazo central frontal -->
    <circle cx="256" cy="88" r="5" fill="#FEF3C7" stroke="#D97706" stroke-width="2"/>
  </g>
</svg>'''
    },
    {
        'id': 'head_roman', 'name': 'Casco Galea de Centurión', 'civ': 'Roma',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - ROMA -->
  <g id="head-roman" filter="url(#headShadow)">
    <!-- Penacho / Cresta transversal roja de centurión (y=30 a y=95) -->
    <path d="M 175 75 C 190 20, 322 20, 337 75 C 300 55, 210 55, 175 75 Z" 
          fill="#DC2626" stroke="#991B1B" stroke-width="3"/>
    <!-- Fibras de crin del penacho -->
    <path d="M 195 60 L 195 38 M 220 50 L 220 28 M 256 45 L 256 22 M 292 50 L 292 28 M 317 60 L 317 38" 
          stroke="#EF4444" stroke-width="3" stroke-linecap="round"/>
    <!-- Soporte dorado de la cresta -->
    <path d="M 210 75 Q 256 68 302 75 L 297 88 Q 256 82 215 88 Z" fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <!-- Casco Galea de bronce -->
    <path d="M 175 130 C 172 70, 340 70, 337 130 C 305 118, 207 118, 175 130 Z" 
          fill="#D97706" stroke="#92400E" stroke-width="4"/>
    <!-- Visera frontal y protector de cejas -->
    <path d="M 175 125 Q 256 100 337 125 L 335 138 Q 256 115 177 138 Z" 
          fill="#FBBF24" stroke="#B45309" stroke-width="2"/>
    <!-- Protectores de mejillas (Carrilleras laterales) -->
    <path d="M 175 135 L 168 185 Q 185 190 190 170 L 188 135 Z" fill="#D97706" stroke="#92400E" stroke-width="2"/>
    <path d="M 337 135 L 344 185 Q 327 190 322 170 L 324 135 Z" fill="#D97706" stroke="#92400E" stroke-width="2"/>
    <!-- Remaches decorativos -->
    <circle cx="182" cy="155" r="3" fill="#FEF3C7"/>
    <circle cx="330" cy="155" r="3" fill="#FEF3C7"/>
  </g>
</svg>'''
    },
    {
        'id': 'head_viking', 'name': 'Yelmo Vikingo Spangenhelm', 'civ': 'Vikingo',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - VIKINGO -->
  <g id="head-viking" filter="url(#headShadow)">
    <!-- Casco cónico de placas de hierro remachadas -->
    <path d="M 175 135 C 180 50, 256 40, 256 40 C 256 40, 332 50, 337 135 C 300 120, 210 120, 175 135 Z" 
          fill="#64748B" stroke="#334155" stroke-width="4"/>
    <!-- Banda de refuerzo vertical central con púa superior -->
    <path d="M 248 40 L 264 40 L 262 125 L 250 125 Z" fill="#475569" stroke="#1E293B" stroke-width="2"/>
    <polygon points="256,22 250,40 262,40" fill="#94A3B8" stroke="#334155" stroke-width="2"/>
    <!-- Banda de cejas / Base con remaches -->
    <path d="M 175 125 Q 256 110 337 125 L 335 142 Q 256 128 177 142 Z" 
          fill="#475569" stroke="#1E293B" stroke-width="2"/>
    <!-- Protector ocular / Antifaz nasal nórdico -->
    <path d="M 215 132 C 220 155, 245 155, 250 135 L 256 175 L 262 135 C 267 155, 292 155, 297 132 Z" 
          fill="#334155" stroke="#0F172A" stroke-width="2"/>
    <!-- Remaches de acero -->
    <circle cx="256" cy="65" r="2.5" fill="#E2E8F0"/>
    <circle cx="256" cy="85" r="2.5" fill="#E2E8F0"/>
    <circle cx="256" cy="105" r="2.5" fill="#E2E8F0"/>
    <circle cx="195" cy="132" r="2.5" fill="#E2E8F0"/>
    <circle cx="317" cy="132" r="2.5" fill="#E2E8F0"/>
  </g>
</svg>'''
    },
    {
        'id': 'head_samurai', 'name': 'Kabuto con Medialuna Dorada', 'civ': 'Samurái',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000" flood-opacity="0.45"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - SAMURAI -->
  <g id="head-samurai" filter="url(#headShadow)">
    <!-- Protector de nuca laminado (Shikoro) -->
    <path d="M 160 140 C 150 185, 200 195, 210 160" stroke="#DC2626" stroke-width="8" fill="none" stroke-linecap="round"/>
    <path d="M 352 140 C 362 185, 312 195, 302 160" stroke="#DC2626" stroke-width="8" fill="none" stroke-linecap="round"/>
    <!-- Casco semiesférico Kabuto negro laqueado -->
    <path d="M 175 130 C 170 55, 342 55, 337 130 C 300 115, 212 115, 175 130 Z" 
          fill="#0F172A" stroke="#000" stroke-width="4"/>
    <!-- Visera Mabizashi con ribete dorado -->
    <path d="M 180 125 Q 256 105 332 125 L 330 138 Q 256 120 182 138 Z" 
          fill="#F59E0B" stroke="#B45309" stroke-width="2"/>
    <!-- Aletas laterales Fukigaeshi -->
    <g transform="translate(178, 125) rotate(20)">
      <rect x="-8" y="-15" width="16" height="30" rx="3" fill="#991B1B" stroke="#F59E0B" stroke-width="2"/>
      <circle cx="0" cy="0" r="3" fill="#FBBF24"/>
    </g>
    <g transform="translate(334, 125) rotate(-20)">
      <rect x="-8" y="-15" width="16" height="30" rx="3" fill="#991B1B" stroke="#F59E0B" stroke-width="2"/>
      <circle cx="0" cy="0" r="3" fill="#FBBF24"/>
    </g>
    <!-- Gran Maedate: Medialuna dorada frontal gigante -->
    <g transform="translate(256, 75)">
      <path d="M 0 -45 C 35 -40, 60 -10, 50 15 C 35 0, 15 -15, 0 -15 C -15 -15, -35 0, -50 15 C -60 -10, -35 -40, 0 -45 Z" 
            fill="#FBBF24" stroke="#D97706" stroke-width="3"/>
      <!-- Sol / Emblema central -->
      <circle cx="0" cy="10" r="10" fill="#DC2626" stroke="#FBBF24" stroke-width="2"/>
    </g>
  </g>
</svg>'''
    },
    {
        'id': 'head_medieval', 'name': 'Gran Yelmo de Caballero', 'civ': 'Medieval',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - MEDIEVAL -->
  <g id="head-medieval" filter="url(#headShadow)">
    <!-- Penacho de plumas de torneo ondeante (y=25 a y=80) -->
    <path d="M 256 60 C 270 20, 310 15, 330 30 C 300 40, 280 50, 265 65 Z" 
          fill="#DC2626" stroke="#991B1B" stroke-width="2"/>
    <path d="M 256 60 C 240 25, 205 20, 185 35 C 215 45, 235 52, 247 65 Z" 
          fill="#1D4ED8" stroke="#1E3A8A" stroke-width="2"/>
    <!-- Bóveda y corona del yelmo de acero pulido -->
    <path d="M 175 140 C 172 58, 340 58, 337 140 C 305 125, 207 125, 175 140 Z" 
          fill="#94A3B8" stroke="#475569" stroke-width="4"/>
    <!-- Cruz de refuerzo de latón dorado sobre el frontal -->
    <path d="M 250 65 L 262 65 L 262 142 L 250 142 Z" fill="#FBBF24" stroke="#B45309" stroke-width="1.5"/>
    <path d="M 190 120 L 322 120 L 322 134 L 190 134 Z" fill="#FBBF24" stroke="#B45309" stroke-width="1.5"/>
    <!-- Ranuras oculares estrechas de combate (Visor slit) -->
    <rect x="200" y="123" width="45" height="6" rx="2" fill="#0F172A"/>
    <rect x="267" y="123" width="45" height="6" rx="2" fill="#0F172A"/>
    <!-- Agujeros de ventilación / Respiraderos en cruz -->
    <circle cx="225" cy="140" r="2" fill="#334155"/>
    <circle cx="235" cy="140" r="2" fill="#334155"/>
    <circle cx="277" cy="140" r="2" fill="#334155"/>
    <circle cx="287" cy="140" r="2" fill="#334155"/>
  </g>
</svg>'''
    },
    {
        'id': 'head_pirate', 'name': 'Tricornio Pirata y Parche', 'civ': 'Pirata',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000" flood-opacity="0.45"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - PIRATA -->
  <g id="head-pirate" filter="url(#headShadow)">
    <!-- Parche en el ojo derecho con cinta diagonal -->
    <path d="M 180 140 L 325 185" stroke="#0F172A" stroke-width="3" fill="none"/>
    <ellipse cx="295" cy="175" rx="14" ry="12" fill="#0F172A" stroke="#334155" stroke-width="2"/>
    <!-- Tricornio de fieltro negro con tres puntas elevadas -->
    <path d="M 145 130 C 170 80, 205 60, 256 60 C 307 60, 342 80, 367 130 C 330 110, 290 100, 256 100 C 222 100, 182 110, 145 130 Z" 
          fill="#0F172A" stroke="#000" stroke-width="4"/>
    <!-- Ribete de galón dorado en los bordes del tricornio -->
    <path d="M 145 130 C 170 80, 205 60, 256 60 C 307 60, 342 80, 367 130" 
          stroke="#F59E0B" stroke-width="4" fill="none"/>
    <!-- Copa interior del sombrero -->
    <path d="M 210 100 C 210 65, 302 65, 302 100 Z" fill="#1E293B"/>
    <!-- Calavera y tibias cruzadas (Jolly Roger) al frente -->
    <g transform="translate(256, 82) scale(0.8)">
      <!-- Tibias -->
      <line x1="-16" y1="-14" x2="16" y2="14" stroke="#F8FAFC" stroke-width="4" stroke-linecap="round"/>
      <line x1="16" y1="-14" x2="-16" y2="14" stroke="#F8FAFC" stroke-width="4" stroke-linecap="round"/>
      <!-- Cráneo -->
      <circle cx="0" cy="-2" r="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
      <circle cx="-3.5" cy="-3" r="2.5" fill="#000"/>
      <circle cx="3.5" cy="-3" r="2.5" fill="#000"/>
      <rect x="-4" y="5" width="8" height="5" rx="1" fill="#F8FAFC"/>
    </g>
    <!-- Pluma de loro roja sobresaliendo en el lateral -->
    <path d="M 190 95 C 160 55, 140 50, 120 70 C 145 80, 165 90, 180 105 Z" 
          fill="#DC2626" stroke="#991B1B" stroke-width="1.5"/>
  </g>
</svg>'''
    },
    {
        'id': 'head_steampunk', 'name': 'Chistera y Gafas de Bronce', 'civ': 'Steampunk',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="headShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - STEAMPUNK -->
  <g id="head-steampunk" filter="url(#headShadow)">
    <!-- Copa cilíndrica alta de la chistera de cuero -->
    <path d="M 205 115 L 212 35 L 300 35 L 307 115 Z" 
          fill="#451A03" stroke="#291003" stroke-width="4"/>
    <ellipse cx="256" cy="35" rx="44" ry="12" fill="#78350F" stroke="#291003" stroke-width="3"/>
    <!-- Cinta ancha de cuero con hebilla de bronce -->
    <path d="M 206 100 L 306 100 L 307 115 L 205 115 Z" fill="#991B1B" stroke="#78350F" stroke-width="2"/>
    <!-- Ala ancha curvada de la chistera -->
    <ellipse cx="256" cy="118" rx="76" ry="18" fill="#451A03" stroke="#291003" stroke-width="4"/>
    <!-- Gafas de aviador de bronce montadas sobre el ala -->
    <!-- Correa de las gafas -->
    <path d="M 195 118 Q 256 128 317 118" stroke="#1E293B" stroke-width="5" fill="none"/>
    <!-- Lente Izquierda -->
    <circle cx="230" cy="118" r="16" fill="#0284C7" stroke="#D97706" stroke-width="4"/>
    <circle cx="230" cy="118" r="12" fill="#38BDF8" opacity="0.7"/>
    <line x1="222" y1="112" x2="238" y2="124" stroke="#FFF" stroke-width="2" stroke-linecap="round"/>
    <!-- Lente Derecha -->
    <circle cx="282" cy="118" r="16" fill="#0284C7" stroke="#D97706" stroke-width="4"/>
    <circle cx="282" cy="118" r="12" fill="#38BDF8" opacity="0.7"/>
    <line x1="274" y1="112" x2="290" y2="124" stroke="#FFF" stroke-width="2" stroke-linecap="round"/>
    <!-- Puente de las gafas con engranaje central -->
    <line x1="246" y1="118" x2="266" y2="118" stroke="#D97706" stroke-width="4"/>
  </g>
</svg>'''
    },
    {
        'id': 'head_cyberpunk', 'name': 'Visor Holográfico AR 2099', 'civ': 'Cyberpunk 2099',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="neonGlowHead" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#06B6D4" flood-opacity="0.95"/>
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#EC4899" flood-opacity="0.8"/>
    </filter>
  </defs>
  <!-- CAPA 3: SOMBRERO / CABEZA (Z-INDEX 40) - CYBERPUNK 2099 -->
  <g id="head-cyberpunk">
    <!-- Diadema / headset techwear temporal -->
    <path d="M 175 145 C 190 120, 322 120, 337 145" stroke="#1E293B" stroke-width="6" fill="none" stroke-linecap="round"/>
    <!-- Nodo auditivo con antena izquierda -->
    <circle cx="178" cy="145" r="9" fill="#0F172A" stroke="#06B6D4" stroke-width="3"/>
    <line x1="178" y1="145" x2="162" y2="95" stroke="#06B6D4" stroke-width="3" stroke-linecap="round"/>
    <circle cx="162" cy="95" r="3" fill="#EC4899"/>
    <!-- Nodo derecho con LED -->
    <circle cx="334" cy="145" r="9" fill="#0F172A" stroke="#EC4899" stroke-width="3"/>
    <circle cx="334" cy="145" r="3" fill="#06B6D4"/>
    <!-- Gran Visor Holográfico AR translúcido neón cian/magenta -->
    <g filter="url(#neonGlowHead)">
      <!-- Panel de vidrio holográfico frontal envolvente (y=140 a y=185) -->
      <polygon points="190,145 322,145 315,185 285,190 256,182 227,190 197,185" 
               fill="#06B6D4" fill-opacity="0.35" stroke="#06B6D4" stroke-width="3"/>
      <!-- Retícula digital y datos HUD holográficos -->
      <circle cx="295" cy="165" r="10" stroke="#EC4899" stroke-width="2" fill="none"/>
      <line x1="280" y1="165" x2="310" y2="165" stroke="#EC4899" stroke-width="1.5"/>
      <line x1="295" y1="150" x2="295" y2="180" stroke="#EC4899" stroke-width="1.5"/>
      <!-- Barras de estado en visor izquierdo -->
      <rect x="205" y="155" width="22" height="3" fill="#06B6D4"/>
      <rect x="205" y="162" width="16" height="3" fill="#06B6D4"/>
      <rect x="205" y="169" width="28" height="3" fill="#EC4899"/>
    </g>
  </g>
</svg>'''
    }
]

for item in HEAD_ITEMS:
    with open(os.path.join(HEADS_DIR, f"{item['id']}.svg"), 'w', encoding='utf-8') as f:
        f.write(item['svg'])

print("Heads generated successfully.")

# ---------------------------------------------------------------------------
# 4. GENERATE FACES (4 expresiones modulares)
# ---------------------------------------------------------------------------
FACE_ITEMS = [
    {
        'id': 'face_focused', 'name': 'Concentrado', 'civ': 'Universal',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="faceGlow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 2: EXPRESIÓN FACIAL (Z-INDEX 30) - CONCENTRADO -->
  <g id="face-focused" filter="url(#faceGlow)">
    <!-- Cejas inclinadas hacia adentro con determinación -->
    <path d="M 195 152 L 236 164" stroke="#0F172A" stroke-width="5" stroke-linecap="round"/>
    <path d="M 317 152 L 276 164" stroke="#0F172A" stroke-width="5" stroke-linecap="round"/>
    <!-- Ojos firmes e intensos -->
    <!-- Ojo Izquierdo -->
    <ellipse cx="218" cy="172" rx="11" ry="13" fill="#0F172A"/>
    <circle cx="215" cy="168" r="4" fill="#FFFFFF"/>
    <circle cx="222" cy="176" r="2" fill="#FFFFFF"/>
    <!-- Ojo Derecho -->
    <ellipse cx="294" cy="172" rx="11" ry="13" fill="#0F172A"/>
    <circle cx="291" cy="168" r="4" fill="#FFFFFF"/>
    <circle cx="298" cy="176" r="2" fill="#FFFFFF"/>
    <!-- Destello de enfoque / concentración -->
    <polygon points="256,166 258,172 264,174 258,176 256,182 254,176 248,174 254,172" fill="#FBBF24"/>
  </g>
</svg>'''
    },
    {
        'id': 'face_confident', 'name': 'Confiado / Pícaro', 'civ': 'Universal',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="faceGlow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 2: EXPRESIÓN FACIAL (Z-INDEX 30) - CONFIADO -->
  <g id="face-confident" filter="url(#faceGlow)">
    <!-- Ceja izquierda arqueada confiada -->
    <path d="M 198 152 Q 220 144 238 156" stroke="#0F172A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    <!-- Ceja derecha pícara -->
    <path d="M 274 158 Q 294 150 314 156" stroke="#0F172A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    <!-- Ojo Izquierdo abierto brillante -->
    <ellipse cx="218" cy="172" rx="12" ry="14" fill="#0F172A"/>
    <circle cx="214" cy="167" r="5" fill="#FFFFFF"/>
    <circle cx="222" cy="177" r="2" fill="#FFFFFF"/>
    <!-- Ojo Derecho GUIÑADO (estrella de triunfo / wink) -->
    <path d="M 280 174 Q 295 162 310 174" stroke="#0F172A" stroke-width="5" fill="none" stroke-linecap="round"/>
    <!-- Estrella dorada de brillo en el guiño -->
    <polygon points="314,162 316,168 322,170 316,172 314,178 312,172 306,170 312,168" fill="#F59E0B"/>
    <!-- Sonrojo pícaro -->
    <ellipse cx="198" cy="184" rx="9" ry="5" fill="#FB7185" opacity="0.6"/>
    <ellipse cx="314" cy="184" rx="9" ry="5" fill="#FB7185" opacity="0.6"/>
  </g>
</svg>'''
    },
    {
        'id': 'face_surprised', 'name': 'Sorprendido', 'civ': 'Universal',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="faceGlow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 2: EXPRESIÓN FACIAL (Z-INDEX 30) - SORPRENDIDO -->
  <g id="face-surprised" filter="url(#faceGlow)">
    <!-- Cejas levantadas de asombro -->
    <path d="M 198 144 Q 218 134 238 146" stroke="#0F172A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    <path d="M 274 146 Q 294 134 314 144" stroke="#0F172A" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    <!-- Ojos redondos muy abiertos -->
    <!-- Ojo Izquierdo -->
    <circle cx="218" cy="170" r="14" fill="#0F172A"/>
    <circle cx="214" cy="165" r="6" fill="#FFFFFF"/>
    <circle cx="223" cy="174" r="3" fill="#FFFFFF"/>
    <!-- Ojo Derecho -->
    <circle cx="294" cy="170" r="14" fill="#0F172A"/>
    <circle cx="290" cy="165" r="6" fill="#FFFFFF"/>
    <circle cx="299" cy="174" r="3" fill="#FFFFFF"/>
    <!-- Detalle de sorpresa (boca/pico entreabierto) -->
    <ellipse cx="256" cy="198" rx="8" ry="10" fill="#78350F" stroke="#EA580C" stroke-width="2"/>
    <ellipse cx="256" cy="201" rx="5" ry="4" fill="#DC2626"/>
  </g>
</svg>'''
    },
    {
        'id': 'face_calm', 'name': 'Calmado / Zen', 'civ': 'Universal',
        'svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <filter id="faceGlow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>
  <!-- CAPA 2: EXPRESIÓN FACIAL (Z-INDEX 30) - CALMADO -->
  <g id="face-calm" filter="url(#faceGlow)">
    <!-- Ojos en arco sereno y feliz (^ ^) -->
    <path d="M 204 172 Q 218 158 232 172" stroke="#0F172A" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M 280 172 Q 294 158 308 172" stroke="#0F172A" stroke-width="5" fill="none" stroke-linecap="round"/>
    <!-- Cejas suaves relajadas -->
    <path d="M 206 150 Q 218 145 230 150" stroke="#475569" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M 282 150 Q 294 145 306 150" stroke="#475569" stroke-width="3" fill="none" stroke-linecap="round"/>
    <!-- Mejillas sonrojadas suaves y tiernas -->
    <ellipse cx="198" cy="180" rx="12" ry="7" fill="#FB7185" opacity="0.65"/>
    <ellipse cx="314" cy="180" rx="12" ry="7" fill="#FB7185" opacity="0.65"/>
    <!-- Pequeño brillo zen -->
    <circle cx="256" cy="165" r="3" fill="#38BDF8" opacity="0.8"/>
  </g>
</svg>'''
    }
]

for item in FACE_ITEMS:
    with open(os.path.join(FACES_DIR, f"{item['id']}.svg"), 'w', encoding='utf-8') as f:
        f.write(item['svg'])

print("Faces generated successfully.")

# ---------------------------------------------------------------------------
# 5. GENERATE CATALOG MANIFEST (catalog.json)
# ---------------------------------------------------------------------------
catalog = {
    "version": "1.0.0",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "canvas": {
        "width": 512,
        "height": 512,
        "format": "svg",
        "anchors": {
            "head_center": [256, 160],
            "eyes_beak_line": [256, 185],
            "torso_center": [256, 320],
            "feet_base": [256, 450]
        }
    },
    "layers_order": [
        {"layer": 0, "category": "body", "z_index": 10, "description": "Cuerpo base del pato"},
        {"layer": 1, "category": "clothes", "z_index": 20, "description": "Ropa y armaduras temáticas"},
        {"layer": 2, "category": "face", "z_index": 30, "description": "Expresiones faciales modulares"},
        {"layer": 3, "category": "head", "z_index": 40, "description": "Sombreros y accesorios de cabeza"}
    ],
    "civilizations": [
        "Cavernícola",
        "Egipto",
        "Grecia",
        "Roma",
        "Vikingo",
        "Samurái",
        "Medieval",
        "Pirata",
        "Steampunk",
        "Cyberpunk 2099"
    ],
    "items": []
}

# Add bodies
for body_id, data in BODY_PALETTES.items():
    catalog["items"].append({
        "id": body_id,
        "name": data["name"],
        "category": "body",
        "civilization": "Universal",
        "z_index": 10,
        "file": f"bodies/{body_id}.svg",
        "path": f"quiz_games/avatars/bodies/{body_id}.svg",
        "preview_color": data["main"]
    })

# Add clothes
for item in CLOTHES_ITEMS:
    catalog["items"].append({
        "id": item["id"],
        "name": item["name"],
        "category": "clothes",
        "civilization": item["civ"],
        "z_index": 20,
        "file": f"clothes/{item['id']}.svg",
        "path": f"quiz_games/avatars/clothes/{item['id']}.svg"
    })

# Add faces
for item in FACE_ITEMS:
    catalog["items"].append({
        "id": item["id"],
        "name": item["name"],
        "category": "face",
        "civilization": item["civ"],
        "z_index": 30,
        "file": f"faces/{item['id']}.svg",
        "path": f"quiz_games/avatars/faces/{item['id']}.svg"
    })

# Add heads
for item in HEAD_ITEMS:
    catalog["items"].append({
        "id": item["id"],
        "name": item["name"],
        "category": "head",
        "civilization": item["civ"],
        "z_index": 40,
        "file": f"heads/{item['id']}.svg",
        "path": f"quiz_games/avatars/heads/{item['id']}.svg"
    })

catalog_path = os.path.join(AVATARS_DIR, 'catalog.json')
with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"Catalog manifest generated at {catalog_path} with {len(catalog['items'])} items.")
