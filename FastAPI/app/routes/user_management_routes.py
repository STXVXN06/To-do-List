"""
Module that defines routes for managing users.

This module uses FastAPI to define the routes that allow
creating, reading, updating, and deleting users through a REST API.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from models.user import UserRead, UserCreate, UserUpdate
from services.user_service import UserService
from utils.dependencies import get_current_admin
from services.auth_service import AuthService

router = APIRouter(
    prefix="/admin/users",
    tags=["admin users"],
)

# Helper function to verify admin permissions
def verify_admin(current_admin: UserRead):  # Cambiar tipo a UserRead
    """Verifies if the user is an administrator."""
    if current_admin.role.name != "Administrator":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@router.get("/", response_model=List[UserRead])
def list_users() -> List[UserRead]:
    """List all registered users."""
    return UserService.list_all_users()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    current_admin: UserRead = Depends(get_current_admin)  # Cambiar tipo a UserRead
) -> UserRead:
    # """Create a new user (for administrators only)."""
    # verify_admin(current_admin)

    try:
        created_user = UserService.create_user(
            email=user.email, password=user.password, role_id=user.role_id
        )
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating user") from e

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    current_admin: UserRead = Depends(get_current_admin)  # Cambiar tipo a UserRead
) -> UserRead:
    """Get user information by their ID (for administrators only)."""
    verify_admin(current_admin)

    user = UserService.get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_admin: UserRead = Depends(get_current_admin)
) -> UserRead:
    """Update existing user information (for administrators only)."""
    verify_admin(current_admin)

    try:
        # Si se proporciona una nueva contraseña, la encriptamos
        hashed_password = None
        if user_update.password:
            hashed_password = AuthService.get_password_hash(user_update.password)

        updated_user = UserService.update_user(
            user_id=user_id,
            email=user_update.email,
            password=hashed_password,  # Pasamos la contraseña encriptada
            role_id=user_update.role_id
        )
        
        if updated_user:
            return updated_user
        raise HTTPException(status_code=404, detail="User not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_admin: UserRead = Depends(get_current_admin)  # Cambiar tipo a UserRead
):
    """Deletes a user by their ID (admin only)."""
    verify_admin(current_admin)

    success = UserService.delete_user(user_id)
    if success:
        return
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/{user_id}/active")
def toggle_user_active(
    user_id: int,
    current_admin: UserRead = Depends(get_current_admin)  # Cambiar tipo a UserRead
):
    """Activate or deactivate a user (for administrators only)."""
    verify_admin(current_admin)

    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = not user.is_active
    # Ya que UserRead es de solo lectura, necesitas actualizar el modelo ORM directamente
    UserService.update_user_status(user_id, user.is_active)
    return {"message": f"User {user_id} is now {'active' if user.is_active else 'inactive'}"}