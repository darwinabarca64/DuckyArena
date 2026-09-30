# 🚀 GUÍA DE INICIO Y MANUAL OPERATIVO — PARTE 1: MÓDULO QUIZZES (QUIZARENAS)

Este documento es la guía técnica de referencia integral para el arranque del entorno local, la arquitectura del subsistema **quizzes** y la resolución total de la matriz de riesgos, experiencia de usuario (UX/DX) y deuda técnica previa a la activación del motor de juego multijugador (Parte 2).

---

## 🛠️ 1. ENTORNO Y ARRANQUE LOCAL (WINDOWS / GIT BASH & UV)

### A. Navegación a la raíz del proyecto
```bash
cd /c/Users/Dar/Desktop/Python/DuckyQuizzArena
ls manage.py
```

### B. Aislamiento y Entorno Virtual (Python 3.11)
```bash
uv python install 3.11
rm -rf venv
uv venv venv --python 3.11
source venv/Scripts/activate
```
*(Verificar que aparezca el prefijo `(venv)` en la terminal).*

### C. Instalación de Dependencias
```bash
uv pip install -r requirements.txt
```

### D. Sincronización de Base de Datos y Verificación
```bash
python manage.py makemigrations quizzes quiz_games
python manage.py migrate
python manage.py check
```

### E. Suite de Pruebas Automatizadas (13 Tests de Integración)
```bash
python manage.py test
```

### F. Creación de Superusuario / Administrador
```bash
python manage.py createsuperuser
```

