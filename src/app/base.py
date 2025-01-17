from abc import ABC, abstractmethod


class BaseApplicationService(ABC):
    @abstractmethod
    async def add(self, application):
        """ Добавление объекта заявки в сессию """
        pass

    @abstractmethod
    async def commit(self):
        """ Подтверждение выполнения сессии """
        pass

    @abstractmethod
    async def rollback(self):
        """ Отмена выполнения сессии """
        pass

    @abstractmethod
    async def get_list(self, page, size, filters: dict = None):
        """ Получения списка заявок из БД """
        pass

    @abstractmethod
    async def get(self, application_id):
        pass

    @abstractmethod
    async def delete(self, application_id):
        pass

    @abstractmethod
    async def update(self, application_id, new_application):
        pass
