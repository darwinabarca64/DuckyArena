@echo off
REM Script para ejecutar la aplicación QuizzMaster en Windows

echo.
echo ========================================
echo   QuizzMaster - Django Quiz App
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar si el entorno virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Instalando dependencias...
    pip install -r requirements.txt
) else (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Verificar si la base de datos existe
if not exist "db.sqlite3" (
    echo Inicializando base de datos...
    python manage.py migrate
    echo Cargando quizzes...
    python manage.py load_quizzes
)

REM Iniciar el servidor
echo.
echo ========================================
echo Iniciando servidor...
echo Abre tu navegador en: http://localhost:8000
echo Presiona Ctrl+C para detener
echo ========================================
echo.

python manage.py runserver

pause
