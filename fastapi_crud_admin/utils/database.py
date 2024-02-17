from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


class Database:
    def __init__(self, db_url: str) -> None:
        self.base = declarative_base()
        self._engine: AsyncEngine = create_async_engine(db_url, echo=True, pool_pre_ping=True)
        self.async_session_maker = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)
            await conn.run_sync(self.base.metadata.create_all)

    async def get_db(self) -> AsyncSession:
        async with self.async_session_maker() as session:
            yield session

    @property
    def session(self):
        return self.get_db
