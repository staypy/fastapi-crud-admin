from fastapi import APIRouter

from fastapi_crud_admin.meta import AdminMeta
from fastapi_crud_admin.utils.repository import Repository
from fastapi_crud_admin.utils.router import Router

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

    @router.post('/{table_name}/create')
    async def create_row(self, table_name: str, columns: dict):
        async with self.database.async_session_maker() as session:
            try:
                table_meta = self.meta.tables[table_name]
                for key, value in columns.items():
                    if table_meta.columns.get(key) is None:
                        raise Exception(f"column {key} is not exist in table {table_name}")

                return await Repository.save(session, self.meta.classes[table_name], columns)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @router.post('/{table_name}/update')
    async def update_row(self, table_name: str, pks: dict, columns: dict):
        async with self.database.async_session_maker() as session:
            try:
                table_meta = self.meta.tables[table_name]
                columns_for_query = {table_meta.columns[key]: value for key, value in pks.items()
                                     if value is not None}

                await Repository.update(session, self.meta.classes[table_name], columns_for_query, columns)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @router.post('/{table_name}/delete')
    async def delete_row(self, table_name: str, columns: dict):
        async with self.database.async_session_maker() as session:
            try:
                table_meta = self.meta.tables[table_name]
                columns_for_query = {table_meta.columns[key]: value for key, value in columns.items()
                                     if value is not None}

                await Repository.delete(session, self.meta.classes[table_name], columns_for_query)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
