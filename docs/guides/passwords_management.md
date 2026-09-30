# 🔐 Guía Rápida: Creación y Gestión de Contraseñas en Django
### *quizArenas / Ducky Arena — Para Windows y Mac*

Esta guía explica paso a paso cómo crear usuarios administradores, cambiar contraseñas olvidadas y gestionar accesos en Django tanto en **Windows (Microsoft)** como en **macOS (Apple)**.

---

## 📋 PASO 0: Abrir la Terminal y Activar el Entorno Virtual

Antes de ejecutar cualquier comando de Django, debes situarte en la carpeta del proyecto y activar el entorno virtual (`venv` o `.venv`).

### 🪟 En Windows (Microsoft):
1. Abre tu terminal (**Git Bash**, **PowerShell** o **Símbolo del sistema / CMD**) en la carpeta del proyecto.
2. Activa el entorno virtual según tu consola:
   * **En Git Bash:**
     ```bash
     source venv/Scripts/activate
     # (o 'source .venv/Scripts/activate' si tu carpeta se llama .venv)
     ```
   * **En PowerShell:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     # (o .\.venv\Scripts\Activate.ps1)
     ```
   * **En CMD (Símbolo del sistema):**
     ```cmd
     venv\Scripts\activate.bat
     # (o .venv\Scripts\activate.bat)
     ```
3. *Verifica que aparezca `(venv)` al inicio de la línea de comandos.*

---

### 🍎 En macOS (Mac):
1. Abre la aplicación **Terminal** o tu terminal integrada en VS Code / Cursor.
2. Navega a la carpeta del proyecto (`cd /ruta/hacia/DuckyArena`).
3. Activa el entorno virtual:
   ```bash
   source venv/bin/activate
   # (o 'source .venv/bin/activate' si tu carpeta se llama .venv)
   ```
4. *Verifica que aparezca `(venv)` al inicio de la línea de comandos.*

---

## 🔑 MÉTODO 1: Crear un Superusuario / Administrador (Nuevo)

Úsalo cuando necesites un usuario con acceso total al panel de administración y a todas las funciones.

### Comando:
- **En Windows:**
  ```bash
  python manage.py createsuperuser
  ```
- **En Mac:**
  ```bash
  python3 manage.py createsuperuser
  # (o 'python manage.py createsuperuser' si el venv está activo)
  ```

### Lo que te pedirá la terminal:
1. **Username (Usuario):** Escribe el nombre de usuario (ej. `admin` o tu nombre) y presiona `Enter`.
2. **Email address (Correo):** Puedes escribir tu correo o dejarlo en blanco presionando `Enter`.
3. **Password (Contraseña):** Escribe tu contraseña y presiona `Enter`.  
   > ⚠️ **IMPORTANTE:** Por motivos de seguridad, **no verás letras ni asteriscos mientras escribes**. Escribe la contraseña con calma y presiona `Enter`.
4. **Password (again):** Repite la contraseña y presiona `Enter`.
5. Si todo es correcto, verás el mensaje: `Superuser created successfully.`

---

## 🔄 MÉTODO 2: Cambiar la Contraseña de un Usuario Existente

Si ya tienes un usuario pero no recuerdas la contraseña:

### Comando:
- **En Windows:**
  ```bash
  python manage.py changepassword nombre_de_usuario
  ```
- **En Mac:**
  ```bash
  python3 manage.py changepassword nombre_de_usuario
  ```

*(Reemplaza `nombre_de_usuario` por el usuario real, ej. `python manage.py changepassword admin`)*

### Pasos:
1. Escribe la nueva contraseña y presiona `Enter` (los caracteres no se mostrarán en pantalla).
2. Repite la nueva contraseña y presiona `Enter`.
3. Verás: `Password changed successfully for user 'nombre_de_usuario'`.

---

## 🖥️ MÉTODO 3: Cambiar Contraseña desde el Panel Web de Django

Si ya tienes acceso con un superusuario:

1. Inicia el servidor local:
   - Windows: `python manage.py runserver`
   - Mac: `python3 manage.py runserver`
2. Abre tu navegador en: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
3. Inicia sesión con tus credenciales de superusuario.
4. Ve a la sección **Authentication and Authorization** > **Users** (Usuarios).
5. Haz clic en el usuario al que deseas cambiarle la contraseña.
6. En la parte superior del formulario, haz clic en el enlace que dice **"this form"** (este formulario) o **"change password"**.
7. Ingresa la nueva contraseña, confírmala y haz clic en **Change password**.

---

## ⚡ MÉTODO 4: Crear Usuario o Cambiar Contraseña por Consola Interactiva (Django Shell)

Si prefieres hacerlo directamente con código Python:

1. Entra a la consola interactiva:
   ```bash
   python manage.py shell
   ```
2. Ejecuta las siguientes líneas:

   * **Para crear un usuario normal con contraseña:**
     ```python
     from django.contrib.auth.models import User
     user = User.objects.create_user(username='miusuario', password='mipassword123', email='correo@ejemplo.com')
     user.save()
     exit()
     ```

   * **Para cambiarle la contraseña a un usuario existente:**
     ```python
     from django.contrib.auth.models import User
     user = User.objects.get(username='miusuario')
     user.set_password('nueva_password_123')
     user.save()
     exit()
     ```

---

## ❓ Preguntas Frecuentes y Solución de Problemas

| Problema | Causa | Solución |
| :--- | :--- | :--- |
| **"Escribo la contraseña y no aparece nada en pantalla"** | Comportamiento estándar de seguridad en terminales. | Sigue escribiendo con normalidad y presiona `Enter`. |
| **`python: command not found` (en Mac)** | En macOS suele llamarse `python3`. | Usa `python3 manage.py ...` o activa tu entorno virtual. |
| **`No module named django`** | El entorno virtual no está activado. | Ejecuta el comando de activación del **Paso 0**. |
| **`This password is too short / too common`** | Django valida que la contraseña sea segura. | Usa al menos 8 caracteres combinando letras y números, o presiona `y` cuando pregunte si deseas ignorar la advertencia en desarrollo local. |
