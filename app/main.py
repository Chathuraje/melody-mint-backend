from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.utils.response import StandardResponse
from app.api.main import router as api_v1_routers
from app.utils import startup

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

# Include your routers
app.include_router(api_v1_routers)   

@app.on_event("startup")
async def startup_event():
    await startup.startup_event()
    
    

@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(code=exc.status_code, response=str(exc.detail)).dict(),
    )
