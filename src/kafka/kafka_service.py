from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from confluent_kafka import KafkaException
from aiokafka.errors import KafkaConnectionError
from src.app.utils import class_method_logger, logger
from src.kafka.base import BaseKafkaService
from src.kafka.settings import KAFKA_TOPIC, KAFKA_PORT, KAFKA_HOSTNAME

KAFKA_URL = f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"


@class_method_logger
class KafkaService(BaseKafkaService):
    """ Класс Kafka сервиса. Реализует отправку и получение сообщений в Kafka """

    def __init__(self):
        self.topic = 'applications-topic'
        try:
            self.p = AIOKafkaProducer(bootstrap_servers=KAFKA_URL)
            self.c = AIOKafkaConsumer(self.topic,
                                      bootstrap_servers=KAFKA_URL,
                                      auto_offset_reset='earliest')
        except KafkaConnectionError:
            self.c = None
            self.p = None

    async def create_message(self, message: str):
        """ Отправка сообщения в Kafka """
        if self.p:
            try:
                await self.p.send_and_wait(KAFKA_TOPIC, bytearray(message, encoding='utf-8'))
            except Exception as e:
                raise KafkaException("Ошибка при отправке сообщения")

    async def get_messages(self, count=1):
        """ Получение сообщений из Kafka. Можно указать кол-во получаемых сообщений """
        if self.c:
            msg_count = 0
            async for msg in self.c:
                msg_count += 1
                logger.info(
                    f'Получено сообщение: {msg.value.decode()} '
                    f'из {msg.topic} [{msg.partition}]')
                if msg_count >= count:
                    break

    async def startup(self):
        """ Метод запуска работы Producer и Consumer """
        await self.c.start()
        await self.p.start()

    async def shutdown(self):
        """ Метод завершения работы Producer и Consumer """
        await self.c.stop()
        await self.p.stop()