### G. Ejecución del Servidor
```bash
python manage.py runserver
```
Acceso Web:
- **Catálogo de Cuestionarios:** [http://localhost:8000/quizzes/](http://localhost:8000/quizzes/)
- **Panel de Administración:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🧩 2. ARQUITECTURA TÉCNICA DEL MÓDULO `quizzes`

La aplicación `quizzes` implementa la creación pedagógica, parametrización de tiempos y puntajes, y ciclo de vida de los cuestionarios que serán consumidos por el motor de salas en tiempo real (`quiz_games`).

### Modelos de Datos (ORM Relacional)
1. **`Quiz`** ([quizzes/models.py](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/models.py#L5)):
   - Campos: `title` (máx. 200 caracteres), `description` (texto explicativo), `creator` (`settings.AUTH_USER_MODEL`, `on_delete=CASCADE`, `related_name='quizzes'`), `is_published` (booleano), `created_at` y `updated_at`.
   - Ordenamiento por defecto: `['-created_at']`.
2. **`Question`** ([quizzes/models.py](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/models.py#L27)):
   - Campos: `quiz` (FK a `Quiz`, `on_delete=CASCADE`, `related_name='questions'`), `text` (enunciado), `time_limit` (tiempo en segundos, por defecto 30), `points` (puntos base, por defecto 1000), `order` (secuencia visual).
   - Ordenamiento: `['order']`.
3. **`Answer`** ([quizzes/models.py](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/models.py#L48)):
   - Campos: `question` (FK a `Question`, `on_delete=CASCADE`, `related_name='answers'`), `text` (texto de la opción), `is_correct` (booleano), `order`.
   - Ordenamiento: `['order']`.

### Formularios y Validaciones de Negocio (`quizzes/forms.py`)
- **`QuizForm`**: Controla metadatos del cuestionario. Bloquea en su método `clean()` la activación de `is_published=True` si el cuestionario no cuenta con preguntas en base de datos.
- **`QuestionForm`**: Valida que `time_limit` se encuentre en el rango de 5 a 300 segundos y que `points` sea un entero positivo mayor a 0.
- **`BaseAnswerFormSet`**: Formset en línea que exige estrictamente:
  1. Cada pregunta debe contener entre 2 y 6 respuestas completadas.
  2. Debe existir **exactamente 1 respuesta** marcada como correcta (`is_correct=True`).

### Vistas y Control de Acceso (`quizzes/views.py`)
- **Mixins de Autorización**:
  * `TeacherRequiredMixin`: Requiere autenticación y rol `TEACHER` (`request.user.profile.role == 'TEACHER'` o superuser).
  * `QuizOwnerRequiredMixin`: Exige que el usuario sea docente y el creador legítimo del cuestionario (`quiz.creator == request.user`).
- **Controladores Principales**:
  * `QuizListView`: Catálogo de cuestionarios publicados para todos los usuarios y sección dedicada "Mis Cuestionarios" para profesores.
  * `QuizDetailView`: Vista del cuestionario con estadísticas acumuladas (preguntas, tiempo, puntos) y previsualización neutral protegida contra fugas de información.
  * `QuizCreateView` / `QuizUpdateView`: Vistas transaccionales con `QuizFormsetMixin` para el guardado atómico de Quiz, Preguntas y Alternativas.
  * `QuizDeleteView`: Eliminación segura con confirmación.
  * `QuizTogglePublishView`: Endpoint `POST` con validación completa de integridad pedagógica antes de publicar.

---

## 🛡️ 3. RESOLUCIÓN DE LA MATRIZ DE RIESGOS Y MEJORAS UX/DX

Durante la auditoría técnica se aplicaron parches definitivos para garantizar máxima seguridad y robustez:

| Riesgo / Deuda Auditada | Causa Raíz | Solución Implementada y Blindaje | Archivos Modificados |
| :--- | :--- | :--- | :--- |
| **Middlewares de Seguridad** | Omisión de `CsrfViewMiddleware` y `XFrameOptionsMiddleware` en `settings.py`. | Se incorporaron ambos middlewares en el orden canónico de Django, protegiendo todas las rutas contra ataques CSRF y clickjacking. | [quizz_project/settings.py](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizz_project/settings.py#L31-L39) |
| **Sincronización de Formsets Dinámicos** | Al eliminar preguntas o alternativas no guardadas, se producían huecos de indexación no secuenciales en el payload POST. | Se implementaron las funciones `reindexAnswers()` y `reindexAllQuestions()` en JavaScript, reindexando atómicamente prefijos, nombres, IDs y actualizando con precisión `TOTAL_FORMS`. | [quizzes/templates/quizzes/quiz_form.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_form.html#L678-L800) |
| **Feedback de Errores Inline** | Los errores globales de `BaseAnswerFormSet` no se mostraban en la tarjeta de la pregunta en servidor. | Se agregó el bloque `{% if ans_fs.non_form_errors %}` dentro del contenedor de respuestas de cada pregunta, mostrando advertencias contextuales inmediatas. | [quizzes/templates/quizzes/quiz_form.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_form.html#L464-L472) |
| **Cero Leaks en Estudiantes y Badges 3D (A, B, C, D)** | Prevenir que el frontend revele respuestas correctas y homogeneizar visualmente las opciones con las letras del arte gráfico 3D. | `quiz_detail.html` y `quiz_form.html` renderizan tarjetas y badges 3D interactivos (**A**, **B**, **C**, **D**, **E**, **F**) con gradientes vibrantes Kahoot, sin referencias a `is_correct` ni clases filtradas en el DOM del estudiante. | [quiz_detail.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_detail.html#L425-L440), [quiz_form.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_form.html#L770-L790) |
| **Buscador Reactivo y Ergonómico** | El texto estático "BUSCAR:" se superponía con el placeholder y no se limpiaba al escribir. | Se sustituyó el texto estático por un icono SVG de lupa integrado con `pointer-events: none`, padding refinado y limpieza en tiempo real del filtro al escribir. | [quiz_list.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_list.html#L470-L490) |
| **Hero Banner Interactivo con Botones en Español** | La imagen original contenía botones estáticos en inglés incrustados que no eran navegables. | Se generó un arte 3D limpio sin botones grabados, integrando sobre la imagen un dock HTML con paleta cósmica púrpura translúcida armonizada y botones de acción limpios en español (`¡Juega en Vivo!`, `¡Gana Puntos!`, `¡Diversión Total!`) que navegan a secciones activas y creación. | [quiz_list.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_list.html#L420-L460), [hero_banner.jpg](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/static/assets/hero_banner.jpg) |
| **Diseño y Ergonomía Mobile-First** | Desbordamiento de tarjetas, grid estático y barras de acción no optimizadas en pantallas táctiles y móviles. | Implementación de header ultra-compacto con menú hamburguesa animado, media queries responsivas (`<900px`, `<768px`, `<480px`), flex-wrap en alternativas de respuestas, grids de 1 columna y barra dock fija táctil. | [base.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/templates/base.html#L405-L460), [quiz_list.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_list.html#L355-L405), [quiz_form.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_form.html#L340-L405), [quiz_detail.html](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quizzes/templates/quizzes/quiz_detail.html#L300-L350) |
| **Integridad Relacional ON DELETE** | Prevenir borrados accidentales de cuestionarios con historial de partidas jugadas. | Se constató la protección con `on_delete=models.PROTECT` en `Game.quiz` y `PlayerAnswer.question`, impidiendo borrar quizzes con partidas asociadas. | [quiz_games/models.py](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/quiz_games/models.py#L13-L18) |

---

## 🔒 4. ESTADO DE BLOQUEO Y PRE-CONDICIONES PARA PARTE 2

> [!IMPORTANT]
> **ESTADO ACTUAL:** La Parte 1 (Módulo Quizzes) se encuentra **100% completada, auditada, corregida y blindada**. No se avanzará a la Parte 2 hasta recibir la orden explícita del usuario.

### Siguientes pasos al autorizar Parte 2 (`quiz_games`):
1. **Conexión de Sala:** Enlazar el botón "Iniciar Sala" de `quiz_detail.html` con el endpoint de creación de partida (`quiz_games:create_game`).
2. **Máquina de Estados de Partida:** Implementar el ciclo `LOBBY` -> `RUNNING` -> `FINISHED` / `CANCELLED`.
3. **PIN y Acceso de Jugadores:** Activación de generación y validación de códigos de 6 dígitos.
4. **Motor de Evaluación en Tiempo Real:** Evaluación server-side, cálculo de rachas y distribución de Ducky Coins.
