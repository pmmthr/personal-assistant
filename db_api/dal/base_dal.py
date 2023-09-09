import traceback
from typing import Optional, Union, List, Dict

from sqlalchemy import Column, update, delete, dialects
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.strategy_options import selectinload

from db_api.postgresql import Database


class BaseDAL:

    @classmethod
    def _get_model(cls) -> DeclarativeMeta:
        return getattr(cls, '_model')

    @classmethod
    async def add(cls,  **kwargs) -> Optional[int]:
        try:
            db = Database.get_instance()

            async with db.session() as session:
                async with session.begin():
                    model = cls._get_model()
                    query = insert(model).values(**kwargs)
                    await session.execute(query)
        except:
            traceback.print_exc()

    @classmethod
    async def get(
            cls,
            id: Optional[int] = None,
            many: bool = False,
            relationship: Optional[Column] = None,
            orderby=None,
            distinct: bool = False,
            *args,
            **kwargs
    ) -> Union[List[any], Optional[any]]:
        db = Database.get_instance()
        model = cls._get_model()

        async with db.session() as session:
            async with session.begin():

                filters = []

                if id is not None:
                    filters.append(getattr(model, 'id') == id)
                else:
                    for key, value in kwargs.items():
                        filters.append(getattr(model, key) == value)

                if orderby:
                    query = select(model).where(*filters).order_by(orderby)
                else:
                    query = select(model).where(*filters)

                if distinct:
                    query = query.distinct(distinct)

                results = await session.execute(query)

                if many:
                    result = results.scalars().all()
                else:
                    result = results.fetchone()
                    if result:
                        (result,) = result

        return result

    @classmethod
    async def update(cls, id: Optional[int] = None, where: Optional[Dict] = None, **kwargs) -> None:
        db = Database.get_instance()
        model = cls._get_model()

        async with db.session() as session:
            async with session.begin():
                filters = []

                if id is not None:
                    filters.append(getattr(model, 'id') == id)
                elif where is not None:
                    for key, value in where.items():
                        filters.append(getattr(model, key) == value)

                query = update(model).where(*filters).values(**kwargs)

                await session.execute(query)

    @classmethod
    async def delete(cls, id: Optional[int] = None, *args, **kwargs) -> None:
        db = Database.get_instance()
        model = cls._get_model()

        async with db.session() as session:
            async with session.begin():
                filters = []

                if id is not None:
                    filters.append(getattr(model, 'id') == id)
                else:
                    for key, value in kwargs.items():
                        filters.append(getattr(model, key) == value)

                query = delete(model).where(*filters)
                await session.execute(query)

    @classmethod
    async def insert_or_update(cls, set_: dict, index_elements: List[str], *rows, **kwargs):
        db = Database.get_instance()

        async with db.session() as session:
            async with session.begin():
                model = cls._get_model()
                query = dialects.postgresql.insert(model).values(**kwargs).on_conflict_do_update(
                    set_=set_,
                    index_elements=index_elements
                )
                await session.execute(query)


    @classmethod
    async def adds(cls, *rows, **kwargs) -> Optional[int]:
        db = Database.get_instance()

        result = None

        async with db.session() as session:
            if len(rows) > 0:
                session.add_all(rows)
                await session.commit()
            else:
                query = insert(cls._model).values(**kwargs)

                results = await session.execute(query)
                await session.commit()

        return result

