# Blueprint de arquitectura: DuckyQuizzArena

Referencia del estado actual del repositorio. Todas las rutas de este documento son relativas a la raiz del proyecto, es decir, la carpeta que contiene `manage.py`.

## 1. Arquitectura general

Es una aplicacion Django monolitica con:

- Proyecto Django: `quizz_project`.
- Aplicacion principal: `quizz_app`.
- SQLite local: `db.sqlite3`.
- Contenido inicial de quizzes en JSON: `data/quizzes.json`.
- HTML renderizado en servidor con plantillas Django.
- JavaScript y CSS estaticos servidos desde `quizz_app/static`.
- Autenticacion basada en el sistema integrado de usuarios de Django.

### Arbol de carpetas y archivos clave

```text
DuckyQuizzArena/
├── manage.py                         CLI de Django; fija DJANGO_SETTINGS_MODULE y ejecuta comandos.
├── db.sqlite3                        Base de datos SQLite local.
├── requirements.txt                  Dependencias Python del proyecto.
├── setup.py                          Metadatos/configuracion de instalacion.
├── run.bat                           Script de arranque para Windows.
├── run.sh                            Script de arranque para Unix.
├── README.md                         Guia general, instalacion y uso.
├── setup.md                          Guia ampliada de configuracion y comprobaciones.
├── inicio.md                         Notas iniciales del proyecto.
├── IMPLEMENTATION_SUMMARY.md         Resumen de funcionalidades implementadas.
├── architecture_blueprint.md         Este mapa tecnico.
├── questions.json                    Banco JSON alternativo; no lo consume load_quizzes.
├── data/
│   └── quizzes.json                  Fuente que consume load_quizzes.
├── quizz_project/
│   ├── __init__.py                   Marca el paquete Python del proyecto.
│   ├── settings.py                   Apps, middleware, BD, plantillas, estaticos, idioma y login.
│   ├── urls.py                       Rutas raiz: /admin/ y delegacion a quizz_app.urls.
│   └── wsgi.py                       Punto de entrada WSGI para despliegue.
└── quizz_app/
    ├── __init__.py                   Inicializa la app y declara QuizzAppConfig por compatibilidad.
    ├── apps.py                       Define la configuracion de la app Django.
    ├── admin.py                      Registra modelos en el admin.
    ├── models.py                     Modelos, relaciones, ordenamientos y codigos automaticos.
    ├── urls.py                       Mapa de rutas HTTP de la aplicacion.
    ├── views.py                      Autenticacion, catalogo, quizzes, resultados y modo live.
    ├── tests.py                      Tests de modelos, autenticacion, resultados y HTML.
    ├── migrations/
    │   ├── __init__.py               Paquete de migraciones.
    │   ├── 0001_initial.py           Quiz, UserProfile, QuizResult y QuizEnrollment.
    │   ├── 0002_livesession_liveparticipant.py
    │   │                                LiveSession y LiveParticipant.
    │   ├── 0003_quizresult_timing_metrics.py
    │   │                                quiz_name, question_times y promedio de tiempo.
    │   └── 0004_category.py           Category y unicidad por profesor.
    ├── management/
    │   ├── __init__.py               Paquete de comandos de gestion.
    │   └── commands/
    │       ├── __init__.py           Paquete descubrible por Django.
    │       ├── load_quizzes.py       Importa JSON de data/ a Quiz.
    │       └── create_test_users.py  Crea estudiantes de desarrollo.
    ├── templates/
    │   ├── base.html                 Layout padre, navegacion, mensajes y carga de assets.
    │   ├── index.html                Catalogo de quizzes.
    │   ├── quiz.html                 Formulario normal, navegacion y envio AJAX.
    │   ├── results.html               Resultado persistido y detalle de respuestas.
    │   ├── leaderboard.html            Top de resultados de un quiz.
    │   ├── my_scores.html              Historial del estudiante.
    │   ├── login.html                  Inicio de sesion.
    │   ├── register.html               Registro; crea perfil estudiante.
    │   ├── teacher_dashboard.html      Gestion y resumen de quizzes del profesor.
    │   ├── teacher_statistics.html     Estadisticas agregadas del profesor.
    │   ├── create_quiz.html             Formulario de creacion.
    │   ├── edit_quiz.html               Formulario de edicion.
    │   ├── delete_quiz.html             Confirmacion de borrado.
    │   ├── quiz_students.html            Resultados de alumnos de un quiz.
    │   ├── manage_categories.html        CRUD de categorias del profesor.
    │   ├── join_live_session.html        Entrada a una sesion live.
    │   ├── live_quiz.html                Formulario del quiz live.
    │   ├── live_results.html              Resultado de un participante live.
    │   └── live_session_manage.html      Panel de control del profesor para live.
    └── static/
        ├── css/style.css              Estilos globales y responsive.
        └── js/main.js                 JS global; animaciones de tarjetas.
```

