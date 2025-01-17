from fastapi import FastAPI
from src.app.urls import router as applications
from src.app.application_service import ApplicationService
from src.kafka.kafka_service import KafkaService
from src.postgresql.database import init_models, get_postgres_db

app = FastAPI(title='Сервис заявок', version='1.0.0')


@app.on_event("startup")
async def init_db():
    await init_models()
    app.app_repository = ApplicationService(db=await anext(get_postgres_db()))
    app.kafka_service = KafkaService()
    await app.kafka_service.startup()

app.include_router(applications, prefix="/v1")

