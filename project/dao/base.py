from typing import Generic, List, Optional, TypeVar

from flask import current_app, request
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from project.setup.db.models import Base
from project.models import Movie


T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)

        page = int(request.args.get('page', 0))
        status = request.args.get('status')

        if status == 'new':
            stmt = stmt.order_by(Movie.year.desc())
        return stmt.paginate(page=page, per_page=self._items_per_page, error_out=False).items
