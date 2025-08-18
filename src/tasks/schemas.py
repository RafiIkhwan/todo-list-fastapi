from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    is_completed: bool

class TaskRead(TaskBase):
    id: int
    is_completed: bool
    project_id: int

    class Config:
        from_attributes = True