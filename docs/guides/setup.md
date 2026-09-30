# 🚀 Guía de Instalación Rápida (Setup) — Ducky Arena

Guía paso a paso para clonar, configurar y ejecutar el proyecto en **Windows** y **Mac**.

---

## 🪟 Opción A: Configuración en Windows (Microsoft)

Abre tu terminal (**Git Bash** o **PowerShell**) y ejecuta los siguientes comandos uno por uno:

### 1. Clonar el repositorio y entrar a la carpeta
```bash
git clone https://github.com/darwinabarca64/DuckyArena.git
cd DuckyArena
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
```
- **Si usas Git Bash:**
  ```bash
  source venv/Scripts/activate
  ```
- **Si usas PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
*(Verás `(venv)` al inicio de tu terminal indicando que está activo).*

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Preparar la base de datos
```bash
python manage.py migrate
```

### 5. Iniciar el servidor
```bash
python manage.py runserver
```
👉 Abre tu navegador en: [http://localhost:8000](http://localhost:8000)

---

## 🍎 Opción B: Configuración en Mac (macOS)

Abre tu **Terminal** y ejecuta los siguientes comandos uno por uno:

### 1. Clonar el repositorio y entrar a la carpeta
```bash
git clone https://github.com/darwinabarca64/DuckyArena.git
cd DuckyArena
```

### 2. Crear y activar el entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```
*(Verás `(venv)` al inicio de tu terminal indicando que está activo).*

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Preparar la base de datos
```bash
python3 manage.py migrate
```

### 5. Iniciar el servidor
```bash
python3 manage.py runserver
```
👉 Abre tu navegador en: [http://localhost:8000](http://localhost:8000)

---

## 🛑 Detener el servidor
Para apagar el servidor de desarrollo, presiona `Ctrl + C` en tu terminal.

## 🔄 Volver a trabajar otro día
Cada vez que abras una nueva terminal para trabajar, solo necesitas:
1. Entrar a la carpeta: `cd DuckyArena`
2. Activar el entorno virtual:
   - En Windows (Git Bash): `source venv/Scripts/activate`
   - En Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
   - En Mac: `source venv/bin/activate`
3. Iniciar el servidor: `python manage.py runserver` (o `python3 manage.py runserver` en Mac)
