from sqlalchemy import select, delete, and_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta


class Repository:
    @staticmethod
    async def find_all(session: AsyncSession, table_meta):
        result = await session.execute(select(table_meta))
        return result.scalars().all()

    @staticmethod
    async def save(session: AsyncSession, table_meta: DeclarativeMeta, columns: dict):
        await session.execute(insert(table_meta).values(**columns))
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, table_meta: DeclarativeMeta, columns: dict):
        query = delete(table_meta)

        where_list = []
        for key, value in columns.items():
            where_list.append(key == value)

        query = query.where(and_(*where_list))

        await session.execute(query)
        await session.commit()
