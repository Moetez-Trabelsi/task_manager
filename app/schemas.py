from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name : str

class UserResponse(BaseModel):
    id: int
    email: str
    name : str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Task schemas

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int
    is_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None