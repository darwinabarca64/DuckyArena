#!/usr/bin/env python
"""
Script de configuración rápida para QuizzMaster
Ejecuta: python setup.py
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}\n")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} falló")
        return False

def main():
    """Main setup function."""
    print("\n" + "="*50)
    print("  QuizzMaster - Setup Inicial")
    print("="*50 + "\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Necesitas Python 3.8 o superior")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detectado\n")
    
    # Create virtual environment
    if not os.path.exists('venv'):
        if not run_command(
            f"{'python -m venv venv' if platform.system() != 'Windows' else 'python -m venv venv'}",
            "Creando entorno virtual..."
        ):
            return False
    else:
        print("✓ Entorno virtual ya existe\n")
    
    # Activate virtual environment and install dependencies
    if platform.system() == 'Windows':
        activate_cmd = 'venv\\Scripts\\activate.bat && pip install -r requirements.txt'
    else:
        activate_cmd = 'source venv/bin/activate && pip install -r requirements.txt'
    
    if not run_command(activate_cmd, "Instalando dependencias..."):
        return False
    
    print("✓ Dependencias instaladas correctamente\n")
    
    # Run migrations
    if platform.system() == 'Windows':
        migrate_cmd = 'venv\\Scripts\\python.exe manage.py migrate'
        load_cmd = 'venv\\Scripts\\python.exe manage.py load_quizzes'
    else:
        migrate_cmd = 'source venv/bin/activate && python manage.py migrate'
        load_cmd = 'source venv/bin/activate && python manage.py load_quizzes'
    
    if not run_command(migrate_cmd, "Configurando base de datos..."):
        return False
    
    print("✓ Base de datos configurada\n")
    
    # Load quizzes
    if not run_command(load_cmd, "Cargando quizzes..."):
        print("⚠ Advertencia: No se pudieron cargar los quizzes, pero la aplicación funcionará")
    else:
        print("✓ Quizzes cargados correctamente\n")
    
    # Print final instructions
    print("\n" + "="*50)
    print("  ¡Configuración completada! ✓")
    print("="*50 + "\n")
    
    print("Para iniciar la aplicación, ejecuta:\n")
    
    if platform.system() == 'Windows':
        print("  1. run.bat")
        print("\n  O manualmente:")
        print("  1. venv\\Scripts\\activate.bat")
        print("  2. python manage.py runserver")
    else:
        print("  1. chmod +x run.sh")
        print("  2. ./run.sh")
        print("\n  O manualmente:")
        print("  1. source venv/bin/activate")
        print("  2. python manage.py runserver")
    
    print("\nLuego abre tu navegador en: http://localhost:8000\n")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
