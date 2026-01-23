# ToDo App con Reports (creator / executor) — README incremental (guía para aprender)

Este repositorio es tu cuaderno de trabajo para construir, paso a paso, una aplicación ToDo profesional con FastAPI (backend), React (frontend) y soporte para generación de reportes asistida por un LLM. Estoy actuando como tu compañero desarrollador: te explico qué hacer, por qué y en qué orden, y añadiremos contenido y ejemplos en este README conforme implementes cada parte.

## Estado actual
- ✅ README incremental y .gitignore creados
- ✅ docker-compose.yml configurado (servicios base: PostgreSQL y smtp4dev)
- El resto del proyecto (backend, frontend, tests, integración LLM) se irá documentando aquí conforme vayamos construyendo cada parte.

## Prerrequisitos

Antes de empezar, asegúrate de tener instalado en tu sistema:

1. **Git** (para clonar y versionar el código)
   - Descarga: https://git-scm.com/downloads
   - Verifica: `git --version` (debe mostrar una versión como 2.x.x)

2. **Docker Desktop** (para levantar la infraestructura)
   - Descarga: https://www.docker.com/products/docker-desktop
   - Verifica: `docker --version` y `docker-compose --version`
   - Asegúrate que Docker Desktop esté ejecutándose

3. **Python 3.10+** (para el backend)
   - Descarga: https://www.python.org/downloads/
   - Verifica: `python --version` o `python3 --version`
   - **Importante en Windows**: Marca la opción "Add Python to PATH" durante la instalación

4. **Node.js 18+** (para el frontend)
   - Descarga: https://nodejs.org/
   - Verifica: `node --version` y `npm --version`

5. **Editor de código** (recomendado)
   - Visual Studio Code: https://code.visualstudio.com/
   - Con extensiones: Python, ESLint, Prettier

Cómo usar este README
- Lee la sección "Plan incremental" para ver los micro‑pasos que haremos.
- Cuando quieras que añadamos el contenido de un paso (código, comandos, ejemplos), dilo y lo añado en la sección correspondiente junto con instrucciones detalladas y fragmentos listos para pegar.
- Cada sección incluirá: objetivo, lo que aprenderás, archivos que crearemos, comandos a ejecutar y criterios de éxito.

Plan incremental (marcaremos y completaremos conforme avance el trabajo)

### ✅ Paso 0: Preparar repo y entorno local

**Objetivo**: Configurar tu entorno de desarrollo local y verificar que todo funciona.

**Lo que aprenderás**: 
- Comandos Git básicos (clone, branch, status, commit, push)
- Virtualenv en Python para aislar dependencias
- Verificación de versiones de herramientas

**Comandos a ejecutar**:

1. **Verificar prerrequisitos** (PowerShell o CMD en Windows / Terminal en Mac/Linux):
   ```bash
   # Verificar Git
   git --version
   
   # Verificar Docker
   docker --version
   docker-compose --version
   
   # Verificar Python
   python --version
   # o en algunos sistemas:
   python3 --version
   
   # Verificar Node.js
   node --version
   npm --version
   ```

2. **Si ya clonaste el repo, navega al directorio**:
   ```bash
   cd ruta/donde/clonaste/todo_app
   ```

3. **Verificar que estás en la rama correcta**:
   ```bash
   git status
   git branch
   ```

4. **Crear y activar entorno virtual de Python** (para el backend):
   
   En **Windows** (PowerShell):
   ```powershell
   # Crear entorno virtual
   python -m venv .venv
   
   # Activar entorno virtual
   .\.venv\Scripts\Activate.ps1
   
   # Si aparece error de permisos, ejecuta primero:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   
   En **Windows** (CMD):
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```
   
   En **Mac/Linux**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Actualizar pip** (gestor de paquetes de Python):
   ```bash
   python -m pip install --upgrade pip
   ```

**Criterios de éxito**:
- ✅ Todos los comandos de verificación muestran versiones correctas
- ✅ El entorno virtual está activado (verás `(.venv)` al inicio de tu terminal)
- ✅ `git status` muestra que estás en la rama correcta sin cambios pendientes

