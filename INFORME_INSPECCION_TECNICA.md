# INFORME DE INSPECCION TECNICA Y ARQUITECTURA
**Proyecto:** Ducky Quiz Arenas (QuizArenas)  
**Modulo:** Diagnostico y Auditoria Previa a Cambios Estructurales  
**Fecha:** 2026-10-01  
**Estado:** Inspeccion Estricta en Modo Solo Lectura (Completada)

---

## RESUMEN EJECUTIVO
Este documento recopila el estado tecnico actual del repositorio para guiar la implementacion controlada de 5 cambios estructurales en la plataforma QuizArenas. Se detallan los archivos involucrados, estado real encontrado y los puntos exactos de conexion e intervencion para asegurar cero regresiones.

---

## 1. ESTADO DE INFRAESTRUCTURA ASGI Y ENRUTAMIENTO

### Diagnostico y Estado Encontrado
- **Configuracion Django (`quizz_project/settings.py`):**
  - La aplicacion se ejecuta bajo arquitectura WSGI clasica: `WSGI_APPLICATION = 'quizz_project.wsgi.application'`.
  - La lista `INSTALLED_APPS` no incluye `daphne` ni `channels`.
  - No existen variables de configuracion para `ASGI_APPLICATION` ni `CHANNEL_LAYERS`.
- **Punto de Entrada ASGI (`quizz_project/asgi.py`):**
  - El archivo `quizz_project/asgi.py` no existe en el proyecto. Solo existe `quizz_project/wsgi.py`.
- **Capa de Enrutamiento y Consumidores (`quiz_games/`):**
  - No existen archivos `routing.py` ni `consumers.py` dentro de la app `quiz_games/`.
- **Entorno Virtual y Dependencias (`requirements.txt`):**
  - Los paquetes `channels` y `daphne` no estan instalados en el entorno Python virtual (la prueba de importacion arroja `ModuleNotFoundError`).
  - El archivo `requirements.txt` actual solo declara:
    - Django==4.2.11
    - qrcode==7.4.2
    - pillow==10.0.0

### Puntos Exactos de Conexion
1. **`requirements.txt`:** Agregar las dependencias `channels` y `daphne`.
2. **`quizz_project/asgi.py`:** Crear el archivo punto de entrada ASGI con `ProtocolTypeRouter` y `URLRouter` apuntando a `quiz_games.routing.websocket_urlpatterns`.
3. **`quizz_project/settings.py`:**
   - Registrar `'daphne'` como la primera aplicacion en `INSTALLED_APPS`.
   - Definir `ASGI_APPLICATION = 'quizz_project.asgi.application'`.
   - Configurar `CHANNEL_LAYERS` con backend InMemoryChannelLayer o Redis.
4. **`quiz_games/routing.py` y `quiz_games/consumers.py`:** Crear los consumidores WebSocket para sincronizacion en tiempo real de lobby, preguntas y conteo de respuestas.

---

## 2. ARQUITECTURA ACTUAL DE AUDIO

### Diagnostico y Estado Encontrado
- **Ubicacion del Motor de Sonido:**
  - El motor de audio reside en `quiz_games/templates/quiz_games/audio_engine.html`.
  - Esta implementado mediante la clase JavaScript `DuckyAudioEngine` utilizando Web Audio API nativa (`window.AudioContext` o `window.webkitAudioContext`).
  - No utiliza archivos de audio externos (mp3/wav), sino osciladores sintetizados en tiempo real.
  - La preferencia de audio silencioso/activo se persiste en `localStorage` con la clave `ducky_audio_muted`.
  - Dispone de un componente de interfaz grafica flotante (`#sound-control-container`) con boton para alternar sonido.

### Catalogo de Funciones de Sonido y Eventos Disparadores
1. **`playTone(freq, type, duration, delay)`:**
   - Metodo base que crea un oscilador (`createOscillator`) y nodo de ganancia (`createGain`) con caida exponencial de volumen (`exponentialRampToValueAtTime`).
2. **`playCorrect()`:**
   - Reproduce un acorde ascendente en ondas de tipo triangular (`triangle`): C5 (523.25 Hz), E5 (659.25 Hz), G5 (783.99 Hz).
   - Se dispara en `quiz_games/templates/quiz_games/game_player_play.html` dentro de la respuesta AJAX cuando la respuesta enviada es correcta.
3. **`playIncorrect()`:**
   - Reproduce un tono grave descendente en ondas de tipo diente de sierra (`sawtooth`): 330 Hz y 240 Hz.
   - Se dispara en `quiz_games/templates/quiz_games/game_player_play.html` cuando la respuesta enviada es incorrecta.
