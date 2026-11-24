from sqlalchemy.orm import Session

from app.models import Task, Project, User
from app.tasks.schemas import TaskCreate, TaskUpdate
from app.worker.tasks import send_task_notification


# Создание задачи
def create_task(
    db: Session,
    task_data: TaskCreate,
    owner_id: int
):
    project = db.query(Project).filter(
        Project.id == task_data.project_id,
        Project.owner_id == owner_id
    ).first()

    if project is None:
        return None

    if task_data.assigned_to is not None:
        assignee = db.query(User).filter(
            User.id == task_data.assigned_to
        ).first()

        if assignee is None:
            return None

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        assigned_to=task_data.assigned_to,
        status="pending"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Отправляем уведомление в Celery
    user = db.query(User).filter(
        User.id == owner_id
    ).first()

    if user:
        send_task_notification.delay(
            new_task.title,
            user.email
        )

    return new_task


# Получение задач пользователя
def get_user_tasks(db: Session, owner_id: int):
    return (
        db.query(Task)
        .join(Project, Task.project_id == Project.id)
        .filter(Project.owner_id == owner_id)
        .all()
    )


# Получение одной задачи
def get_task_by_id(
    db: Session,
    task_id: int,
    owner_id: int
):
    return (
        db.query(Task)
        .join(Project, Task.project_id == Project.id)
        .filter(
            Task.id == task_id,
            Project.owner_id == owner_id
        )
        .first()
    )


# Обновление задачи
def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate
):
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


# Удаление задачи
def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()

    return True