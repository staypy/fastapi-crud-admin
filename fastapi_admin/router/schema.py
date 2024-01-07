from fastapi import APIRouter

from fastapi_admin.meta import AdminMeta
from fastapi_admin.utils.repository import Repository
from fastapi_admin.utils.router import Router

router = APIRouter(prefix='/schema')


class SchemaRouter(Router):
    def __init__(self, meta: AdminMeta, database):
        super().__init__(router)
        self.meta = meta
        self.database = database

    @router.get('/{table_name}')
    async def find_rows(self, table_name: str):
        async with self.database.async_session_maker() as session:
            try:
                return await Repository.find_all(session, self.meta.classes[table_name])
            finally:
                await session.close()

    @router.post('/{table_name}')
    async def create_row(self, table_name: str):
        async with self.database.async_session_maker() as session:
            try:
                pass
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @router.put('/{table_name}/{row_id}')
    async def update_row(self, table_name: str, row_id):
        async with self.database.async_session_maker() as session:
            try:
                pass
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @router.delete('/{table_name}/{row_id}')
    async def delete_row(self, table_name: str, row_id):
        async with self.database.async_session_maker() as session:
            try:
                pass
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

