from fastapi import FastAPI
from src.app.urls import router as applications, kafka_service
from src.postgresql.database import init_models

app = FastAPI(title='Сервис заявок', version='1.0.0')


@app.on_event("startup")
async def init_db():
    await init_models()
    await kafka_service.startup()

app.include_router(applications, prefix="/v1")

