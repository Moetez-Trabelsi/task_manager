from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List
from app.oauth2 import get_current_user

router = APIRouter()

@router.post("/", status_code=201, response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, current_user:models.User= Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump(), owner_id=current_user.id, is_completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(
    current_user:models.User= Depends(get_current_user), 
    db: Session = Depends(get_db),
    is_completed:bool=Query(None),
    limit: int = Query(10),
    skip: int = Query(0)
    ):
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)

    if is_completed is not None:
        query = query.filter(models.Task.is_completed == is_completed)

    tasks=query.offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, current_user:models.User= Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, updated_task: schemas.TaskUpdate, current_user:models.User= Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in updated_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, current_user:models.User= Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}