### Conexiones de configuracion

1. `manage.py` establece `DJANGO_SETTINGS_MODULE=quizz_project.settings`.
2. `settings.py` registra las apps Django incorporadas y `quizz_app`, usa `db.sqlite3`, busca plantillas en `quizz_app/templates` y estaticos en `quizz_app/static`.
3. `quizz_project/urls.py` publica `/admin/` y monta `quizz_app.urls` en `/`.
4. `quizz_app/urls.py` asigna rutas a funciones de `views.py` y define el namespace `quizz_app`.
5. `base.html` es la plantilla padre; las demas paginas heredan su navegacion, CSS, notificaciones, footer y `main.js`.
6. `admin.py` registra `UserProfile`, `Category`, `Quiz`, `QuizEnrollment` y `QuizResult`. Los modelos live existen, pero no estan registrados en admin.

`settings.py` usa `DEBUG=True`, `ALLOWED_HOSTS=['*']`, `LANGUAGE_CODE='es-es'`, `TIME_ZONE='UTC'`, `STATIC_URL='/static/'` y `LOGIN_URL='quizz_app:login'`. Es una configuracion de desarrollo, no de produccion.

## 2. Viaje del dato

### A. Desde `python manage.py load_quizzes` hasta SQLite

1. El comando se ejecuta desde la raiz y `manage.py` prepara Django.
2. Django carga settings, apps y modelos, y descubre `quizz_app.management.commands.load_quizzes.Command`.
3. Django invoca `Command.handle()` en `quizz_app/management/commands/load_quizzes.py`.
4. El comando calcula `data_dir` relativo a su propio archivo. La ruta resultante es la carpeta raiz `data/`.
5. Lista todos los nombres terminados en `.json`. Actualmente la fuente relevante es `data/quizzes.json`; un JSON nuevo en esa carpeta tambien seria procesado.
6. Abre cada archivo con UTF-8 y ejecuta `json.load()`.
7. Si la raiz JSON es un diccionario, lo envuelve en una lista; si es una lista, procesa sus elementos directamente.
8. Para cada quiz obtiene `title`, `description`, `category`, `difficulty` y `questions`. Los valores ausentes son `Sin titulo`, cadena vacia, `General`, `medio` y lista vacia, respectivamente.
9. Ejecuta `Quiz.objects.filter(title=title).delete()`. Por tanto, una recarga reemplaza por titulo y puede borrar resultados, inscripciones y sesiones relacionadas por `CASCADE`.
10. Ejecuta `Quiz.objects.create(...)`. `Quiz.save()` genera un `access_code` unico de 10 caracteres a partir de un UUID si no se proporciono uno.
11. `questions` se guarda completo en `Quiz.questions_data`, un `JSONField`. No se crean filas separadas para preguntas ni respuestas.
12. El comando imprime exito por quiz. Un JSON invalido o una excepcion se informa y el proceso continua con el siguiente archivo, si lo hay.

Antes de importar deben existir las tablas: `python manage.py migrate`. La secuencia operativa es instalar dependencias, migrar, cargar y ejecutar servidor.

### B. Desde la base de datos hasta la web

#### Catalogo y quiz normal

1. `GET /` entra por `quizz_project/urls.py`, se delega a `quizz_app.urls` y llega a `views.index`.
2. `index()` consulta `Quiz.objects.all().order_by('-created_at')` y renderiza `index.html` con `quizzes`.
3. `index.html` muestra metadatos y genera el enlace a `quiz_detail` con el `id` del quiz.
4. `GET /quiz/<id>/` llega a `quiz_detail()`, protegido por `login_required`. `get_object_or_404()` recupera el quiz y `quiz.get_questions()` entrega la lista almacenada a `quiz.html`.
5. `quiz.html` crea un radio por opcion. El nombre de cada grupo es `question_0`, `question_1`, etc. La navegacion paso a paso y el envio se implementan en el JavaScript incluido en esa plantilla; `main.js` solo aplica comportamiento global a tarjetas.

#### Envio y resultado

1. El navegador envia JSON por `POST /quiz/<id>/submit/` con `answers` y `question_times`.
2. `submit_quiz()` carga el quiz, normaliza tiempos no negativos, calcula `time_taken` y `average_time_per_question`, y compara cada respuesta con `question['correct_answer']`.
3. Crea `QuizResult` con quiz, usuario autenticado, puntuacion, porcentaje, respuestas y metricas temporales.
4. Devuelve JSON con `score`, `total`, `percentage`, tiempos y `result_id`.
5. `results()` recupera el resultado y vuelve a recorrer `result.quiz.get_questions()` para construir `detailed_results`; `results.html` presenta aciertos y errores.
6. `my_scores`, `leaderboard`, `teacher_dashboard`, `teacher_statistics` y `quiz_students` hacen consultas adicionales a `QuizResult`, `QuizEnrollment`, `Quiz` y `Category` para sus plantillas.

