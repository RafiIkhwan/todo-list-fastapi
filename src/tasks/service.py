from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from ..projects.models import Project

def create_task_for_project(db: Session, task: schemas.TaskCreate, project_id: int) -> models.Task:
    """Membuat task baru dalam sebuah project."""
    db_task = models.Task(**task.model_dump(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task_by_id(db: Session, task_id: int) -> Optional[models.Task]:
    """Mendapatkan task berdasarkan ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_project(db: Session, project_id: int) -> List[models.Task]:
    """Mendapatkan semua task dari sebuah project."""
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate) -> Optional[models.Task]:
    """Memperbarui data task."""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
        
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Menghapus task."""
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
        
    db.delete(db_task)
    db.commit()
    return db_task