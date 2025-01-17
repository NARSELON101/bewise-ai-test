from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dto import ApplicationDTO
from src.app.models import Application
from src.app.utils import paginate, class_method_logger
from src.app.base import BaseApplicationService


@class_method_logger
class ApplicationService(BaseApplicationService):
    """ Класс сервиса заявок. Реализует работу с БД заявок """

    def __init__(self, db: AsyncSession):
        self._db = db

    async def add(self, application: Application):
        """ Добавление объекта заявки в сессию """
        self._db.add(application)

    async def commit(self):
        """ Подтверждение выполнения сессии """
        await self._db.commit()

    async def rollback(self):
        """ Отмена выполнения сессии """
        await self._db.rollback()

    async def get_list(self, page, size, filters: dict = None):
        """ Получения списка заявок из БД """
        statement = select(Application)

        # Если есть фильтры, то добавляем к выражению filter_by
        if filters:
            statement = statement.filter_by(**filters)

        # Добавляем к выражению пагинацию
        statement = paginate(statement, page=page, size=size)

        # Выполняем выражение, и возвращаем результаты в виде списка DTO объектов
        applications = await self._db.execute(statement)
        return [ApplicationDTO.from_orm(app) for app in applications.scalars()]

    async def get(self, application_id):
        pass

    async def delete(self, application_id: Application):
        pass

    async def update(self, application_id, new_application):
        pass