4. **`playCountdownTick()`:**
   - Reproduce un tic suave de reloj en onda senoidal (`sine`): 880 Hz durante 0.05 segundos.
   - Se dispara en `quiz_games/templates/quiz_games/game_host_play.html` cuando el temporizador entra en los ultimos 5 segundos (`timeLeft <= 5 && timeLeft > 0`).
5. **`playFanfare()`:**
   - Reproduce una fanfarria de victoria en onda cuadrada (`square`): secuencia de notas C5, C5, C5, E5, G5.
   - Se dispara en `quiz_games/templates/quiz_games/game_leaderboard.html` al cargar la pantalla de podio o en el primer clic de interaccion.

### Puntos Exactos de Conexion
- Centralizar la carga del script `audio_engine.html` en la plantilla base `templates/base.html` o en un layout comun de juego para evitar directivas `include` repetidas.
- Vincular los disparadores de audio a eventos entrantes por WebSocket (inicio de juego, bloqueo de opciones, revelacion de podio).

---

## 3. DESACOPLAMIENTO DE PANTALLAS DE CIERRE

### Diagnostico y Estado Encontrado
- **Controladores en `quiz_games/views.py`:**
  - **`game_leaderboard(request, code)` (lineas 407-460):**
    - Vista orientada al anfitrion y participantes para consultar el cierre general.
    - Valida que el juego este en estado `FINISHED`.
    - Ordena la clasificacion completa mediante `order_by('-score', '-correct_answers', 'joined_at')`.
    - Extrae explicitamente: `first_place`, `second_place`, `third_place` y `rest_players` (del puesto 4 en adelante).
    - Realiza agregaciones ORM con `Max('score')`, `Avg('correct_answers')` y `Count('id')`.
    - Renderiza la plantilla `quiz_games/game_leaderboard.html`.
  - **`game_player_results(request, code)` (lineas 463-508):**
    - Vista personal para el estudiante individual.
    - Calcula la posicion del jugador (`position`), el porcentaje de precision (`accuracy`) y asigna la medalla correspondiente (`ORO`, `PLATA`, `BRONCE` o badge de puesto general).
    - Renderiza la plantilla `quiz_games/game_player_results.html`.
  - **`export_game_results_csv(request, code)` (lineas 587-625):**
    - Endpoint exclusivo del anfitrion para descargar la tabla de notas completa en formato CSV con BOM UTF-8.
- **Plantillas Involucradas:**
  - `game_leaderboard.html`: Integra en un solo archivo el encabezado, las tarjetas de metricas globales, el podio olimpico Top 3 visual, la tabla de posiciones restantes y los botones de accion.
  - `game_player_results.html`: Muestra de forma independiente la tarjeta de felicitacion del jugador, barra de precision y 4 baldosas de resumen (Puntos, Aciertos, Racha, Posicion).

### Variables de Contexto Identificadas
- **En `game_leaderboard`:**
  - `game`: Objeto Game con informacion de la sala y PIN.
  - `quiz`: Objeto Quiz asociado.
  - `ranking`: Lista completa de objetos GamePlayer ordenados.
  - `first_place`, `second_place`, `third_place`: Objetos individuales del Top 3.
  - `rest_players`: Lista de jugadores a partir del 4to puesto.
  - `total_questions`: Total de preguntas del cuestionario.
  - `max_score`: Puntuacion maxima obtenida en la sesion.
  - `avg_correct`: Promedio de respuestas correctas.
  - `total_participants`: Conteo total de jugadores registrados.
  - `is_host`: Booleano que indica si el usuario actual es el anfitrion.
- **En `game_player_results`:**
  - `game`, `quiz`, `player_entry`: Instancia de GamePlayer del usuario actual.
  - `position`: Numero entero con el puesto general obtenido.
  - `total_players`: Total de participantes en la sala.
  - `total_questions`: Numero de preguntas evaluadas.
  - `accuracy`: Porcentaje numerico de precision.
  - `medal`: Diccionario con tipo, icono y clase de medalla si alcanzo podio.

### Puntos Exactos de Conexion
- Mantener la separacion entre la pantalla de celebracion ceremonial (Podio Top 3 del docente) y el resumen individual del estudiante.
- Implementar la transicion automatica hacia estas vistas al emitir el evento WebSocket de fin de partida.

---

## 4. LAYOUT DE RANKING Y DUCKYCOINS (DESKTOP VS MOBILE)

### Diagnostico y Estado Encontrado
- **Nomenclatura y Modelo Economico:**
  - En la barra de navegacion principal (`templates/base.html`, linea 593), el saldo del usuario se visualiza correctamente como DuckyCoins usando la etiqueta `{{ user.profile.ducky_coins }} DC`.
  - En las pantallas de juego activo (`game_player_play.html`, linea 286), la puntuacion todavia se presenta bajo la nomenclatura tradicional de puntos: `⭐ <span id="total-score">{{ player_entry.score }}</span> pts`.
