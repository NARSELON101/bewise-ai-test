from fastapi import APIRouter, Response, Depends, Query
from sqlalchemy.orm import Session
from src.app.applications_repository import ApplicationRepository
from src.app.models import Application
from src.postgresql.database import get_postgres_db

router = APIRouter()


def get_application_service(db: Session = Depends(get_postgres_db)):
    return ApplicationRepository(db=db)


@router.get('/applications')
def get_applications(user_name: str = '',
                     app_repository: ApplicationRepository = Depends(get_application_service),
                     page: int = Query(default=1, gt=0), size: int = Query(default=10, gt=0)):
    return app_repository.get_list(page=page, size=size, filters={"user_name": user_name} if user_name else None)


@router.post('/applications')
def add_application(name: str, description: str,
                    app_repository: ApplicationRepository = Depends(get_application_service)):
    app_repository.add(Application(user_name=name, description=description))

    return Response(status_code=201)
