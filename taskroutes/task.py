from fastapi import APIRouter, HTTPException, Depends


from sqlalchemy.orm import Session

from db.db_setup import get_db
from db.models.task import Task
from pydantic_schemas.task import TaskCreate, TaskUpdate, TaskResponse
from dependencies.currentuser import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/")
async def create_task(
    task: TaskCreate, 
    db:Session = Depends(get_db), 
    current_user : dict = Depends(get_current_user)
):
  
    new_task = Task(
        title = task.title,
        description = task.description,
        user_id = current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return{
        "message" : "Task Added.",
        "task": {
            "id":new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "done": new_task.done,
            "created_at": new_task.created_at,
        },
    }
    
@router.get("/get-all-tasks")
async def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()

    return {
        "message" : "Tasks Retrieved.",
        "tasks" : tasks
    }

@router.get("/{task_id}")
async def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not Found")
    
    return {
        "message": "Task retrieved successfully.",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "done": task.done,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
    }

@router.put("/{task_id}")
async def update_task(
        task_id: int,
        updated_task: TaskUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = updated_task.title
    task.description = updated_task.description
    task.done = updated_task.done
    task.updated_at = updated_task.updated_at

    db.commit()
    db.refresh(task)

    return {
        "message" : "Task updated Successfully",
        "task": {
            "id" : task.id,
            "title": task.title,
            "description": task.description,
            "done" : task.done,
            "created-at": task.created_at,
            "updated-at": task.updated_at
        }
    }

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description
        }
    }