from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.projects.router import router as projects_router
from app.tasks.router import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="TaskFlow API",
    description="Система управления проектами и задачами",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


app.include_router(auth_router)


app.include_router(users_router)

app.include_router(projects_router)

app.include_router(tasks_router)


@app.get("/", tags=["Главная"])
def home():
    return {
        "message": "Добро пожаловать в TaskFlow API"
    }


@app.get("/health", tags=["Проверка"])
def health():
    return {
        "status": "healthy"
    }