**Problemas comunes**:
- **Error al activar virtualenv en Windows**: Ejecuta `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Python no reconocido**: Añade Python a la variable PATH del sistema
- **Docker no funciona**: Asegúrate de que Docker Desktop esté ejecutándose

---

### [ ] Paso 1: Infraestructura con Docker (Postgres + smtp4dev)

**Objetivo**: Levantar servicios de infraestructura (base de datos PostgreSQL y servidor SMTP de prueba) usando Docker.

**Lo que aprenderás**:
- Cómo funciona `docker compose` para orquestar múltiples contenedores
- Configuración de PostgreSQL para desarrollo
- Servicio SMTP de prueba (smtp4dev) para ver correos sin enviarlos realmente
- Redes entre contenedores Docker

**Archivos ya configurados**:
- ✅ `docker-compose.yml` - Define los servicios: db (PostgreSQL) y smtp (smtp4dev)

**Comandos a ejecutar**:

1. **Levantar los servicios** (desde la raíz del proyecto):
   ```bash
   docker compose up -d
   ```
   - `-d` = modo "detached" (en segundo plano)
   - Descargará las imágenes si es la primera vez (puede tardar unos minutos)

2. **Verificar que los contenedores están corriendo**:
   ```bash
   docker compose ps
   ```
   - Deberías ver 2 servicios: `db` y `smtp`, ambos en estado "Up"

3. **Ver los logs de los servicios** (opcional, útil para debugging):
   ```bash
   # Ver todos los logs
   docker compose logs
   
   # Ver logs de un servicio específico
   docker compose logs db
   docker compose logs smtp
   
   # Seguir los logs en tiempo real
   docker compose logs -f
   ```

4. **Probar la conexión a PostgreSQL**:
   
   Opción A - Desde la terminal con `psql` (si lo tienes instalado):
   ```bash
   psql -h localhost -U todo_user -d todo_db
   # Contraseña: todo_pass
   # Luego ejecuta: \dt para ver tablas (estará vacío por ahora)
   # Salir: \q
   ```
   
   Opción B - Usar una herramienta gráfica como:
   - **DBeaver** (gratuito): https://dbeaver.io/
   - **pgAdmin**: https://www.pgadmin.org/
   - **TablePlus**: https://tableplus.com/
   
   Datos de conexión:
   - Host: `localhost`
   - Puerto: `5432`
   - Usuario: `todo_user`
   - Contraseña: `todo_pass`
   - Base de datos: `todo_db`

5. **Probar smtp4dev (interfaz web para correos)**:
   - Abre tu navegador en: http://localhost:3000
   - Verás una interfaz donde aparecerán los correos que la app envíe durante desarrollo
   - Por ahora estará vacía (enviaremos correos en pasos posteriores)

6. **Detener los servicios cuando termines**:
   ```bash
   # Detener sin eliminar los contenedores
   docker compose stop
   
   # Detener y eliminar contenedores (pero conserva los datos en volumes)
   docker compose down
   
   # Eliminar TODO incluyendo datos (⚠️ CUIDADO)
   docker compose down -v
   ```

**Criterios de éxito**:
- ✅ `docker compose ps` muestra ambos servicios en estado "Up"
- ✅ Puedes conectarte a PostgreSQL en localhost:5432
- ✅ Puedes ver la interfaz de smtp4dev en http://localhost:3000
- ✅ No hay errores en los logs (`docker compose logs`)

**Problemas comunes**:
- **Puerto 5432 ya en uso**: Tienes PostgreSQL instalado localmente. Opción 1: Detén tu PostgreSQL local. Opción 2: Cambia el puerto en docker-compose.yml (ej: "5433:5432")
- **Puerto 3000 ya en uso**: Cambia el puerto en docker-compose.yml (ej: "3001:80")
- **Docker daemon no está corriendo**: Abre Docker Desktop y espera a que inicie
- **Error de permisos en volúmenes**: En Windows, asegúrate de que Docker Desktop tenga acceso a la unidad donde está el proyecto

**Notas importantes**:
- Los datos de PostgreSQL se guardan en un volumen Docker llamado `db_data`, así que persisten aunque detengas los contenedores
- smtp4dev NO envía correos realmente, solo los muestra en su interfaz - perfecto para desarrollo
- El servicio `web` (backend) está comentado en docker-compose.yml porque aún no hemos creado el directorio backend

---

### [ ] Paso 2: Scaffolding del backend (estructura y requirements)

**Objetivo**: Crear la estructura de directorios del proyecto backend y definir las dependencias.

**Lo que aprenderás**: 
- Organización profesional de un proyecto FastAPI
- Cómo estructurar el código en módulos (routers, models, schemas, services)
- Gestión de dependencias con requirements.txt

**Estructura que crearemos**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── database.py          # Configuración de SQLAlchemy
│   ├── models/              # Modelos de la base de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── report.py
│   ├── schemas/             # Schemas de validación (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── report.py
│   ├── routers/             # Endpoints organizados por dominio
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── reports.py
│   ├── services/            # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── email.py
│   │   └── llm.py
│   └── utils/               # Utilidades (JWT, hashing, etc.)
│       ├── __init__.py
│       ├── security.py
│       └── dependencies.py
├── alembic/                 # Migraciones de base de datos
├── tests/                   # Tests automatizados
├── .env.example             # Plantilla de variables de entorno
├── .env                     # Variables de entorno (NO subir a git)
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Para construir la imagen Docker
└── README.md                # Documentación del backend
```

