from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description : str
    done : bool = False

class TaskUpdate(BaseModel):
    title: str
    description: str
    done: bool
    updated_at: datetime

class TaskResponse(BaseModel):
    title: str
    description : str
    id: int
    done: bool
    created_at: datetime
    updated_at: datetime

    class Config():
        orm_mode = True