#### Creacion y edicion por profesor

`create_quiz()` y `edit_quiz()` exigen perfil con rol `profesor`, reciben el JSON del formulario, verifican que sea una lista de diccionarios con `question`, `options` y `correct_answer`, y guardan la lista en `questions_data`. En este flujo `correct_answer` debe ser un entero valido. `delete_quiz()` borra el quiz y sus dependencias en cascada.

#### Inscripcion, QR y modo live

- `generate_qr_code()` crea una imagen PNG con la URL basada en `Quiz.access_code`.
- `enroll_quiz()` busca un quiz activo por codigo y crea `QuizEnrollment` para el usuario autenticado.
- `start_live_session()` crea `LiveSession`; `manage_live_session()` cambia `waiting`, `active`, `paused` y `finished`.
- `join_live_session()` busca el codigo, crea o recupera `LiveParticipant` y redirige a `live_quiz()`.
- `live_quiz()` recibe respuestas de formulario, calcula el score y actualiza el participante.
- `live_results()` reconstruye el detalle desde el quiz y el participante.
- `api_session_status()` devuelve estado, pregunta actual, cantidad de participantes y puntuaciones en JSON. Esta vista esta exenta de CSRF.

### C. Formatos JSON y advertencias reales

`data/quizzes.json` contiene una lista de quizzes con esta forma:

```json
{
  "title": "Titulo",
  "description": "Descripcion",
  "category": "Programacion",
  "difficulty": "medio",
  "questions": [
    {
      "question": "Texto",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "1"
    }
  ]
}
```

`questions.json` no se importa: su raiz es `exam` y sus preguntas usan campos `id`, `topic`, `type`, `code`, opciones con `id/text`, `answer` y `explanation`, que no coinciden con el contrato de `load_quizzes`.

Existe una discrepancia de tipos: `data/quizzes.json` guarda `correct_answer` como string, pero `quiz.html` envia el indice como entero y `submit_quiz()`, `live_quiz()` y las vistas de resultados comparan sin convertir. En consecuencia, los quizzes cargados desde ese archivo pueden marcar respuestas correctas como incorrectas. Los quizzes creados por el profesor guardan enteros y no tienen ese problema.

## 3. Mapeo de modelos y tablas

Django crea por defecto las tablas de la app con el prefijo `quizz_app_`. Todos los modelos siguientes tienen una PK `id` de tipo `BigAutoField`, omitida de las tablas para no repetirla. Ademas existen las tablas internas de `django.contrib.auth`, sesiones, mensajes y admin.

### `Quiz` -> `quizz_app_quiz`

| Campo Python | Tipo y propiedades | Funcion |
|---|---|---|
| `creator` | `ForeignKey(User)`, `null=True`, `blank=True`, `CASCADE`, `related_name='quizzes_created'` | Profesor creador; puede estar vacio en imports. |
| `title` | `CharField(max_length=200)` | Titulo; clave practica de reemplazo del loader. |
| `description` | `TextField(blank=True)` | Descripcion. |
| `category` | `CharField(max_length=100, default='General')` | Categoria textual. |
| `difficulty` | `CharField(max_length=20)`; choices `fácil`, `medio`, `difícil`; default `medio` | Nivel. |
| `questions_data` | `JSONField(default=list)` | Lista completa de preguntas y opciones. |
| `time_limit` | `IntegerField(default=0)` | Segundos; cero significa sin limite. |
| `access_code` | `CharField(max_length=10, unique=True, blank=True)` | Codigo generado por `save()`. |
| `is_active` | `BooleanField(default=True)` | Permite inscripcion por codigo. |
| `created_at` | `DateTimeField(auto_now_add=True)` | Alta. |
| `updated_at` | `DateTimeField(auto_now=True)` | Ultima modificacion. |

Orden por defecto: `-created_at`. `get_questions()` devuelve `questions_data` o hace `json.loads()` si recibe una cadena.

### Preguntas y respuestas: no son tablas

Cada elemento de `questions_data` es un diccionario JSON:

```json
{
  "question": "Texto de la pregunta",
  "options": ["Opcion A", "Opcion B", "Opcion C", "Opcion D"],
  "correct_answer": 1
}
```

