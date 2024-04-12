from venv import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils import startup
from app.config.settings import get_settings
from app.api import api_router

env = get_settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=env.APP_ORGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():

    await startup.startup_event()
