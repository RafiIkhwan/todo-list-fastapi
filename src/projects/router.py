from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import schemas, service
from ..database import get_db
from ..auth.dependencies import get_current_active_user
from ..auth.models import User
from .dependencies import get_project_or_404

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_new_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Membuat project baru."""
    return service.create_project(db=db, project=project, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.ProjectRead])
def read_user_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Membaca semua project milik user yang sedang login."""
    projects = service.get_projects_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=schemas.ProjectReadWithTasks)
def read_single_project(project = Depends(get_project_or_404)):
    """Membaca satu project spesifik beserta semua task di dalamnya."""
    return project

@router.put("/{project_id}", response_model=schemas.ProjectRead)
def update_existing_project(
    project_data: schemas.ProjectUpdate,
    project = Depends(get_project_or_404),
    db: Session = Depends(get_db)
):
    """Memperbarui project yang ada."""
    return service.update_project(db=db, project_id=project.id, project_data=project_data)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_project(
    project = Depends(get_project_or_404),
    db: Session = Depends(get_db)
):
    """Menghapus project yang ada."""
    service.delete_project(db=db, project_id=project.id)
    return