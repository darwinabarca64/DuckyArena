---
name: ducky-arena
description: >-
  Directivas operativas, patrones de arquitectura Django, motor de partidas multijugador,
  seguridad server-side y normas de desarrollo para el proyecto Ducky Quiz Arenas.
---

# Skill: Ducky Quiz Arena Workflow

## Propósito
Esta skill contiene las pautas y flujos de trabajo para extender y mantener las aplicaciones `quizzes` y `quiz_games` en la plataforma Ducky Quiz Arenas.

## Flujos de Desarrollo

### 1. Gestión de Cuestionarios (`quizzes`)
- Todo Quiz publicado debe contener al menos 1 pregunta.
- Cada Question contiene entre 2 y 6 opciones de Answer.
- Exactamente 1 opción debe tener `is_correct=True`.
- Solo el docente creador (`quiz.creator == request.user`) con rol `TEACHER` puede editar/eliminar.

### 2. Motor de Partidas Multijugador (`quiz_games`)
- Generación de PIN numérico de 6 dígitos con `secrets.randbelow(1000000)`.
- El anfitrión administra la sala desde `game_host_lobby` y `game_host_play`.
- Los participantes ingresan mediante `game_join` y responden a través de `game_player_play`.
- La calificación de respuestas se efectúa server-side en `submit_player_answer` con `select_for_update()` y `transaction.atomic()`.
- Se calcula la puntuación con base en el tiempo y racha consecutiva de aciertos.

### 3. Protocolo de Verificación
Tras cualquier cambio:
```bash
python manage.py check
python manage.py test
```
