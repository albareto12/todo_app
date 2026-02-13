# ToDo App con Reports (creator / executor) — README incremental (guía para aprender)

Este repositorio es tu cuaderno de trabajo para construir, paso a paso, una aplicación ToDo profesional con FastAPI (backend), React (frontend) y soporte para generación de reportes asistida por un LLM. Estoy actuando como tu compañero desarrollador: te explico qué hacer, por qué y en qué orden, y añadiremos contenido y ejemplos en este README conforme implementes cada parte.

## Estado actual
- ✅ Repo creado con .gitignore
- ✅ Infraestructura Docker configurada (Postgres + smtp4dev)
- ✅ Backend skeleton creado con FastAPI
- ⏳ Próximo: Crear modelos de datos y probar con Docker

## Cómo usar este README
- Lee la sección "Plan incremental" para ver los micro‑pasos que haremos.
- Cuando quieras que añadamos el contenido de un paso (código, comandos, ejemplos), dilo y lo añado en la sección correspondiente junto con instrucciones detalladas y fragmentos listos para pegar.
- Cada sección incluirá: objetivo, lo que aprenderás, archivos que crearemos, comandos a ejecutar y criterios de éxito.

---

## Plan incremental (marcaremos y completaremos conforme avance el trabajo)

- [x] **0. Preparar repo y entorno local**  
  - Objetivo: crear repo, rama de trabajo y activar virtualenv.  
  - Aprenderás: comandos Git básicos, virtualenv en Windows, comprobación de versiones.
  - ✅ Completado: Repo creado, rama `feat/infra` activa, virtualenv configurado.

- [x] **1. Infra con Docker (Postgres + smtp4dev + contenedor web esqueleto)**  
  - Objetivo: levantar servicios dependientes que usaremos durante el desarrollo.  
  - Aprenderás: docker compose, redes entre contenedores, servicio SMTP de prueba.  
  - Archivos: `docker-compose.yml`, `backend/Dockerfile`, `backend/.env.example`.
  - ✅ Completado: docker-compose.yml configurado con PostgreSQL y smtp4dev.

- [x] **2. Scaffolding del backend (estructura y requirements)**  
  - Objetivo: crear la estructura de carpetas y listar dependencias.  
  - Aprenderás: organización de un proyecto FastAPI y cómo preparar requirements.  
  - Archivos: `backend/requirements.txt`, `backend/app/` (main.py, routers, etc.).
  - ✅ Completado: Ver detalles abajo.

- [ ] **3. Conexión a la base de datos con SQLAlchemy**  
  - Objetivo: implementar `database.py` y la dependencia `get_db`.  
  - Aprenderás: engine, SessionLocal, Base y patrón de dependencias en FastAPI.
  - ✅ Implementado en `backend/app/database.py` - falta probar con Postgres en Docker.

- [ ] **4. Modelos y schemas (User, Task, Report, ReportDraft)**  
  - Objetivo: diseñar los modelos SQLAlchemy y Pydantic schemas.  
  - Aprenderás: relaciones, Enums, orm_mode y buenas prácticas.  
  - Incluiré los modelos paso a paso y las migraciones de ejemplo.

- [ ] **5. Alembic: migraciones**  
  - Objetivo: versionar el esquema y aplicar la migración inicial a la DB.  
  - Aprenderás: configurar alembic/env.py, generar `autogenerate` y ejecutar `upgrade head`.

- [ ] **6. Autenticación: registro/login con JWT**  
  - Objetivo: endpoints de registro y token con acceso controlado.  
  - Aprenderás: hashing con passlib, tokens con python-jose, OAuth2PasswordBearer.  
  - Implementaremos pruebas básicas para asegurar el flujo.

- [ ] **7. Endpoints de Task (creator / executor)**  
  - Objetivo: CRUD de tareas, asignación de executor y reglas de permiso.  
  - Aprenderás: validaciones, control de permisos y diseño REST.

- [ ] **8. Endpoint Report + BackgroundTasks + envío de correo**  
  - Objetivo: que el executor genere el report final, marca la tarea como `completed` y envía correos a creator y executor usando smtp4dev.  
  - Aprenderás: BackgroundTasks, smtplib/servicios SMTP, plantillas de email y pruebas en smtp4dev.

- [ ] **9. Integración LLM para generar borradores de reportes**  
  - Objetivo: endpoint que genera un borrador usando un LLM (OpenAI/Hugging Face/local) y lo devuelve para que el executor lo edite.  
  - Aprenderás: diseño de prompt, trazabilidad (ReportDraft), seguridad y privacidad, caching y límites.  
  - Añadiré la plantilla de prompt y el contrato del endpoint cuando me confirmes proveedor y políticas.

- [ ] **10. Adjuntos y almacenamiento (MinIO/S3 opcional)**  
  - Objetivo: permitir subir archivos al reporte y guardarlos de forma segura.  
  - Aprenderás: multipart uploads, MinIO en Docker y políticas de acceso.

