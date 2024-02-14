from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, delete, and_, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta


class Repository:
    @staticmethod
    async def find_all(session: AsyncSession, table_meta, queries: dict, params: Params):
        where_list = []
        for key, value in queries.items():
            where_list.append(key == value)

        query = select(table_meta).where(and_(*where_list))

        return await paginate(query=query, params=params, conn=session)

    @staticmethod
    async def save(session: AsyncSession, table_meta: DeclarativeMeta, columns: dict):
        await session.execute(insert(table_meta).values(**columns))
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, table_meta: DeclarativeMeta, queries: dict, columns: dict):
        where_list = []
        for key, value in queries.items():
            where_list.append(key == value)

        await session.execute(update(table_meta).where(and_(*where_list)).values(**columns))
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, table_meta: DeclarativeMeta, queries: dict):
        where_list = []
        for key, value in queries.items():
            where_list.append(key == value)

        await session.execute(delete(table_meta).where(and_(*where_list)))
        await session.commit()
