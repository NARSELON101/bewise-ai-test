from sqlalchemy.orm import Session

from src.app.dto import ApplicationDTO
from src.app.models import Application
from src.app.utils import paginate


class ApplicationRepository:
    def __init__(self, db: Session):
        self._db = db

    def add(self, application):
        self._db.add(application)
        self._db.commit()
        return application.id

    def delete(self, application: ApplicationDTO):
        pass

    def update(self, application: ApplicationDTO):
        pass

    def get_list(self, page, size, filters: dict = None):
        applications = self._db.query(Application)
        if filters:
            applications = applications.filter_by(**filters)
        return [ApplicationDTO.from_orm(app) for app in paginate(applications, page=page, size=size)]

    def get(self, application_id):
        pass
