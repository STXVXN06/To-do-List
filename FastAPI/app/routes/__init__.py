"""
init.py
"""
from .user_routes import router as user_router # pylint: disable=import-error
from .task_routes import router as task_router
from .user_management_routes import router as user_management_router

__all__ = ["user_router", "task_router", "user_management_router"]
