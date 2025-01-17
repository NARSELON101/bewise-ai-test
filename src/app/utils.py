import os
import time

from sqlalchemy import Executable
import logging

logger = logging.getLogger('uvicorn')
logger.setLevel(logging.INFO)


def paginate(query: Executable, size: int = 10, page: int = 1):
    """ Функция добавляет к выражению параметры OFFSET и LIMIT """
    if page == 1:
        return query.limit(size)
    return query.offset((page * size) - size).limit(size)


def log_method(func, cls):
    """ Декоратор логирования метода """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f'Call method {func.__name__} of service {cls.__name__}, args: {args[1:]}, kwargs: {kwargs}')
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.warning(
                f'{str(e)} method: {func.__name__} '
                f'of service {cls.__name__}, args: {args[1:]}, kwargs: {kwargs}')
            raise e
        logger.debug(f'{func.__name__}: Executed time: {time.time() - start_time}')
        return result

    return wrapper


def class_method_logger(cls):
    """ Декоратор, обеспечивающий логирование запуска
    и ошибок во время выполнения методов класса """
    for method in dir(cls):
        if not method.startswith("__") and callable(getattr(cls, method)):
            setattr(cls, method, log_method(getattr(cls, method), cls))

    return cls
