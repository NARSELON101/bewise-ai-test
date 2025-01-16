from confluent_kafka import KafkaException
from fastapi import APIRouter, Response, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.applications_repository import ApplicationRepository
from src.app.models import Application
from src.kafka.kafka_producer import KafkaService
from src.postgresql.database import get_postgres_db

router = APIRouter()
kafka_service = KafkaService()


def get_application_repository(db: AsyncSession = Depends(get_postgres_db)):
    return ApplicationRepository(db=db)


@router.get('/applications')
async def get_applications(user_name: str = '',
                           app_repository: ApplicationRepository = Depends(get_application_repository),
                           page: int = Query(default=1, gt=0), size: int = Query(default=10, gt=0)):
    return await app_repository.get_list(page=page, size=size, filters={"user_name": user_name} if user_name else None)


@router.post('/applications')
async def add_application(name: str, description: str,
                          app_repository: ApplicationRepository = Depends(get_application_repository)):
    new_record = Application(user_name=name, description=description)
    await app_repository.add(new_record)

    try:
        await kafka_service.create_message(str(new_record))
    except KafkaException as e:
        await app_repository.rollback()
        return Response(status_code=503, content=str(e))

    await app_repository.commit()

    return Response(status_code=201, content=b'Created')
