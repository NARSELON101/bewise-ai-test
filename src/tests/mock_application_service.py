import datetime
import uuid

from src.app.base import BaseApplicationService

from src.app.dto import ApplicationDTO


class MockApplicationService(BaseApplicationService):
    """ Класс сервиса заявок. Реализует работу с БД заявок """

    def __init__(self):
        self._db = []
        self._db_session = []

    async def add(self, application):
        """ Добавление объекта заявки в сессию """
        application.id = uuid.uuid4()
        application.created_at = datetime.datetime.now()
        self._db_session.append(application)

    async def commit(self):
        """ Подтверждение выполнения сессии """
        self._db += self._db_session
        self._db_session = []

    async def rollback(self):
        """ Отмена выполнения сессии """
        self._db_session = []

    async def get_list(self, page, size, filters: dict = None):
        """ Получения списка заявок из БД """
        data = self._db
        if filters:
            data = list(filter(lambda x: filters.get('user_name') == x.user_name, self._db))
        data = data[(page * size) - size:][:size]
        return [ApplicationDTO.model_validate(app) for app in data]

    async def get(self, application_id):
        for application in self._db:
            if str(application.id) == application_id:
                return application

    async def delete(self, application_id):
        pass

    async def update(self, application_id, new_application):
        pass
