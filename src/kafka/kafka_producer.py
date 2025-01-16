from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from confluent_kafka import KafkaException
from aiokafka.errors import KafkaConnectionError

from src.kafka.settings import KAFKA_TOPIC, KAFKA_PORT, KAFKA_HOSTNAME

KAFKA_URL = f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"


class KafkaService:
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
        if self.p:
            try:
                await self.p.send_and_wait(KAFKA_TOPIC, bytearray(message, encoding='utf-8'))
            except Exception as e:
                print(e)
                raise KafkaException("Ошибка при отправке сообщения")

    async def get_messages(self, count=1):
        if self.c:
            msg_count = 0
            async for msg in self.c:
                msg_count += 1
                print(
                    f'Получено сообщение: {msg.value.decode()} '
                    f'из {msg.topic} [{msg.partition}]')
                if msg_count >= count:
                    break

    async def startup(self):
        await self.c.start()
        await self.p.start()

    async def shutdown(self):
        await self.c.stop()
        await self.p.stop()
