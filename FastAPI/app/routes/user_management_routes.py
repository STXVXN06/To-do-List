"""
Module that defines routes for managing users.

This module uses FastAPI to define the routes that allow
creating, reading, updating, and deleting users through a REST API.
"""

from typing import List

from fastapi import APIRouter, HTTPException, Depends, status

from models.user import UserRead, UserCreate, UserUpdate
from utils.dependencies import get_current_admin
from services.user_service import UserService
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
    current_admin: UserRead = Depends(get_current_admin)  # Changed from User to UserRead
) -> UserRead:
    """
    Create a new user in the system.
    Args:
        user (UserCreate): The user data required to create a new user.
        current_admin (UserRead, optional):
        The current admin user making the request.
        Defaults to the result of get_current_admin.
    Returns:
        UserRead: The created user data.
    Raises:
        HTTPException: If there is a validation error 
        (status code 400) or an unexpected error (status code 500).
    """
    verify_admin(current_admin)

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
    current_admin: UserRead = Depends(get_current_admin)  # Changed from User to UserRead
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
        # Verify that the email is not empty if provided
        if user_update.email is not None and not user_update.email.strip():
            raise ValueError("Email cannot be empty")
        # Verify that the password is not empty if provided
        hashed_password = None
        if user_update.password is not None:
            if not user_update.password.strip():  # Check if `password` contains only spaces
                raise ValueError("Password field cannot be empty")
            hashed_password = AuthService.get_password_hash(user_update.password)
                # Verify that the role_id is not empty, 0, or None
        if user_update.role_id in ('', 0):
            raise ValueError("Role ID cannot be empty or zero")

        # Attempt to update the user if all validations pass
        updated_user = UserService.update_user(
            user_id=user_id,
            email=user_update.email,
            password=hashed_password,  # Pass the hashed password
            role_id=user_update.role_id
        )
        if updated_user:
            return updated_user
        raise HTTPException(status_code=404, detail="User not found")
    except ValueError as e:
        # Capture any validation error and return a 400
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_admin: UserRead = Depends(get_current_admin)  # Changed from User to UserRead
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
    current_admin: UserRead = Depends(get_current_admin)  # Changed from User to UserRead
):
    """Activate or deactivate a user (for administrators only)."""
    verify_admin(current_admin)

    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = not user.is_active
    # Since UserRead is read-only, you need to update the ORM model directly.
    UserService.update_user_status(user_id, user.is_active)
    return {"message": f"User {user_id} is now {'active' if user.is_active else 'inactive'}"}
