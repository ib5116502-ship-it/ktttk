from sqlalchemy.orm import Session

from app.models import Project
from app.projects.schemas import ProjectCreate, ProjectUpdate


# Создание проекта
def create_project(
    db: Session,
    project_data: ProjectCreate,
    owner_id: int
):
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# Получение всех проектов пользователя
def get_user_projects(db: Session, owner_id: int):
    return db.query(Project).filter(
        Project.owner_id == owner_id
    ).all()


# Получение одного проекта
def get_project_by_id(
    db: Session,
    project_id: int,
    owner_id: int
):
    return db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == owner_id
    ).first()


# Обновление проекта
def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate
):
    update_data = project_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(db: Session, project: Project):
    db.delete(project)
    db.commit()

    return True