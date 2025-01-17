from abc import ABC, abstractmethod


class BaseKafkaService(ABC):
    """ Класс Kafka сервиса. Реализует отправку и получение сообщений в Kafka """

    @abstractmethod
    async def create_message(self, message: str):
        pass

    @abstractmethod
    async def get_messages(self, count=1):
        pass

    @abstractmethod
    async def startup(self):
        pass

    @abstractmethod
    async def shutdown(self):
        pass
