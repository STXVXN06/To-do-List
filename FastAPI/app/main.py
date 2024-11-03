"""
Main module for the FastAPI application.
"""

from contextlib import asynccontextmanager
from starlette.responses import RedirectResponse
from routes import task_router, user_management_router, auth_routes

# Routers

from config.database import database as connection
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(api: FastAPI):  # pylint: disable=unused-argument
    """
    Manage the lifespan of the FastAPI application.

    Connects to the database at startup and closes the connection at shutdown.
    """

    # Connect to the database if the connection is closed
    if connection.is_closed():
        connection.connect()
    try:
        yield  # Application code runs here
    finally:
        #  close connection when the aplication is stop
        if not connection.is_closed:
            connection.close()


app = FastAPI(lifespan=lifespan)

# On Startup
# On Shutdown


# Documentation
@app.get("/")
async def docs():
    """
    Redirect to the documentation.
    """
    return RedirectResponse(url="/docs")


# Include routers for events and tickets
app.include_router(auth_routes.router)
app.include_router(task_router)
app.include_router(user_management_router)
