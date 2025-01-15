from fastapi import FastAPI
from src.app.urls import router as applications


app = FastAPI(title='Сервис заявок', version='1.0.0')

app.include_router(applications, prefix="/v1")

