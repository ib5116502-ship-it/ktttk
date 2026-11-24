from app.worker.celery_app import celery_app


@celery_app.task
def send_task_notification(task_title: str, user_email: str):
    message = (
        f"Новая задача создана: {task_title}. "
        f"Уведомление предназначено для {user_email}."
    )

    print(message)

    return {
        "status": "success",
        "message": message
    }