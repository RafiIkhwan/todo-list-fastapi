from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, exceptions
from ..auth.models import User

def create_project(db: Session, project: schemas.ProjectCreate, owner_id: int) -> models.Project:
    """Membuat project baru untuk user."""
    db_project = models.Project(**project.model_dump(), owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project_by_id(db: Session, project_id: int) -> Optional[models.Project]:
    """Mendapatkan project berdasarkan ID."""
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.Project]:
    """Mendapatkan semua project milik seorang user."""
    return db.query(models.Project).filter(models.Project.owner_id == owner_id).offset(skip).limit(limit).all()

def update_project(db: Session, project_id: int, project_data: schemas.ProjectUpdate) -> Optional[models.Project]:
    """Memperbarui data project."""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
    
    for key, value in project_data.model_dump().items():
        setattr(db_project, key, value)
        
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int) -> Optional[models.Project]:
    """Menghapus project."""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
        
    db.delete(db_project)
    db.commit()
    return db_project