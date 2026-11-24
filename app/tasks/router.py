from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.tasks.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.tasks.service import (
    create_task,
    get_user_tasks,
    get_task_by_id,
    update_task,
    delete_task
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# 1. Создание задачи
@router.post("/", response_model=TaskResponse, status_code=201)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = create_task(db, task_data, current_user.id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Project or assigned user not found"
        )

    return task


# 2. Получение всех задач пользователя
@router.get("/", response_model=list[TaskResponse])
def read_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_tasks(db, current_user.id)


# 3. Получение одной задачи
@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(db, task_id, current_user.id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# 4. Обновление задачи
@router.put("/{task_id}", response_model=TaskResponse)
def edit_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(db, task_id, current_user.id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return update_task(db, task, task_data)


# 5. Удаление задачи
@router.delete("/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(db, task_id, current_user.id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    delete_task(db, task)

    return {
        "message": "Task deleted successfully"
    }