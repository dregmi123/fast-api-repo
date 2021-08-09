from fastapi import FastAPI
from .router import staff

app = FastAPI()

app.include_router(staff.router)
