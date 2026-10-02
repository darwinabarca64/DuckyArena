# 🐥 GUÍA FÁCIL DE GIT Y GITHUB — quizArenas

¡Bienvenido al equipo de desarrollo! Si nunca has usado Git o GitHub, no te preocupes. Sigue esta guía paso a paso y no tendrás ningún problema.

---

## 👥 ¿EN QUÉ EQUIPO ESTÁS?

El proyecto está dividido en dos partes. Debes saber a cuál perteneces:
- **PARTE 1 (quizzes - Rama: `parte-1-quizzes`):**
  * Sasha (@sashasafont)
  * Nacho (@nachopython)
  * Robert Betancourt (@Trevor783)
- **PARTE 2 (quiz_games - Rama: `parte-2-quizgames`):**
  * @dalcolea
  * Thais (@thaishps3)
- **MENTOR / AUDITORÍA:**
  * Oscar Burgos (@mihifidem)
- **LEAD / APROBADOR:**
  * Darwin (@darwinabarca64)

---

## ⚙️ PASO 1: PREPARAR EL PROYECTO EN TU COMPUTADORA (SOLO LA PRIMERA VEZ)

1. Abre tu terminal (recomendamos **Git Bash** en Windows).
2. Descarga una copia del proyecto escribiendo:
   ```bash
   git clone https://github.com/darwinabarca64/DuckyArena.git
   ```
3. Entra a la carpeta del proyecto:
   ```bash
   cd DuckyArena
   ```
   *(o `cd DuckyQuizzArena` según el nombre de la carpeta descargada)*
4. Configura tu nombre y correo para que GitHub sepa quién eres:
   ```bash
   git config --global user.name "Tu Nombre y Apellido"
   git config --global user.email "tu-correo-de-github@ejemplo.com"
   ```

---

## 🚀 PASO 2: CREAR TU RAMA DE TRABAJO (CADA VEZ QUE VAYAS A HACER ALGO)

> ⚠️ **REGLA DE ORO:** Nunca programes directamente en `main`, ni en `parte-1-quizzes`, ni en `parte-2-quizgames`. Siempre crea tu propia rama personal.
> 
> 🔄 **¿Ya tienes una copia y quieres actualizarla con los últimos cambios de Daphne/Channels/WebSockets?** Consulta el [**Protocolo de Sincronización Oficial (`github_management.md`)**](file:///c:/Users/Dar/Desktop/Python/DuckyQuizzArena/docs/guides/github_management.md).

### Si estás en el Equipo de la PARTE 1:
```bash
# 1. Ve a la rama de tu equipo
git checkout parte-1-quizzes

# 2. Descarga los últimos cambios que existan
git pull origin parte-1-quizzes

# 3. Crea tu rama personal (ejemplo: mi-nombre-tarea)
git checkout -b mi-nombre-tarea
```

### Si estás en el Equipo de la PARTE 2:
```bash
# 1. Ve a la rama de tu equipo
git checkout parte-2-quizgames

# 2. Descarga los últimos cambios que existan
git pull origin parte-2-quizgames

# 3. Crea tu rama personal (ejemplo: mi-nombre-tarea)
git checkout -b mi-nombre-tarea
```

---

## 💻 PASO 3: PROGRAMAR Y GUARDAR TUS CAMBIOS

Ahora abre tu editor (VS Code, Cursor, etc.), programa tus tareas y prueba que todo funcione.

Cuando termines:
1. Abre la terminal en la carpeta del proyecto.
2. Revisa qué archivos modificaste:
   ```bash
   git status
   ```
3. Prepara los archivos para guardarlos:
   ```bash
   git add .
   ```
4. Guarda un punto de control con un mensaje claro que explique qué hiciste:
   ```bash
   git commit -m "feat: agregue el boton de iniciar sala con estilos"
   ```

---

## ☁️ PASO 4: SUBIR TUS CAMBIOS A GITHUB

Sube tu rama personal a la web de GitHub con este comando:
```bash
git push -u origin mi-nombre-tarea
```
*(Sustituye "mi-nombre-tarea" por el nombre exacto de la rama que creaste en el Paso 2).*

---

## 🔍 PASO 5: SOLICITAR REVISIÓN (PULL REQUEST)

1. Abre tu navegador e ingresa a: **https://github.com/darwinabarca64/DuckyArena**
2. Verás un botón amarillo que dice: **"Compare & pull request"**. Haz clic en él.
3. **MUY IMPORTANTE (Destino de la fusión):**
   * En la casilla izquierda llamada **base:** selecciona la rama de tu equipo (`parte-1-quizzes` o `parte-2-quizgames`).
   * En la casilla derecha llamada **compare:** debe aparecer tu rama personal.
4. Escribe un título breve y explica qué hiciste en la descripción.
5. Haz clic en el botón verde: **"Create pull request"**.
6. ¡Listo! El Lead revisará tu código. Si todo cumple las reglas, lo integrará al proyecto. Si hay algo que corregir, te dejará un comentario para que lo ajustes.

---

## 🆘 ¿QUÉ HACER SI TE TRABAS O ALGO SALE MAL?
- **Para saber en qué rama estás:** `git branch`
- **Para cancelar cambios no guardados:** `git restore .`
- **Para salir de una pantalla extraña en la terminal:** Presiona la tecla `q` o escribe `:q!` y presiona `Enter`.
