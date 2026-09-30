# DUCKY ARENA — REGLAS MAESTRAS DE GOBIERNO TÉCNICO Y ARQUITECTURA (GEMINI & AGENTS)

Este documento es la fuente inquebrantable de directivas operativas para el desarrollo en Ducky Quiz Arenas con Google Antigravity (Gemini).

## 1. ARQUITECTURA MODULAR Y ALCANCE DE EQUIPOS
- El desarrollo asignado abarca exclusivamente dos aplicaciones modulares:
  * `quizzes`: Responsable del banco de cuestionarios, preguntas y respuestas (CRUD del Profesor / Equipo 1).
  * `quiz_games`: Responsable del motor de partidas grupales en tiempo real, PIN, lobby, evaluación server-side y ranking (Equipo 2).
- Prohibición absoluta de crear aplicaciones monolíticas (e.g., `quizz_app`) o unificar responsabilidades.
- Prohibición estricta de crear modelos `User` personalizados o modificar la app `accounts`/`core` (Equipo 0). Las referencias a usuarios siempre deben emplear `settings.AUTH_USER_MODEL`.

## 2. PRESERVACIÓN DE CÓDIGO Y POLÍTICA CERO LAZY CODING
- Queda terminantemente prohibido sobreescribir, borrar o podar código funcional implementado en fases previas. Toda adición debe extender o integrarse limpiamente con los modelos existentes.
- Prohibición de comentarios tipo `# TODO`, stubs de funciones o métodos sin completar (`pass`). Todo código entregado debe estar 100% listo para producción.
- No generar plantillas HTML sin estilos CSS completos ni vistas sin validación robusta de formularios.

## 3. IDENTIDAD, PERMISOS Y ECONOMÍA (EQUIPO 0 & 1)
- La única fuente oficial de saldo es `request.user.profile.ducky_coins`. Está prohibido duplicar lógica económica o crear modelos de saldo alternativos.
- Permisos Estrictos en `quizzes`: Solo el creador del Quiz (`quiz.creator == request.user`) y con rol `profile.role == 'TEACHER'` tiene autorización para crear, editar o eliminar cuestionarios y sus preguntas asociadas.
- Regla de Validación de Negocio para Quizzes:
  * Todo Quiz publicado (`is_published=True`) debe contener como mínimo 1 pregunta.
  * Cada Question debe tener entre 2 y 6 opciones de Answer.
  * Cada Question debe tener EXACTAMENTE UNA respuesta con `is_correct=True`.
  * El tiempo límite (`time_limit`) y los puntos (`points`) deben ser estrictamente mayores a cero.

## 4. INTEGRIDAD RELACIONAL, SEGURIDAD Y TRANSACCIONES (EQUIPO 2)
- Protección Histórica: Todas las claves foráneas de `quiz_games` hacia `quizzes.Quiz`, `quizzes.Question` y `quizzes.Answer` deben tener `on_delete=models.PROTECT` para imposibilitar borrados accidentales de partidas jugadas.
- Unicidad Obligatoria:
  * `GamePlayer` debe implementar `UniqueConstraint(fields=['game', 'player'], name='unique_player_per_quiz_game')`.
  * `PlayerAnswer` debe implementar `UniqueConstraint(fields=['game_player', 'question'], name='unique_answer_per_player_question')`.
- Cero Leaks Server-Side: El servidor NUNCA debe incluir el atributo `is_correct` en el contexto HTML o payload JSON entregado al cliente durante la partida. La validación se ejecuta exclusivamente en el backend mediante `selected_answer.is_correct`.
- Atomicidad Transaccional: La recepción y calificación de respuestas debe ejecutarse dentro de un bloque `with transaction.atomic():` usando `select_for_update()`, actualizando simultáneamente `PlayerAnswer` y los campos `score`, `correct_answers` y `current_streak` de `GamePlayer`.
- Generación de PIN: El código PIN de 6 dígitos de `Game` debe generarse algorítmicamente verificando la no existencia en base de datos antes del guardado para prevenir colisiones.

## 5. ESTÁNDARES UX/UI DUCKY ARENA
- Todas las vistas deben heredar de `base.html` (provisto por el Equipo 0).
- Utilizar la paleta de colores oficial Ducky Arena (amarillos vibrantes, acentos oscuros, feedback visual claro).
- Enfoque mobile-first, diseño responsive, micro-interacciones, animaciones de transición, estados de carga y feedback visual inmediato tras el envío de respuestas o acciones de formulario.

## 6. PROTOCOLO DE VERIFICACIÓN CONTINUA
- Tras cada modificación en el código fuente, ejecutar:
  * `python manage.py check`
  * `python manage.py test`
- Todo cambio de modelos debe ir acompañado de sus correspondientes `makemigrations` y `migrate` probados sin dependencias rotas.
