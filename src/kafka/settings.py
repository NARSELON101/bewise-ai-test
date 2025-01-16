import os

KAFKA_HOSTNAME = os.getenv('KAFKA_HOSTNAME', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '29092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'applications-topic')
