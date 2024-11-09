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