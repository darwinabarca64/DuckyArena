# 📚 Centro de Documentación Técnica — Ducky Arena

Bienvenido al repositorio central de documentación de **Ducky Arena (quizArenas)**. Este directorio organiza todo el conocimiento del proyecto estructurado bajo estándares de arquitectura limpia y desarrollo colaborativo.

---

## 🗂️ Estructura de Documentación

```text
docs/
├── guides/            # Guías operativas paso a paso para desarrolladores
├── architecture/      # Planos arquitectónicos, diagramas y especificaciones
└── reports/           # Auditorías, diagnósticos e históricos de implementación
```

---

## 📖 1. Guías para Desarrolladores (`docs/guides/`)

| Documento | Audiencia | Descripción |
| :--- | :--- | :--- |
| [**`setup.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/guides/setup.md) | Todos los Desarrolladores | Guía de instalación rápida y arranque local para **Windows** y **Mac**. |
| [**`github_management.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/guides/github_management.md) | Todos los Desarrolladores | Protocolo oficial de sincronización y actualización local sin conflictos ni pérdidas. |
| [**`github_workflow.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/guides/github_workflow.md) | Todos los Equipos | Flujo Git, asignación de equipos (`quizzes` vs `quiz_games`) y política de Pull Requests. |
| [**`passwords_management.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/guides/passwords_management.md) | Todos los Desarrolladores | Creación de superusuarios y reseteo de contraseñas en Django vía CLI, shell y admin. |
| [**`quickstart.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/guides/quickstart.md) | Onboarding | Guía introductoria de comandos rápidos de entorno. |

---

## 🏛️ 2. Arquitectura y Especificaciones (`docs/architecture/`)

| Documento | Enfoque | Descripción |
| :--- | :--- | :--- |
| [**`architecture_blueprint.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/architecture/architecture_blueprint.md) | Arquitectura del Sistema | Plano maestro de la arquitectura modular Django, modelos, relaciones y flujos server-side. |
| [**`ducky_arena_master_spec.pdf`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/architecture/ducky_arena_master_spec.pdf) | Especificación Oficial | Documento PDF con los requerimientos funcionales y de negocio de Ducky Arena. |

---

## 📊 3. Informes y Reportes (`docs/reports/`)

| Documento | Tipo | Descripción |
| :--- | :--- | :--- |
| [**`implementation_summary.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/reports/implementation_summary.md) | Informe Técnico | Resumen ejecutivo del refactor modular y trazabilidad de entregables. |
| [**`diagnostic_report.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/reports/diagnostic_report.md) | Auditoría de Sistema | Diagnóstico profundo de estabilidad, dependencias y base de datos. |
| [**`commits_log.md`**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/reports/commits_log.md) | Histórico | Bitácora cronológica de commits y transformaciones del repositorio. |

---

## ⚖️ Reglas y Gobernanza
- Las reglas maestras de desarrollo y restricciones arquitectónicas se encuentran en [`PROJECT_RULES.md`](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/PROJECT_RULES.md) en la raíz del proyecto.
- Las directivas para asistentes de IA y agentes están en [`GEMINI.md`](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/GEMINI.md) y [`AGENTS.md`](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/AGENTS.md).
