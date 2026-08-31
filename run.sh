#!/bin/bash
# Script para ejecutar la aplicación QuizzMaster en Linux/Mac

echo "========================================"
echo "  QuizzMaster - Django Quiz App"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    exit 1
fi

# Crear y activar entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Instalando dependencias..."
    pip install -r requirements.txt
else
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Inicializar base de datos si no existe
if [ ! -f "db.sqlite3" ]; then
    echo "Inicializando base de datos..."
    python manage.py migrate
    echo "Cargando quizzes..."
    python manage.py load_quizzes
fi

# Iniciar el servidor
echo ""
echo "========================================"
echo "Iniciando servidor..."
echo "Abre tu navegador en: http://localhost:8000"
echo "Presiona Ctrl+C para detener"
echo "========================================"
echo ""

python manage.py runserver
