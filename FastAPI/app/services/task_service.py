"""
Module defining services for managing tasks.
"""

from datetime import date, datetime
from typing import List, Optional
from models.task import Task
from models.change import Change
from config.database import TaskModel, ChangeModel

class TaskService:
    """
    Module defining the services.
    """

    @staticmethod
    def create_task(
        title: str,
        description: Optional[str],
        expiration_date: Optional[date],
        status_id: int,
        user_id: int,
    ) -> TaskModel:  # Devuelve el modelo de la base de datos
        """Creates a new task."""
        task = TaskModel.create(  # Asegúrate de usar el modelo ORM aquí
            title=title,
            description=description,
            expiration_date=expiration_date,
            status_id=status_id,
            user_id=user_id,
        )
        return task

    @staticmethod
    def get_task_by_id(task_id: int, user_id: int, is_admin: bool) -> Optional[TaskModel]:
        """Retrieves a task by ID, checking user permissions."""
        task = TaskModel.get_or_none(TaskModel.id == task_id)  # Usa el modelo ORM aquí
        if task and (task.user_id == user_id or is_admin):
            return task
        return None
    
    @staticmethod
    def update_task(
        task_id: int, user_id: int, is_admin: bool, **updates
    ) -> Optional[Task]:
        """Updates a task, logging changes, and checking user permissions."""
        task = TaskModel.get_or_none(TaskModel.id == task_id)
        if task and (task.user_id == user_id or is_admin):
            for key, value in updates.items():
                setattr(task, key, value)
            task.save()

            # Log changes to the change history
            for field, new_value in updates.items():
                ChangeModel.create(
                    task=task,
                    field_changed=field,
                    old_value=getattr(task, field, None),
                    new_value=new_value,
                )
            return task
        return None

    @staticmethod
    def delete_task(task_id: int, user_id: int, is_admin: bool) -> bool:
        """Deletes a task, checking user permissions."""
        task = TaskModel.get_or_none(TaskModel.id == task_id)
        if task and (task.user_id == user_id or is_admin):
            task.delete_instance()
            return True
        return False

    @staticmethod
    def list_tasks(
        user_id: int,
        status: Optional[str],
        expiration_date: Optional[date],
        is_admin: bool,
    ) -> List[Task]:
        """Lists tasks, applying filters and checking user permissions."""
        query = TaskModel.select().where((TaskModel.user_id == user_id) | (is_admin))
        if status:
            query = query.where(TaskModel.status_id == status)
        if expiration_date:
            query = query.where(TaskModel.expiration_date <= expiration_date)
        return list(query)

    @staticmethod
    def toggle_favorite(task_id: int, user_id: int, is_admin: bool) -> Optional[Task]:
        """Toggles the favorite status of a task, checking user permissions."""
        task = Task.get_or_none(Task.id == task_id)
        if task and (task.user_id == user_id or is_admin):
            task.is_favorite = not task.is_favorite
            task.save()
            return task
        return None

    @staticmethod
    def get_changes_by_task_id(task_id: int) -> List[Change]:
        """Retrieves changes for a specific task."""
        return list(
            Change.select()
            .where(Change.task == task_id)
            .order_by(Change.timestamp.desc())
        )
