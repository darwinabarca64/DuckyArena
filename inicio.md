# 🚀 GUÍA DE INICIO Y MANUAL OPERATIVO — PARTE 1: MÓDULO QUIZZES (DUCKY QUIZ ARENAS)

Este documento es la guía técnica de referencia rápida para el arranque del entorno local y la comprensión integral del subsistema **quizzes** (Equipo 1). No reemplaza el README.md final, sino que documenta el estado operativo consolidado de la Parte 1 antes de conectar el motor de juego (Parte 2).

## 🛠️ ENTORNO Y ARRANQUE LOCAL (WINDOWS / GIT BASH & UV)

### 1. Navegación a la raíz del proyecto
```bash
cd /c/Users/Dar/Desktop/Python/DuckyQuizzArena
ls manage.py
```

### 2. Aislamiento y Entorno Virtual (Python 3.11)
```bash
uv python install 3.11
rm -rf venv
uv venv venv --python 3.11
source venv/Scripts/activate
```
*(Verificar que aparezca el prefijo `(venv)` en la consola).*

### 3. Instalación de Dependencias
```bash
uv pip install -r requirements.txt
```

### 4. Sincronización de Base de Datos y Verificación
```bash
python manage.py makemigrations quizzes quiz_games
python manage.py migrate
python manage.py check
```

### 5. Creación de Superusuario / Administrador
```bash
python manage.py createsuperuser
```

### 6. Ejecución del Servidor
```bash
python manage.py runserver
```
Acceso Web:
- Aplicación: http://localhost:8000/quizzes/
- Panel de Administración: http://localhost:8000/admin/

---

## 🧩 ARQUITECTURA TÉCNICA DE LA PARTE 1: APP `quizzes`

La aplicación `quizzes` gestiona la creación, parametrización pedagógica y ciclo de vida de los cuestionarios que alimentarán las partidas en tiempo real de `quiz_games`.

### 1. Modelos de Datos (ORM Relacional)
- **Quiz**: Representa la entidad central del cuestionario.
  * Campos: `title` (200 caracteres), `description` (texto explicativo), `creator` (FK hacia `settings.AUTH_USER_MODEL` con CASCADE), `is_published` (booleano), marcas de tiempo `created_at` y `updated_at`.
  * Ordenamiento predeterminado: `ordering = ['-created_at']`.
- **Question**: Representa cada enunciado o ítem de evaluación.
  * Campos: `quiz` (FK hacia `Quiz` con CASCADE y `related_name='questions'`), `text` (enunciado), `time_limit` (tiempo en segundos, por defecto 30), `points` (puntuación base, por defecto 1000), `order` (secuencia visual).
  * Ordenamiento: `ordering = ['order']`.
- **Answer**: Alternativas de opción múltiple vinculadas a una pregunta.
  * Campos: `question` (FK hacia `Question` con CASCADE y `related_name='answers'`), `text` (texto de la opción), `is_correct` (booleano), `order`.
  * Ordenamiento: `ordering = ['order']`.

### 2. Capa de Formularios y Validaciones (`quizzes/forms.py`)
- **QuizForm**: Controla la metadata del cuestionario. Bloquea mediante validación en `clean()` la activación de `is_published=True` si el cuestionario no cuenta con al menos una pregunta en base de datos. Exige al menos 5 caracteres en el título.
- **QuestionForm**: Valida rangos pedagógicos: `time_limit` entre 5 y 300 segundos, y `points` estrictamente mayores a 0.
- **AnswerForm**: Estiliza las opciones con widgets Ducky Arena.
- **BaseAnswerFormSet & AnswerFormSet**: Formset en línea que audita dos reglas inviolables:
  * Cada pregunta debe contener entre 2 y 6 respuestas completadas.
  * Debe existir EXACTAMENTE 1 respuesta con `is_correct=True`.

### 3. Vistas y Control de Acceso (`quizzes/views.py`)
- **Mixins de Permisos**:
  * `TeacherRequiredMixin`: Exige que `request.user.profile.role == 'TEACHER'`.
  * `QuizOwnerRequiredMixin`: Exige que el usuario sea profesor y propietario (`quiz.creator == request.user`).
- **Catálogo de Vistas**:
  * `QuizListView`: Muestra cuestionarios publicados a toda la comunidad y sección de gestión propia ("Mis Cuestionarios") para profesores.
  * `QuizDetailView`: Ficha pedagógica con métricas agregadas (total preguntas, tiempo acumulado, puntuación potencial). No expone respuestas correctas.
  * `QuizCreateView`: Creación transaccional vinculando automáticamente el autor autenticado.
  * `QuizUpdateView`: Edición controlada exclusiva para el profesor creador.
  * `QuizDeleteView`: Eliminación segura con confirmación.
  * `QuizTogglePublishView`: Endpoint vía POST que valida que todas las preguntas cumplan la regla 2-6 respuestas y 1 correcta antes de otorgar el estado publicado.

### 4. Rutas Registradas (`quizzes/urls.py`)
Prefijo global: `/quizzes/`
- `''` -> `quizzes:quiz_list`
- `'<int:pk>/'` -> `quizzes:quiz_detail`
- `'create/'` -> `quizzes:quiz_create`
- `'<int:pk>/edit/'` -> `quizzes:quiz_edit`
- `'<int:pk>/delete/'` -> `quizzes:quiz_delete`
- `'<int:pk>/toggle-publish/'` -> `quizzes:quiz_toggle_publish`

### 5. Plantillas y Experiencia de Usuario (UI/UX Ducky Arena)
- Herencia estricta de `base.html` del Equipo 0.
- `quiz_list.html`: Cuadrícula responsiva con tarjetas oscuras, acentos dorados, insignias de estado (Borrador/Publicado), buscador interactivo y acceso rápido a acciones CRUD.
- `quiz_detail.html`: Panel estadístico de cuestionario y desglose de preguntas sin filtración de respuestas.
- `quiz_form.html`: Editor dinámico con JavaScript para inserción y remoción de alternativas, mutua exclusión de la opción correcta y ajuste en tiempo real de `TOTAL_FORMS`.
- `quiz_confirm_delete.html`: Modal/tarjeta de confirmación para evitar destrucciones no deseadas.

### 6. Administración Django (`quizzes/admin.py`)
- `QuestionInline` tabular dentro de `QuizAdmin`.
- `AnswerInline` tabular dentro de `QuestionAdmin`.
- Consultas optimizadas con `select_related` y agregación `Count('questions')` para prevenir problemas de rendimiento N+1.

---

## ⏭️ PREPARACIÓN PARA LA PARTE 2 (`quiz_games`)
Al finalizar y validar la Parte 1, el proyecto queda habilitado para desplegar:
1. Conexión del botón "Iniciar Sala" de `quiz_detail.html` con `quiz_games:create_game`.
2. Máquina de estados (`LOBBY`, `RUNNING`, `FINISHED`, `CANCELLED`).
3. Generación y validación de PIN de 6 dígitos.
4. Lógica de evaluación server-side y cálculo transaccional de rachas y puntajes.
