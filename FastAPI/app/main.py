# pylint: disable=import-error, no-member,unused-argument
"""
Main module for the FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from routes import auth_router, task_router, user_management_router
from config.database import database as connection

@asynccontextmanager
async def lifespan(api: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    This function ensures that the database connection is properly managed
    during the lifespan of the FastAPI application. It connects to the database
    if the connection is closed at the start and ensures the connection is closed
    when the application shuts down.
    Args:
        api (FastAPI): The FastAPI application instance.
    Yields:
        None
    """

    if connection.is_closed():
        connection.connect()
    try:
        yield
    finally:
        if not connection.is_closed():
            connection.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def docs_redirect():
    """Redirige a la documentación de la API."""
    return RedirectResponse(url="/docs")

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(user_management_router)
