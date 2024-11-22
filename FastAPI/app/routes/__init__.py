"""
init.py
"""
from .auth_routes import router as auth_router
from .task_routes import router as task_router
from .user_management_routes import router as user_management_router

__all__ = ["auth_router", "task_router", "user_management_router"]