La posicion de la pregunta es su indice (`0`, `1`, ...). Ese indice se usa tambien en las claves de `answers` y `question_times`. `correct_answer` representa el indice de la opcion correcta; en el archivo inicial actual es texto, aunque el modelo JSON no impone un tipo y los formularios esperan entero.

### `QuizResult` -> `quizz_app_quizresult`

| Campo Python | Tipo y propiedades | Funcion |
|---|---|---|
| `quiz` | `ForeignKey(Quiz)`, `CASCADE`, `related_name='results'` | Quiz respondido. |
| `quiz_name` | `CharField(max_length=200, default='')` | Copia del titulo al enviar. |
| `student` | `ForeignKey(User)`, nullable, `blank=True`, `CASCADE`, `related_name='quiz_results'` | Usuario autenticado. |
| `player_name` | `CharField(max_length=100)` | Nombre persistido; el envio normal usa `request.user.username`. |
| `score` | `IntegerField` | Numero de aciertos. |
| `total_questions` | `IntegerField` | Numero total. |
| `percentage` | `FloatField` | Porcentaje. |
| `answers` | `JSONField(default=dict)` | Mapa indice de pregunta a respuesta elegida. |
| `question_times` | `JSONField(default=dict)` | Mapa indice a segundos. |
| `time_taken` | `IntegerField(default=0)` | Suma de tiempos. |
| `average_time_per_question` | `FloatField(default=0)` | Media de tiempo. |
| `created_at` | `DateTimeField(auto_now_add=True)` | Alta. |
| `updated_at` | `DateTimeField(auto_now=True)` | Modificacion. |

Orden: `-created_at`. Indices: `(student, -created_at)` y `(quiz, -created_at)`.

### Modelos auxiliares

| Modelo / tabla | Campos propios y relaciones |
|---|---|
| `UserProfile` / `quizz_app_userprofile` | `user` OneToOne a `User`, `CASCADE`, `related_name='profile'`; `role` (`profesor`/`estudiante`, default `estudiante`); `created_at`. |
| `Category` / `quizz_app_category` | `name` (`CharField(100)`), `teacher` FK a `User` con `related_name='quiz_categories'`, `created_at`; orden por nombre y unicidad `(teacher, name)`. |
| `QuizEnrollment` / `quizz_app_quizenrollment` | `student` FK, `quiz` FK, `enrolled_at`, `completed`; unicidad `(student, quiz)` y orden por `-enrolled_at`. |
| `LiveSession` / `quizz_app_livesession` | `quiz` FK, `teacher` FK, `session_code` unico de maximo 10, `status` (`waiting`, `active`, `paused`, `finished`), `current_question`, `allow_join`, `started_at`, `ended_at`, `created_at`, `updated_at`; orden `-created_at`. `save()` genera codigo de 8 caracteres. |
| `LiveParticipant` / `quizz_app_liveparticipant` | `session` FK, `student` FK nullable, `student_name`, `answers`, `score`, `completed`, `joined_at`, `submitted_at`; unicidad `(session, student_name)` y orden `-joined_at`. |

Las FK usan `on_delete=CASCADE`: borrar un quiz borra inscripciones, resultados y sesiones; borrar una sesion borra sus participantes; borrar un usuario elimina sus objetos relacionados segun cada relacion.

## 4. Rutas HTTP principales

| Ruta | Vista | Proposito |
|---|---|---|
| `/` | `index` | Catalogo. |
| `/login/`, `/register/`, `/logout/` | autenticacion | Entrada, alta y salida. |
| `/quiz/<id>/` | `quiz_detail` | Resolver quiz normal. |
| `/quiz/<id>/submit/` | `submit_quiz` | Recibir respuestas JSON y guardar resultado. |
| `/results/<id>/` | `results` | Ver resultado detallado. |
| `/mis-puntuaciones/` | `my_scores` | Historial propio. |
| `/quiz/<id>/leaderboard/` | `leaderboard` | Top 10. |
| `/quiz/<id>/qr/` y `/quiz/enroll/<code>/` | QR/inscripcion | Compartir y matricular. |
| `/teacher/...` | vistas de profesor | CRUD, estadisticas y sesiones live. |
| `/live/...` | vistas live | Unirse, responder y ver resultados. |
| `/api/session/<id>/status/` | `api_session_status` | Estado live en JSON. |
| `/admin/` | Django admin | Administracion de modelos registrados. |

## 5. Secuencia minima de ejecucion

```text
1. Activar venv y ejecutar pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py load_quizzes
4. python manage.py runserver
5. Abrir http://localhost:8000/
```

La importacion es reemplazo por titulo, no una insercion incremental: al repetirla se genera un nuevo `access_code` para cada quiz reemplazado y se pueden perder datos dependientes por cascada.
