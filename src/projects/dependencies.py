from fastapi import Depends
from sqlalchemy.orm import Session

from . import service, exceptions
from ..database import get_db
from ..auth.models import User
from ..auth.dependencies import get_current_active_user

def get_project_or_404(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Dependency untuk mendapatkan project berdasarkan ID dan memastikan
    user yang login adalah pemiliknya.
    """
    project = service.get_project_by_id(db, project_id)
    
    if not project:
        raise exceptions.ProjectNotFoundException
        
    if project.owner_id != current_user.id:
        raise exceptions.ProjectAccessForbiddenException
        
    return project