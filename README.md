# 🐥 Ducky Quiz Arenas — Plataforma Académica Gamificada

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular-orange.svg)](docs/architecture/architecture_blueprint.md)
[![Docs](https://img.shields.io/badge/Documentation-docs%2F-brightgreen.svg)](docs/README.md)

**Ducky Quiz Arenas** es una plataforma educativa interactiva orientada al aprendizaje gamificado y evaluación formativa. Desarrollada en **Django**, permite a los docentes diseñar bancos de preguntas temáticas y desplegar salas de competición multijugador en tiempo real mediante códigos PIN de acceso, fomentando la participación dinámica de los estudiantes a través de rankings en vivo y una economía virtual basada en **Ducky Coins**.

---

## 🎯 ¿Qué hace el Proyecto en su Totalidad?

El sistema integra de forma modular dos grandes áreas funcionales:

1. **Gestión de Contenido y Banco de Preguntas (`quizzes`):**
   - Panel del profesor para crear, editar, estructurar y publicar cuestionarios con control de tiempo límite y ponderación de puntos.
   - Banco de preguntas de opción múltiple con validación estricta en servidor.
   - Búsqueda, categorización y exploración de cuestionarios públicos.

2. **Motor de Partidas en Tiempo Real (`quiz_games`):**
   - Generación dinámica de salas con **código PIN de 6 dígitos** no colisionable.
   - Lobby de espera para participantes con visualización de estado.
   - Evaluación server-side de respuestas con protección contra fugas de información (*zero client leaks*).
   - Motor de puntuación transaccional (`transaction.atomic`) con bonificación por tiempo de respuesta y cálculo de rachas (*streaks*).
   - Podio y tabla de clasificación en vivo al finalizar la partida.

3. **Economía Virtual y Perfiles:**
   - Asignación y acumulación de recompensas en *Ducky Coins* asociadas al perfil del estudiante.

---

## 👥 Estructura del Equipo y Asignación de Módulos

El desarrollo colaborativo del proyecto se encuentra estructurado en equipos de trabajo especializados bajo la metodología de revisión por pares y gobernanza con `CODEOWNERS`:

| Rol / Módulo | Responsables | Rama Base / Ámbito |
| :--- | :--- | :--- |
| **🚀 Lead Developer & DevOps** | **Darwin** ([@darwinabarca64](https://github.com/darwinabarca64)) | `main` · Infraestructura, arquitectura base y aprobación |
| **🔍 Mentor & Auditoría** | **Oscar Burgos** ([@mihifidem](https://github.com/mihifidem)) | `main` · Revisión técnica y aseguramiento de calidad |
| **📝 PARTE 1: Cuestionarios (`quizzes`)** | **Sasha** ([@sashasafont](https://github.com/sashasafont))<br>**Nacho** ([@nachopython](https://github.com/nachopython))<br>**Robert Betancourt** ([@Trevor783](https://github.com/Trevor783)) | `parte-1-quizzes`<br>Banco de preguntas, respuestas y CRUD del profesor |
| **🎮 PARTE 2: Motor de Juego (`quiz_games`)** | **[@dalcolea](https://github.com/dalcolea)**<br>**Thais** ([@thaishps3](https://github.com/thaishps3)) | `parte-2-quizgames`<br>Salas con PIN, lobby, evaluación y puntuación en vivo |

---

## 📚 Mapa de Documentación del Proyecto

Para mantener el código limpio y modular, toda la documentación detallada se encuentra organizada en el directorio [`docs/`](docs/README.md). A continuación se describe la utilidad de cada documento:

### 🚀 Guías de Instalación y Operación (`docs/guides/`)
- [**`docs/guides/setup.md`**](docs/guides/setup.md): **Guía de Configuración Inicial.** Paso a paso simplificado para clonar el repositorio, crear el entorno virtual, instalar dependencias y levantar el servidor tanto en **Windows** como en **Mac**.
- [**`docs/guides/github_workflow.md`**](docs/guides/github_workflow.md): **Flujo Git y Trabajo en Equipo.** Explica cómo sincronizar ramas, crear ramas personales de trabajo y solicitar revisiones mediante Pull Requests según el equipo asignado.
- [**`docs/guides/passwords_management.md`**](docs/guides/passwords_management.md): **Gestión de Contraseñas Django.** Instrucciones prácticas para crear superusuarios/administradores y recuperar o resetear contraseñas por terminal, shell interactivo o panel web.
- [**`docs/guides/quickstart.md`**](docs/guides/quickstart.md): **Inicio Rápido.** Referencia de comandos rápidos de consola para el entorno de desarrollo.

### 🏛️ Arquitectura y Especificaciones (`docs/architecture/`)
- [**`docs/architecture/architecture_blueprint.md`**](docs/architecture/architecture_blueprint.md): **Plano Arquitectónico.** Diagramas, modelos de datos, contratos relacionales y flujos de evaluación server-side.
- [**`docs/architecture/ducky_arena_master_spec.pdf`**](docs/architecture/ducky_arena_master_spec.pdf): **Especificación Maestra Oficial.** Documento de requerimientos funcionales y diseño del sistema.

### 📊 Informes y Registros Técnicos (`docs/reports/`)
- [**`docs/reports/implementation_summary.md`**](docs/reports/implementation_summary.md): **Resumen de Implementación.** Detalle de componentes construidos y trazabilidad por fases.
- [**`docs/reports/diagnostic_report.md`**](docs/reports/diagnostic_report.md): **Informe Diagnóstico.** Análisis de dependencias, base de datos y estabilidad del sistema.
- [**`docs/reports/commits_log.md`**](docs/reports/commits_log.md): **Histórico de Commits.** Registro cronológico de cambios y transformaciones del repositorio.

### ⚖️ Reglas Maestras de Código
- [**`PROJECT_RULES.md`**](PROJECT_RULES.md): **Directivas Técnicas Inquebrantables.** Estándares de concurrencia (`transaction.atomic`), integridad (`models.PROTECT`) y seguridad de datos.
