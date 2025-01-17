import json
import uuid
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from fastapi import FastAPI
from src.app.urls import router as applications
from src.tests.mock_application_service import MockApplicationService
from src.tests.mock_kafka_service import MockKafkaService

app = FastAPI(title='Сервис заявок', version='1.0.0')

app.app_repository = MockApplicationService()
app.kafka_service = MockKafkaService()

app.include_router(applications, prefix="/v1")

client = TestClient(app)


@pytest.mark.asyncio
@patch.object(uuid, 'uuid4', side_effect=[uuid.UUID('44ae7dc5-b01f-432b-a07a-c433d315d1f4'),
                                          uuid.UUID('3bfe0568-ccd2-4c9f-8069-491f8d60ab3d')])
async def test_get_items(*args):
    """ Тест на добавление и получение заметок без фильтрации"""
    client.post('/v1/applications', params={"name": 'test', "description": 'test'})
    client.post('/v1/applications', params={"name": 'test2', "description": 'test2'})

    res = await app.app_repository.get_list(page=1, size=10)
    res = list(map(lambda x: json.loads(x.model_dump_json()), res))

    response = client.get('/v1/applications', params={"page": '1', "size": '10'})

    assert res == json.loads(response.content.decode('utf-8'))


@pytest.mark.asyncio
@patch.object(uuid, 'uuid4', side_effect=[uuid.UUID('44ae7dc5-b01f-432b-a07a-c433d315d1f4'),
                                          uuid.UUID('3bfe0568-ccd2-4c9f-8069-491f8d60ab3d'),
                                          uuid.UUID('5bfe0568-ccd2-4c9f-8069-491f8d60ab3d')])
async def test_kafka_messages(*args):
    """ Тест на получение сообщений из очереди """
    client.post('/v1/applications', params={"name": 'test', "description": 'test'})
    client.post('/v1/applications', params={"name": 'test2', "description": 'test2'})
    messages = await app.kafka_service.get_messages(2)
    assert len(messages) == 2

    client.post('/v1/applications', params={"name": 'test', "description": 'test'})
    await app.kafka_service.get_messages(1)


@pytest.mark.asyncio
async def test_get_items_with_filter(*args):
    """ Тест на добавление и получение заметок с фильтром """
    client.post('/v1/applications', params={"name": 'test', "description": 'test'})
    client.post('/v1/applications', params={"name": 'test2', "description": 'test2'})

    res = await app.app_repository.get_list(page=1, size=10, filters={"user_name": 'test2'})
    res = list(map(lambda x: json.loads(x.model_dump_json()), res))

    response = client.get('/v1/applications', params={"page": '1', "size": '10', 'user_name': 'test2'})

    assert res == json.loads(response.content.decode('utf-8'))
