from fastapi import FastAPI
from .router import staff
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="sms/media"), name="media")   

app.include_router(staff.router)
