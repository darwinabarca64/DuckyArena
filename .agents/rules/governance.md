# Reglas de Gobierno y Calidad de Código — Ducky Arena

## Directivas Obligatorias
- **No Lazy Coding:** Prohibido dejar funciones con `pass` o comentarios `# TODO`. Todo código entregado debe estar probado y completamente funcional.
- **Seguridad en Partidas en Vivo:**
  - Jamás exponer el atributo `is_correct` de las respuestas en plantillas HTML ni en respuestas JSON al jugador durante la partida.
  - La calificación siempre se realiza en el servidor comparando `selected_answer.is_correct`.
- **Integridad de Base de Datos:**
  - Usar `with transaction.atomic()` y `select_for_update()` en operaciones de evaluación y guardado de respuestas.
  - Asegurar `UniqueConstraint` en `GamePlayer` y `PlayerAnswer`.
- **Pruebas Continuas:**
  - Mantener la suite de tests en `quizzes/tests.py` y `quiz_games/tests.py` con 100% de éxito.
