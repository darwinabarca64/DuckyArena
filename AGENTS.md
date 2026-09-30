# AGENTS.md — GUÍA DE AGENTES ANTIGRAVITY / GEMINI

## Propósito
Este archivo define el gobierno de agentes autónomos y asistentes de código en el proyecto Ducky Quiz Arenas.

## Directivas Principales
1. **Gobierno Técnico:** Cumplir estrictamente con las directivas de [GEMINI.md](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/GEMINI.md) y [PROJECT_RULES.md](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/PROJECT_RULES.md).
2. **Arquitectura:** Desarrollar exclusivamente en las apps `quizzes` (Equipo 1) y `quiz_games` (Equipo 2).
3. **Seguridad y Concurrencia:**
   - Cero leaks de `is_correct` en contextos de cliente y serializadores.
   - Uso de `transaction.atomic()` y `select_for_update()` en transacciones de evaluación.
   - Protección de claves foráneas con `models.PROTECT`.
4. **Verificación Sistemática:**
   - Ejecutar `python manage.py check` y `python manage.py test` antes de dar por completada cualquier micro-fase o tarea.
