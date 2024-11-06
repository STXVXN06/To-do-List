from typing import Optional
from pydantic import BaseModel, EmailStr
from .role import Role

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role_id: int
    is_active: bool
    role: Role

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str  # Contraseña en texto plano; se hashea antes de almacenar
    role_id: int

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None