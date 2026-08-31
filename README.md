# 🎯 QuizzMaster - Aplicación Django para Quizzes

Una aplicación web interactiva y moderna para crear y responder quizzes. Los datos de los quizzes se cargan desde archivos JSON, permitiendo una gestión sencilla de contenido.

## ✨ Características

- 🎮 Interfaz moderna, dinámica y divertida
- 📝 Soporte para múltiples quizzes
- 🎯 Tres niveles de dificultad (Fácil, Medio, Difícil)
- 📊 Sistema de puntuación y tabla de posiciones
- 📱 Totalmente responsive
- 🎨 Estilos modernos con gradientes y animaciones
- 📄 Carga de quizzes desde JSON

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clona o descarga el proyecto**
```bash
cd c:\Proyectos\quizz
```

2. **Crea un entorno virtual** (opcional pero recomendado)
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

4. **Realiza las migraciones de la base de datos**
```bash
python manage.py migrate
```

5. **Carga los quizzes desde el archivo JSON**
```bash
python manage.py load_quizzes
```

6. **Inicia el servidor de desarrollo**
```bash
python manage.py runserver
```

7. **Abre tu navegador y ve a**
```
http://localhost:8000
```

## 📋 Estructura del Proyecto

```
quizz/
├── quizz_project/          # Configuración del proyecto Django
│   ├── settings.py         # Configuración principal
│   ├── urls.py            # URLs del proyecto
│   └── wsgi.py            # WSGI para producción
├── quizz_app/              # Aplicación principal
│   ├── models.py          # Modelos de datos (Quiz, QuizResult)
│   ├── views.py           # Vistas de la aplicación
│   ├── urls.py            # URLs de la aplicación
│   ├── management/        # Comandos personalizados
│   │   └── commands/
│   │       └── load_quizzes.py  # Comando para cargar quizzes
│   ├── templates/         # Plantillas HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── quiz.html
│   │   ├── results.html
│   │   └── leaderboard.html
│   └── static/            # Archivos estáticos
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── data/                  # Archivos JSON de quizzes
│   └── quizzes.json
├── manage.py              # Script de gestión de Django
└── requirements.txt       # Dependencias del proyecto
```

## 📝 Formato del JSON de Quizzes

Agrega tus propios quizzes en `data/quizzes.json`:

```json
[
    {
        "title": "Título del Quiz",
        "description": "Descripción del quiz",
        "category": "Categoría",
        "difficulty": "fácil",
        "questions": [
            {
                "question": "¿Pregunta 1?",
                "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
                "correct_answer": "0"
            }
        ]
    }
]
```

### Parámetros:
- **title**: Nombre del quiz
- **description**: Descripción breve
- **category**: Categoría (Programación, Geografía, Historia, etc.)
- **difficulty**: Nivel de dificultad (fácil, medio, difícil)
- **questions**: Array de preguntas
  - **question**: Texto de la pregunta
  - **options**: Array con 4 opciones de respuesta
  - **correct_answer**: Índice de la respuesta correcta (0-3)

## 🎮 Uso

1. **Ver Quizzes**: La página de inicio muestra todos los quizzes disponibles
2. **Responder Quiz**: Selecciona un quiz y responde todas las preguntas
3. **Ver Resultados**: Después de enviar, verás tu puntuación y análisis detallado
4. **Tabla de Posiciones**: Compite con otros jugadores en la tabla de puntuaciones

## 🛠️ Comandos útiles

```bash
# Cargar quizzes desde JSON
python manage.py load_quizzes

# Crear superusuario (para admin)
python manage.py createsuperuser

# Acceder a admin en http://localhost:8000/admin
# (requiere superusuario)

# Realizar migraciones después de cambiar modelos
python manage.py makemigrations
python manage.py migrate
```

## 🎨 Personalización

### Cambiar colores principales
Edita `quizz_app/static/css/style.css` y modifica los gradientes:
```css
/* Gradiente principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Agregar más quizzes
Simplemente agrega más objetos al archivo `data/quizzes.json` y ejecuta:
```bash
python manage.py load_quizzes
```

## 📱 Características Responsive

La aplicación se adapta perfectamente a:
- 📱 Dispositivos móviles
- 📱 Tablets
- 🖥️ Desktops

## 🔒 Seguridad

- CSRF protection habilitada
- Input validation en servidor
- SQLite por defecto (cambiar en producción)

## 📦 Producción

Para desplegar en producción:

1. Cambia `DEBUG = False` en `settings.py`
2. Configura `ALLOWED_HOSTS` apropiadamente
3. Usa una base de datos robusta (PostgreSQL, MySQL)
4. Configura un servidor WSGI (Gunicorn, uWSGI)
5. Usa un servidor web (Nginx, Apache)

## 🐛 Solución de problemas

**Error: "ModuleNotFoundError: No module named 'django'"**
```bash
pip install -r requirements.txt
```

**Error: "No table found"**
```bash
python manage.py migrate
```

**Los quizzes no aparecen**
```bash
python manage.py load_quizzes
```

## 📄 Licencia

Este proyecto es de código abierto y libre de usar.

## 🎯 Próximas mejoras

- [ ] Sistema de login de usuarios
- [ ] Perfil de usuario con historial
- [ ] Editor visual de quizzes
- [ ] Exportar resultados a PDF
- [ ] Compartir resultados en redes sociales
- [ ] Modo multijugador en tiempo real

---

¡Diviértete y aprende con QuizzMaster! 🚀
