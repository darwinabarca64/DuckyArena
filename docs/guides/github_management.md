# 🔄 PROTOCOLO DE ACTUALIZACIÓN Y SINCRONIZACIÓN — quizArenas

Este documento establece el procedimiento obligatorio para sincronizar tu entorno local con los últimos cambios consolidados en el repositorio central, previniendo conflictos de ramas, incompatibilidad de librerías y bloqueos en base de datos.

---

## ⚠️ PRE-REQUISITO: RESGUARDAR CAMBIOS LOCALES PENDIENTES

Si tienes código local sin guardar antes de actualizar, **no hagas pull directo**. Ejecuta en tu terminal una de las siguientes opciones:

- **Guardar temporalmente cambios en curso:**
  ```bash
  git stash
  ```
- **O confirmar tus avances en tu rama personal:**
  ```bash
  git add . && git commit -m "wip: guardar progreso local antes de sync"
  ```

---

## 🚀 PASO A PASO DE SINCRONIZACIÓN SEGÚN TU EQUIPO

### Caso A: Equipo 1 (quizzes) — Sasha, Nacho, Robert
Abre Git Bash en la raíz del proyecto con tu entorno virtual activo `(venv)` y ejecuta en orden:

1. **Cambiar a la rama base de tu equipo:**
   ```bash
   git checkout parte-1-quizzes
   ```

2. **Descargar e integrar las actualizaciones remotas:**
   ```bash
   git pull origin parte-1-quizzes
   ```

3. **Instalar dependencias actualizadas del sistema (Daphne, Channels, etc.):**
   ```bash
   uv pip install -r requirements.txt || pip install -r requirements.txt
   ```

4. **Aplicar migraciones a la base de datos local:**
   ```bash
   python manage.py migrate
   ```

5. **Validar la integridad del sistema:**
   ```bash
   python manage.py check
   ```

---

### Caso B: Equipo 2 (quiz_games) — Dalcolea, Thais
Abre Git Bash en la raíz del proyecto con tu entorno virtual activo `(venv)` y ejecuta en orden:

1. **Cambiar a la rama base de tu equipo:**
   ```bash
   git checkout parte-2-quizgames
   ```

2. **Descargar e integrar las actualizaciones remotas:**
   ```bash
   git pull origin parte-2-quizgames
   ```

3. **Instalar dependencias actualizadas del sistema (Daphne, Channels, etc.):**
   ```bash
   uv pip install -r requirements.txt || pip install -r requirements.txt
   ```

4. **Aplicar migraciones a la base de datos local:**
   ```bash
   python manage.py migrate
   ```

5. **Validar la integridad del sistema:**
   ```bash
   python manage.py check
   ```

---

## 🛠️ RESOLUCIÓN DE INCIDENCIAS FRECUENTES

- **Error: Your local changes would be overwritten by merge**:
  Ejecuta `git stash`, luego realiza el `git pull` y finalmente recupera tus archivos con `git stash pop`.

- **Error: ModuleNotFoundError: No module named 'channels' o 'daphne'**:
  Significa que no se ejecutó la instalación de dependencias en el entorno virtual. Asegúrate de ver `(venv)` al inicio de la consola y corre:
  ```bash
  pip install -r requirements.txt
  ```

- **Error: Conflicto en base de datos SQLite**:
  Si la base de datos local queda inconsistente, puedes recrearla limpiamente ejecutando:
  ```bash
  python manage.py migrate
  ```
  y luego regenerar los perfiles de prueba con:
  ```bash
  python manage.py init_dev_users
  ```

---

## 📋 REGLA DE ORO DE DESARROLLO

Una vez sincronizada la rama de tu equipo, **nunca programes directo sobre ella**. Crea siempre tu rama secundaria de trabajo:

```bash
git checkout -b feat/nombre-de-tu-tarea
```