**Archivos que crearemos en este paso** (te los proporcionaré cuando estés listo):
- `backend/requirements.txt` - Lista de todas las dependencias
- `backend/.env.example` - Plantilla de configuración
- `backend/Dockerfile` - Para construir la imagen del contenedor
- Estructura básica de directorios vacíos

**Principales dependencias que usaremos**:
- `fastapi` - Framework web
- `uvicorn[standard]` - Servidor ASGI
- `sqlalchemy` - ORM para base de datos
- `psycopg2-binary` - Driver de PostgreSQL
- `alembic` - Migraciones de base de datos
- `pydantic[email]` - Validación de datos
- `python-jose[cryptography]` - Manejo de JWT
- `passlib[bcrypt]` - Hashing de contraseñas
- `python-multipart` - Para subir archivos
- `aiosmtplib` - Cliente SMTP asíncrono
- `openai` - (Opcional) Cliente para OpenAI API

**Comando para instalar dependencias** (ejecutar después de crear requirements.txt):
```bash
# Asegúrate de tener el entorno virtual activado
pip install -r backend/requirements.txt
```

---

### [ ] Paso 3: Conexión a la base de datos con SQLAlchemy
  - Objetivo: Implementar `database.py` y la dependencia `get_db`.  
  - Aprenderás: Engine, SessionLocal, Base y patrón de dependencias en FastAPI.  
  - Te mostraré el código y pruebas para ejecutar contra Postgres en Docker.

### [ ] Paso 4: Modelos y schemas (User, Task, Report, ReportDraft)
  - Objetivo: Diseñar los modelos SQLAlchemy y Pydantic schemas.  
  - Aprenderás: Relaciones, Enums, orm_mode y buenas prácticas.  
  - Incluiré los modelos paso a paso y las migraciones de ejemplo.

### [ ] Paso 5: Alembic - migraciones de base de datos
  - Objetivo: Versionar el esquema y aplicar la migración inicial a la DB.  
  - Aprenderás: Configurar alembic/env.py, generar `autogenerate` y ejecutar `upgrade head`.

### [ ] Paso 6: Autenticación - registro/login con JWT
  - Objetivo: Endpoints de registro y token con acceso controlado.  
  - Aprenderás: Hashing con passlib, tokens con python-jose, OAuth2PasswordBearer.  
  - Implementaremos pruebas básicas para asegurar el flujo.

### [ ] Paso 7: Endpoints de Task (creator / executor)
  - Objetivo: CRUD de tareas, asignación de executor y reglas de permiso.  
  - Aprenderás: Validaciones, control de permisos y diseño REST.

### [ ] Paso 8: Endpoint Report + BackgroundTasks + envío de correo
  - Objetivo: Que el executor genere el report final, marque la tarea como `completed` y envíe correos a creator y executor usando smtp4dev.  
  - Aprenderás: BackgroundTasks, smtplib/servicios SMTP, plantillas de email y pruebas en smtp4dev.

### [ ] Paso 9: Integración LLM para generar borradores de reportes
  - Objetivo: Endpoint que genera un borrador usando un LLM (OpenAI/Hugging Face/local) y lo devuelve para que el executor lo edite.  
  - Aprenderás: Diseño de prompt, trazabilidad (ReportDraft), seguridad y privacidad, caching y límites.  
  - Añadiré la plantilla de prompt y el contrato del endpoint cuando me confirmes proveedor y políticas.

