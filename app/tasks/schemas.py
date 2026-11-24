from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = None
    project_id: int
    assigned_to: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    status: str | None = None
    assigned_to: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    project_id: int
    assigned_to: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)