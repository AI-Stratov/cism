import asyncio
import subprocess

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from logger_config import logger
from src.auth.routers import router as auth_router
from src.tasks.consumer import consume_tasks
from src.tasks.processing import periodic_task_deletion
from src.tasks.routers import router as task_router

app = FastAPI()
app.include_router(auth_router, prefix='/auth')
app.include_router(task_router, prefix='/tasks')


@app.get("/", include_in_schema=False)
def root():
    """
    Redirects to the docs page.
    """
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.
    """
    subprocess.run(["alembic", "upgrade", "head"])
    logger.info('Initializing API ...')
    asyncio.create_task(periodic_task_deletion())
    asyncio.create_task(consume_tasks())
