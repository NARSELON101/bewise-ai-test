from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.dto import ApplicationDTO
from src.app.models import Application
from src.app.utils import paginate


class ApplicationRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def add(self, application):
        self._db.add(application)
        return application.id

    async def commit(self):
        await self._db.commit()

    async def rollback(self):
        await self._db.rollback()

    async def delete(self, application: ApplicationDTO):
        pass

    async def update(self, application: ApplicationDTO):
        pass

    async def get_list(self, page, size, filters: dict = None):
        statement = select(Application)

        if filters:
            statement = statement.filter_by(**filters)

        statement = paginate(statement, page=page, size=size)

        applications = await self._db.execute(statement)
        return [ApplicationDTO.from_orm(app) for app in applications.scalars()]

    async def get(self, application_id):
        pass
