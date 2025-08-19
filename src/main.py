from fastapi import FastAPI
from .auth.router import router as auth_router
from .projects.router import router as projects_router
from .tasks.router import router as tasks_router

app = FastAPI(
    title="Task Manager API",
    description="API untuk mengelola proyek dan tugas pribadi.",
    version="1.0.0",
)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint root untuk mengecek status API."""
    return {"status": "OK", "message": "Welcome to Task Manager API!"}

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(tasks_router)