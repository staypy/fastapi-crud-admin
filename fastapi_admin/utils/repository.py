from typing import TypeVar, Generic, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    @staticmethod
    async def find_all(session: AsyncSession, table_meta):
        result = await session.execute(select(table_meta))
        return result.scalars().all()

    @staticmethod
    async def save(session: AsyncSession, entity):
        session.add(entity)
        await session.merge(entity)
        await session.commit()
        return entity

    @staticmethod
    async def delete(session: AsyncSession, entity):
        await session.delete(entity)
        await session.commit()
