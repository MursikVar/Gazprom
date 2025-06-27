from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import date
from typing import Optional, Annotated, List


class UserCreate(BaseModel):
    email: EmailStr
    telephone: str
    password: str
    username: str
    is_superuser: bool
    department: str
    position: str
    birth_date: date
    skills: str
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    birth_date: Optional[date] = None  # Используем Pydantic date
    skills: Optional[str] = None
    interests: Optional[List[str]] = None

class UserUpdateInternal(UserUpdate):
    profile_image_url: Optional[str] = None
    is_superuser: Optional[bool] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserPasswordReset(BaseModel):
    email: str
    code: str
    new_password: str
    confirm_new_password: str
class UserResponse(BaseModel):
    id: int
    username: str
    telephone: str
    email: EmailStr
    is_superuser: bool
    department: Optional[str]
    position: Optional[str]
    birth_date: Optional[date]
    skills: Optional[str] = None
    profile_image_url: Optional[str]
    interests: List[str] = []  # Список интересов пользователя

    model_config = ConfigDict(from_attributes=True)

class AvatarResponse(BaseModel):
    profile_image_url: str
