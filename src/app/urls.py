from confluent_kafka import KafkaException
from fastapi import APIRouter, Response, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.application_service import ApplicationService
from src.app.models import Application

from src.postgresql.database import get_postgres_db

router = APIRouter()


def get_application_service(db: AsyncSession = Depends(get_postgres_db)):
    return ApplicationService(db=db)


@router.get('/applications')
async def get_applications(request: Request,
                           user_name: str = '',
                           page: int = Query(default=1, gt=0), size: int = Query(default=10, gt=0)):
    """ Возвращает список заметок на текущей странице, с возможностью фильтрации по имени пользователя

        Параметры:
        - **user_name**: Имя пользователя, по которому будет происходить фильтрация заметок
        - **page**: Текущая страница
        - **size**: Размер страницы
    """
    return await request.app.app_repository.get_list(page=page, size=size,
                                                     filters={"user_name": user_name} if user_name else None)


@router.post('/applications')
async def add_application(request: Request,
                          name: str, description: str):
    """ Добавляет новую заметку в БД

        Параметры:
        - **name**: Имя пользователя
        - **description**: Описание
    """
    new_record = Application(user_name=name, description=description)
    await request.app.app_repository.add(new_record)
    await request.app.app_repository.commit()

    try:
        await request.app.kafka_service.create_message(str(new_record))
    except KafkaException:
        pass

    return Response(status_code=201, content=b'Created')