- **Estructura de Layout Actual:**
  - **Vista del Jugador (`game_player_play.html`):** Utiliza un contenedor centrado `.mobile-play-wrapper` con `max-width: 640px` y una franja superior `.player-stats-strip` donde agrupa racha, puntuacion y numero de pregunta en disposicion flexbox horizontal.
  - **Vista del Docente (`game_host_play.html`):** Utiliza un contenedor `.host-play-container` con `max-width: 1100px`. Durante la presentacion de la pregunta no muestra ranking lateral en tiempo real (las posiciones solo se visualizan al abrir el modal de desglose).

### Puntos Exactos de Conexion
1. **Estandarizacion de Nomenclatura:** Homogeneizar los marcadores de juego para mostrar icono y nombre oficial `DuckyCoins (DC)` junto a la racha activa.
2. **Adaptacion Escritorio (Desktop):** Modificar los contenedores principales a una rejilla CSS (`grid-template-columns: 1fr 300px; gap: 1.5rem;`) que aloje una barra lateral fija con el Top 5 en vivo y movimientos de posiciones.
3. **Adaptacion Movil (Mobile):** Incorporar una barra inferior fija (`position: fixed; bottom: 0; left: 0; right: 0; z-index: 100; backdrop-filter: blur(10px);`) optimizada para pulgares, mostrando racha, DuckyCoins ganadas en la pregunta y puesto en vivo.

---

## 5. DIAGNOSTICO DE UX MOVIL (PULL-TO-REFRESH Y DESPLAZAMIENTO)

### Diagnostico y Estado Encontrado
- **Etiqueta Viewport (`templates/base.html`, linea 6):**
  - Configuracion actual: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
  - Deficiencia: No incluye `viewport-fit=cover`, `maximum-scale=1.0` ni `user-scalable=no`. Esto permite gestos de pellizco/zoom accidentales y no aprovecha las areas seguras de pantalla (safe areas) en dispositivos moviles modernos.
- **Pull-to-Refresh y Rebote Tactil:**
  - No existe ninguna regla CSS que declare `overscroll-behavior` o `touch-action` en `body`, `html` ni en contenedores de juego.
  - En navegadores moviles (Chrome/Safari), deslizar hacia abajo en la parte superior desencadena la recarga de pagina no deseada en plena partida en vivo.
- **Desplazamiento Horizontal Involuntario:**
  - En `templates/base.html` (linea 74), existe la regla `body { overflow-x: hidden; }` que oculta el desbordamiento visual pero no elimina las causas de desborde interno.
  - El contenedor principal `.main-content` posee paddings laterales de `1.5rem` que, combinados con elementos sin `box-sizing: border-box` estricto o tablas sin contenedor de desplazamiento aislado, generan desbordes en resoluciones menores a 380px.

### Puntos Exactos de Conexion
1. **Actualizacion de Viewport (`templates/base.html`):**
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
   ```
2. **Reglas CSS Antidesborde y Antibloqueo (`templates/base.html` y estilos de juego):**
   ```css
   html, body {
       overscroll-behavior-y: contain;
       touch-action: manipulation;
       -webkit-tap-highlight-color: transparent;
   }
   .mobile-play-wrapper, .host-play-container {
       width: 100%;
       max-width: 100vw;
       box-sizing: border-box;
   }
   ```

---

## MATRIZ RESUMEN DE INTERVENCIONES

| ID | Modulo / Area | Archivos a Modificar / Crear | Impacto Arquitectonico |
| :--- | :--- | :--- | :--- |
| **01** | Infraestructura ASGI | `requirements.txt`, `quizz_project/settings.py`, `quizz_project/asgi.py`, `quiz_games/routing.py`, `quiz_games/consumers.py` | Migracion de polling HTTP a WebSockets ASGI bidireccional de baja latencia. |
| **02** | Motor de Audio | `quiz_games/templates/quiz_games/audio_engine.html`, `templates/base.html` | Centralizacion y enlace directo con eventos en tiempo real. |
| **03** | Pantallas de Cierre | `quiz_games/views.py`, `game_leaderboard.html`, `game_player_results.html` | Desacoplamiento de ceremonia de podio Top 3 y reporte individual. |
| **04** | Layout Ranking / DC | `game_player_play.html`, `game_host_play.html` | Unificacion de DuckyCoins y division barra lateral (desktop) / dock inferior (mobile). |
| **05** | Optimizacion UX Movil | `templates/base.html`, CSS de `quiz_games` | Bloqueo de pull-to-refresh, eliminacion de overflow y bloqueo de zoom accidental. |

---
**Fin del informe de inspeccion.**
