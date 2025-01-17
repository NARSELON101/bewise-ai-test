from src.kafka.base import BaseKafkaService

from queue import Queue, Empty


class MockKafkaService(BaseKafkaService):
    """ Класс Kafka сервиса. Реализует отправку и получение сообщений в Kafka """

    def __init__(self):
        self.queue = Queue()

    async def create_message(self, message: str):
        self.queue.put(message)

    async def get_messages(self, count=1):
        messages_list = []
        for i in range(1, count + 1):
            try:
                messages_list.append(self.queue.get(timeout=1))
            except Empty:
                break
        return messages_list if count > 1 else messages_list[0]

    async def startup(self):
        pass

    async def shutdown(self):
        pass
