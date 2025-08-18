from fastapi import FastAPI

app = FastAPI(title="Task Manager API")

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint root untuk mengecek apakah server berjalan.
    """
    return {"message": "Welcome to the Task Manager API! ✅"}

# Di sini nanti kita akan meng-include router dari auth, projects, dan tasks
# from .auth.router import router as auth_router
# from .projects.router import router as projects_router
#
# app.include_router(auth_router)
# app.include_router(projects_router)