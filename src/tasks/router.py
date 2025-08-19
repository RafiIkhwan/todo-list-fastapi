from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import schemas, service, exceptions
from ..database import get_db
from ..projects.models import Project
from ..projects.dependencies import get_project_or_404

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task: schemas.TaskCreate,
    project: Project = Depends(get_project_or_404),
    db: Session = Depends(get_db)
):
    """Membuat task baru di dalam project spesifik."""
    return service.create_task_for_project(db=db, task=task, project_id=project.id)

@router.get("/", response_model=List[schemas.TaskRead])
def read_project_tasks(project: Project = Depends(get_project_or_404)):
    """Membaca semua task dari project spesifik."""
    return project.tasks

@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_existing_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    project: Project = Depends(get_project_or_404), # Memastikan user punya akses ke project
    db: Session = Depends(get_db)
):
    """Memperbarui task yang ada."""
    task = service.get_task_by_id(db, task_id)
    if not task or task.project_id != project.id:
        raise exceptions.TaskNotFoundException
    
    return service.update_task(db=db, task_id=task_id, task_data=task_data)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    project: Project = Depends(get_project_or_404), # Memastikan user punya akses ke project
    db: Session = Depends(get_db)
):
    """Menghapus task yang ada."""
    task = service.get_task_by_id(db, task_id)
    if not task or task.project_id != project.id:
        raise exceptions.TaskNotFoundException
        
    service.delete_task(db=db, task_id=task_id)
    return