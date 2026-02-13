"""
Punto de entrada principal de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ToDo App API",
    description="API para gestión de tareas con reporters asistidos por LLM",
    version="0.1.0",
)

# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Endpoint de health check
    """
    return {
        "message": "ToDo App API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar que la API está funcionando
    """
    return {"status": "healthy"}


# Aquí irán los routers cuando los creemos
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
# app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])