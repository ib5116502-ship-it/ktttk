from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.projects.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.projects.service import (
    create_project,
    get_user_projects,
    get_project_by_id,
    update_project,
    delete_project
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# 1. Создание проекта
@router.post("/", response_model=ProjectResponse, status_code=201)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_project(
        db=db,
        project_data=project_data,
        owner_id=current_user.id
    )


# 2. Получение всех проектов пользователя
@router.get("/", response_model=list[ProjectResponse])
def read_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_projects(db, current_user.id)


# 3. Получение одного проекта
@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(
        db,
        project_id,
        current_user.id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project


# 4. Обновление проекта
@router.put("/{project_id}", response_model=ProjectResponse)
def edit_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(
        db,
        project_id,
        current_user.id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return update_project(db, project, project_data)


# 5. Удаление проекта
@router.delete("/{project_id}")
def remove_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(
        db,
        project_id,
        current_user.id
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    delete_project(db, project)

    return {
        "message": "Project deleted successfully"
    }