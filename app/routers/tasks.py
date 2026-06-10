from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter()

@router.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, owner_id: int, db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump(), owner_id=owner_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(owner_id: int, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == owner_id).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, owner_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == owner_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, owner_id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == owner_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, owner_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == owner_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}