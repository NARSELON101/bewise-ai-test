from sqlalchemy.orm import Query


def paginate(query: Query, size: int = 10, page: int = 1):
    if page == 1:
        return query.limit(size)
    return query.offset((page * size) - size).limit(size)
