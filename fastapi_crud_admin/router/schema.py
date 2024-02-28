from fastapi import APIRouter, Request, Depends
from fastapi_pagination import Params
from pydantic import BaseModel

from fastapi_crud_admin.meta import TableMeta
from fastapi_crud_admin.utils.auth import get_session
from fastapi_crud_admin.utils.interceptor import api_interceptor
from fastapi_crud_admin.utils.pagination import to_pagination
from fastapi_crud_admin.utils.repository import Repository
from fastapi_crud_admin.utils.router import Router

router = APIRouter(prefix='/schema')


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10


class SchemaRouter(Router):
    def __init__(
            self,
            table_name: str,
            table_meta: TableMeta,
            database
    ):
        super().__init__(router)
        self.table_name = table_name
        self.table_meta = table_meta
        self.database = database

    @router.post('/get')
    @api_interceptor
    async def find_rows(
            self,
            _request: Request,
            queries: dict,
            params: PaginationParams,
            session: str = Depends(get_session)
    ):
        async with self.database.async_session_maker() as db_session:
            try:
                table_meta = self.table_meta.table
                columns_for_query = {table_meta.columns[key]: value for key, value in queries.items()
                                     if value is not None}

                params = Params(page=params.page, size=params.size)

                return await to_pagination(
                    await Repository.find_all(db_session, self.table_meta.entity, columns_for_query, params))
            finally:
                await db_session.close()

    @router.post('/create')
    @api_interceptor
    async def create_row(
            self,
            _request: Request,
            columns: dict,
            session: str = Depends(get_session)
    ):
        async with self.database.async_session_maker() as db_session:
            try:
                table_meta = self.table_meta.table
                for key, value in columns.items():
                    if table_meta.columns.get(key) is None:
                        raise Exception(f"column {key} is not exist in table {self.table_name}")

                return await Repository.save(db_session, self.table_meta.entity, columns)
            except Exception as e:
                await db_session.rollback()
                raise e
            finally:
                await db_session.close()

    @router.post('/update')
    @api_interceptor
    async def update_row(
            self,
            _request: Request,
            queries: dict,
            columns: dict,
            session: str = Depends(get_session)
    ):
        async with self.database.async_session_maker() as db_session:
            try:
                table_meta = self.table_meta.table
                columns_for_query = {table_meta.columns[key]: value for key, value in queries.items()
                                     if value is not None}

                await Repository.update(db_session, self.table_meta.entity, columns_for_query, columns)
            except Exception as e:
                await db_session.rollback()
                raise e
            finally:
                await db_session.close()

    @router.post('/delete')
    @api_interceptor
    async def delete_row(
            self,
            _request: Request,
            columns: dict,
            session: str = Depends(get_session)
    ):
        async with self.database.async_session_maker() as db_session:
            try:
                table_meta = self.table_meta.table
                columns_for_query = {table_meta.columns[key]: value for key, value in columns.items()
                                     if value is not None}

                await Repository.delete(db_session, self.table_meta.entity, columns_for_query)
            except Exception as e:
                await db_session.rollback()
                raise e
            finally:
                await db_session.close()
