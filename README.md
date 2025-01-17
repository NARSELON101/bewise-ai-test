<h1>Сервис сохранения заметок</h1>

<h2>Разделен на 4 модуля</h2>
- <h3>*Модуль App*</h3>
  - Содержит класс ApplicationService, который является API для работы с БД. 
  - Так же содержит router запросов FastAPI
- <h3>*Модуль Kafka*</h3>
  - Содержит настройки для KafkaService.
  - API для работы с Kafka
- <h3>*Модуль PostgreSQL*</h3>
  - Содержит настройки для БД. 
  - Основные функции для работы с БД через sqlalchemy
- <h3>*Модуль Tests*</h3>
  - Тесты для приложения 
  - Моковые ApplicationService и KafkaService

Файл main.py содержит само приложение, и его настройки 

Файл run.py запускает приложение из main.py с помощью uvicorn


<h2>Запуск через docker-compose.yml файл</h2>
- Создать и настроить .env файл в главной директории проекта (за основу можно взять .env.example)
- Запустить через командную строку docker-compose.yml файл

<h2>Для запуска standalone приложения с внешними БД и Kafka</h2>
- Поменять settings.py в модуле Kafka и PostgreSQL, указав актуальные ссылки на БД и Kafka
- Установить requirements.txt
- Запустить через run.py
