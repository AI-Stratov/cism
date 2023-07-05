import asyncio
import subprocess

from fastapi import FastAPI
from logger_config import logger
from src.auth.routers import router as auth_router
from src.tasks.consumer import consume_tasks
from src.tasks.processing import periodic_task_deletion
from src.tasks.routers import router as task_router


app = FastAPI()
app.include_router(auth_router, prefix='/auth')
app.include_router(task_router, prefix='/tasks')


@app.on_event("startup")
async def startup_event():
    subprocess.run(["alembic", "upgrade", "head"])
    logger.info('Initializing API ...')
    asyncio.create_task(periodic_task_deletion())
    asyncio.create_task(consume_tasks())
