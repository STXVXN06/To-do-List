"""
Module defining routes for managing tasks.

This module uses FastAPI to define routes that allow
creating, reading, updating, and deleting tasks through a REST API.
"""
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from models.user import UserRead
from models.task import Task, TaskUpdate, TaskCreate
from models.change import Change
from services.task_service import TaskService
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)
@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: UserRead = Depends(get_current_user)
) -> Task:
    task_model = TaskService.create_task(
        title=task_data.title,
        description=task_data.description,
        expiration_date=task_data.expiration_date,
        status_id=task_data.status_id,
        user_id=current_user.id
    )
    # Convierte el modelo ORM a un modelo Pydantic
    return Task.from_orm(task_model)



@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user)
) -> Task:
    """
    Get a task by its ID.
    """
    is_admin = current_user.role.name == "Administrator"
    task = TaskService.get_task_by_id(task_id, user_id=current_user.id, is_admin=is_admin)
    if task:
        return Task.from_orm(task)  # Convierte de ORM a modelo Pydantic
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserRead = Depends(get_current_user)  # Cambiado de User a UserRead
) -> Task:
    """Update an existing task."""
    is_admin = current_user.role.name == "Administrator"
    task = TaskService.update_task(
        task_id=task_id,
        user_id=current_user.id,
        is_admin=is_admin,
        **task_update.model_dump(exclude_unset=True)
    )
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: UserRead = Depends(get_current_user)  # Cambiado de User a UserRead
):
    """
    Delete a task by its ID.
    """
    is_admin = current_user.role.name == "Administrator"
    success = TaskService.delete_task(
        task_id=task_id,
        user_id=current_user.id,
        is_admin=is_admin
    )
    if success:
        return
    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/", response_model=List[Task])
def list_tasks(
    task_status: Optional[str] = None,
    expiration_date: Optional[date] = None,
    current_user: UserRead = Depends(get_current_user)  # Cambiado de User a UserRead
) -> List[Task]:
    """
    List all tasks for the user with filtering options.
    """
    is_admin = current_user.role.name == "Administrator"
    tasks = TaskService.list_tasks(
        user_id=current_user.id,
        status=task_status,
        expiration_date=expiration_date,
        is_admin=is_admin
    )
    return tasks

@router.patch("/{task_id}/favorite", response_model=Task)
def toggle_favorite(
    task_id: int,
    current_user: UserRead = Depends(get_current_user)  # Cambiado de User a UserRead
) -> Task:
    """
    Toggle the favorite status of a task.
    """
    is_admin = current_user.role.name == "Administrator"
    task = TaskService.toggle_favorite(
        task_id=task_id,
        user_id=current_user.id,
        is_admin=is_admin
    )
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/{task_id}/changes", response_model=List[Change])
def get_task_changes(
    task_id: int,
    current_user: UserRead = Depends(get_current_user)  # Cambiado de User a UserRead
) -> List[Change]:
    """
    Get the change history of a specific task.
    """
    is_admin = current_user.role.name == "Administrator"
    task = TaskService.get_task_by_id(task_id, user_id=current_user.id, is_admin=is_admin)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    changes = TaskService.get_changes_by_task_id(task_id)
    return [Change.from_orm(change) for change in changes]