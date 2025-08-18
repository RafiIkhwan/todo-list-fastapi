from pydantic import BaseModel
from typing import List
from ..tasks.schemas import TaskRead

class ProjectBase(BaseModel):
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class ProjectReadWithTasks(ProjectRead):
    tasks: List[TaskRead] = []