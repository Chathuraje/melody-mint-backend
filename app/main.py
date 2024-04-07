from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import router as api_v1_routers
from app.utils import startup

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_routers)


@app.on_event("startup")
async def startup_event():
    await startup.startup_event()