- [ ] **11. Tests (pytest, httpx, mocking SMTP y LLM)**  
  - Objetivo: cubrir endpoints críticos con tests automatizados.  
  - Aprenderás: fixtures, TestClient/AsyncClient, mockeo de servicios externos.

- [ ] **12. Docker final del backend y pruebas E2E**  
  - Objetivo: construir la imagen definitiva y levantar la stack completa para demostración.  
  - Aprenderás: optimización de Dockerfile, manejo de dependencias nativas (libpq), healthchecks.

- [ ] **13. Frontend React (Vite + TypeScript + Tailwind)**  
  - Objetivo: UI con login, listado, detalle de tarea y formulario de reporte con botón "Generar borrador (AI)".  
  - Aprenderás: manejo de tokens, llamadas a la API, formularios y toasts.

- [ ] **14. CI/CD y despliegue (opcional)**  
  - Objetivo: automatizar tests y despliegue (GitHub Actions, Render/Railway).  
  - Aprenderás: pipelines, build images y secretos en CI.

---

## ✅ Paso 2 Completado: Scaffolding del Backend

### 📂 Estructura creada

```
backend/
├── Dockerfile                  # Configuración Docker del backend
├── .env.example               # Plantilla de variables de entorno
├── requirements.txt           # Dependencias Python
└── app/
    ├── __init__.py           # Módulo principal
    ├── main.py               # Aplicación FastAPI
    ├── database.py           # Configuración SQLAlchemy
    ├── models/               # Modelos de datos (SQLAlchemy)
    │   └── __init__.py
    ├── schemas/              # Schemas de validación (Pydantic)
    │   └── __init__.py
    ├── routers/              # Endpoints organizados
    │   └── __init__.py
    └── services/             # Lógica de negocio
        └── __init__.py
```

### 🎯 Archivos principales

#### **requirements.txt**
Dependencias instaladas:
- **FastAPI + Uvicorn**: Framework web y servidor ASGI
- **SQLAlchemy + psycopg2**: ORM y driver PostgreSQL
- **Pydantic**: Validación de datos
- **python-jose + passlib**: Autenticación JWT y hashing
- **Alembic**: Migraciones de BD

#### **main.py**
- ✅ Aplicación FastAPI básica
- ✅ CORS configurado para desarrollo
- ✅ Endpoints: `/` y `/health`
- ✅ Documentación automática en `/docs`

#### **database.py**
- ✅ Engine SQLAlchemy configurado
- ✅ SessionLocal para sesiones de BD
- ✅ Base declarativa para modelos
- ✅ Dependencia `get_db()` para FastAPI

#### **Dockerfile**
- ✅ Imagen Python 3.11-slim
- ✅ Instalación de dependencias del sistema
- ✅ Auto-reload para desarrollo

### ⚙️ Comandos para probar localmente

```powershell
# 1. Crear archivo .env
cd backend
copy .env.example .env

# 2. Activar virtualenv
..\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar servidor
uvicorn app.main:app --reload
```

### 🌐 Verificación

Abre en tu navegador:
- http://127.0.0.1:8000 → API info
- http://127.0.0.1:8000/health → Health check
- http://127.0.0.1:8000/docs → Swagger UI (documentación interactiva)

### ✅ Criterios de éxito
- [x] Estructura de carpetas creada
- [x] Todos los archivos tienen contenido
- [x] FastAPI arranca sin errores
- [x] Endpoints responden correctamente
- [x] Documentación automática funciona

---

## Cómo documentaremos el progreso aquí
- Cada vez que completes un micro‑paso, lo marcaré como hecho y añadiré:
  - El código del/los archivos creados (si tú me autorizas) en bloques listos para copiar/pegar.
  - Los comandos exactos para ejecutarlos (PowerShell).
  - Una breve lista de pruebas que debes ejecutar para verificar que todo funciona.
  - Problemas comunes y cómo solucionarlos.

## Buenas prácticas que aplicaremos desde el inicio
- Hacemos commits pequeños y descriptivos por cada micro‑paso.
- No subimos `.env` ni secretos al repositorio.
- Usamos docker-compose para infra reproducible y smtp4dev para ver correos de desarrollo.
- Guardamos drafts generados por LLM en la BD para trazabilidad (opcional; lo discutiremos y lo implementamos según lo decidas).

## Notas sobre privacidad y LLM
- Los borradores generados por el LLM pueden contener datos de la tarea; antes de enviar datos a un proveedor externo consideraremos la sensibilidad y te mostraré cómo configurar un LLM local si lo prefieres.

## Contacto rápido y flujo de trabajo contigo
- Tú pides: "Mostrar archivo X" o "Crea archivo Y" cuando quieras que genere el contenido exacto.  
- Yo te doy: el contenido listo, una explicación línea por línea si la pides, y los comandos para probar.  
- Tú haces: pegas/guardas los archivos, ejecutas los comandos y me dices los resultados.

## 📅 Registro de cambios

- **2026-02-13**: Completado Paso 2 - Skeleton del backend con FastAPI, estructura de carpetas, requirements y configuración base.
- **2025-11-20**: Se creó README incremental y .gitignore; configurado docker-compose con Postgres y smtp4dev.
