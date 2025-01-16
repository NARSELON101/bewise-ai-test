from sqlalchemy import Executable


def paginate(query: Executable, size: int = 10, page: int = 1):
    if page == 1:
        return query.limit(size)
    return query.offset((page * size) - size).limit(size)
