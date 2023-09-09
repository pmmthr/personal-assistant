import ssl
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session


from data import config
from .base import Base



class Database:

    _instance: Optional[any] = None
    _database_url: Optional[str] = None
    _sync_database_url: Optional[str] = None

    def __init__(self):
        self._engine = create_async_engine(Database._database_url)
        self._sync_engine = create_engine(Database._sync_database_url)
        self._session: sessionmaker = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)
        self._sync_session = scoped_session(sessionmaker(bind=self._sync_engine, expire_on_commit=True))

    @classmethod
    def bind(cls, database_url: str):
        database_url = database_url.split('://')[1]
        cls._database_url: str = 'postgresql+asyncpg://' + database_url
        cls._sync_database_url: str = 'postgresql://' + database_url

    @classmethod
    def get_instance(cls) -> any:
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    async def close(self):
        await self._engine.dispose()

    async def create_all(self):
        async with self._session() as session:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self, cascade: bool = False):
        async with self._session() as session:
            if cascade:
                async with session.begin():
                    tables = Base.metadata.tables.keys()
                    for table in tables:
                        await session.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
            else:
                async with self._engine.begin() as conn:
                    await conn.run_sync(Base.metadata.drop_all)

    @property
    def session(self):
        return self._session

    @property
    def sync_session(self):
        return self._sync_session

    @property
    def engine(self):
        return self._engine

Database.bind(config.DATABASE_URL)
db = Database.get_instance()