### [ ] Paso 10: Adjuntos y almacenamiento (MinIO/S3 opcional)
  - Objetivo: Permitir subir archivos al reporte y guardarlos de forma segura.  
  - Aprenderás: Multipart uploads, MinIO en Docker y políticas de acceso.

### [ ] Paso 11: Tests (pytest, httpx, mocking SMTP y LLM)
  - Objetivo: Cubrir endpoints críticos con tests automatizados.  
  - Aprenderás: Fixtures, TestClient/AsyncClient, mockeo de servicios externos.

### [ ] Paso 12: Docker final del backend y pruebas E2E
  - Objetivo: Construir la imagen definitiva y levantar la stack completa para demostración.  
  - Aprenderás: Optimización de Dockerfile, manejo de dependencias nativas (libpq), healthchecks.

### [ ] Paso 13: Frontend React (Vite + TypeScript + Tailwind)  
  - Objetivo: UI con login, listado, detalle de tarea y formulario de reporte con botón “Generar borrador (AI)”.  
  - Aprenderás: manejo de tokens, llamadas a la API, formularios y toasts.

- [ ] 14. CI/CD y despliegue (opcional)  
  - Objetivo: automatizar tests y despliegue (GitHub Actions, Render/Railway).  
  - Aprenderás: pipelines, build images y secretos en CI.

Cómo documentaremos el progreso aquí
- Cada vez que completes un micro‑paso, lo marcaré como hecho y añadiré:
  - El código del/los archivos creados (si tú me autorizas) en bloques listos para copiar/pegar.
  - Los comandos exactos para ejecutarlos (PowerShell).
  - Una breve lista de pruebas que debes ejecutar para verificar que todo funciona.
  - Problemas comunes y cómo solucionarlos.

Buenas prácticas que aplicaremos desde el inicio
- Hacemos commits pequeños y descriptivos por cada micro‑paso.
- No subimos `.env` ni secretos al repositorio.
- Usamos docker-compose para infra reproducible y smtp4dev para ver correos de desarrollo.
- Guardamos drafts generados por LLM en la BD para trazabilidad (opcional; lo discutiremos y lo implementamos según lo decidas).

Notas sobre privacidad y LLM
- Los borradores generados por el LLM pueden contener datos de la tarea; antes de enviar datos a un proveedor externo consideraremos la sensibilidad y te mostraré cómo configurar un LLM local si lo prefieres.

Contacto rápido y flujo de trabajo contigo
- Tú pedes: “Mostrar archivo X” o “Crea archivo Y” cuando quieras que genere el contenido exacto.  
- Yo te doy: el contenido listo, una explicación línea por línea si la pides, y los comandos para probar.  
- Tú haces: pegas/guardas los archivos, ejecutas los comandos y me dices los resultados.

Registro de cambios (se irá llenando)
- 2025-11-20: Se creó README incremental y .gitignore; punto de partida para el trabajo guiado.


---

## 🚀 ¿Por dónde empezar?

### Si acabas de clonar el repositorio:

1. **Lee la sección "Prerrequisitos"** arriba y verifica que tienes todo instalado
2. **Ejecuta el Paso 0** para configurar tu entorno local
3. **Levanta Docker con el Paso 1** para tener la base de datos y SMTP funcionando

### Si ya completaste algunos pasos:

- Marca los pasos completados en este README actualizando `[ ]` a `[x]`
- Revisa los "Criterios de éxito" de cada paso para asegurarte de que todo funciona
- Continúa con el siguiente paso en la secuencia

### ¿Necesitas ayuda?

Puedes pedirme:
- **Contenido completo de archivos**: "Dame el código completo de requirements.txt"
- **Explicaciones detalladas**: "Explícame qué hace SQLAlchemy"  
- **Solución a errores**: "Tengo este error al ejecutar docker-compose: [mensaje]"
- **Buenas prácticas**: "¿Cómo organizo los routers en FastAPI?"

---

## 📚 Recursos adicionales

### Documentación oficial
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **React**: https://react.dev/
- **Docker**: https://docs.docker.com/

### Tutoriales recomendados
- FastAPI Tutorial oficial: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy ORM Tutorial: https://docs.sqlalchemy.org/en/20/tutorial/
- React con TypeScript: https://react.dev/learn/typescript

---

