import asyncio
from typing import List, Any, Callable, Optional

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlalchemy.orm import DeclarativeMeta
from starlette.responses import Response

from fastapi_crud_admin.enum import HttpMethod
from fastapi_crud_admin.meta import TableMeta, AdminMeta
from fastapi_crud_admin.router.auth import AuthRouter
from fastapi_crud_admin.router.meta import MetaRouter
from fastapi_crud_admin.router.schema import SchemaRouter
from fastapi_crud_admin.utils.auth import Authentication, auth_db
from fastapi_crud_admin.utils.database import Database


class FastAPIAdmin:
    def __init__(self, app: FastAPI, db_url: str, prefix: str = ''):
        """
        Parameters:
        - app (FastAPI): The FastAPI app instance.
        - db_url (str): Database connection URL.
        - prefix (str, optional): URL prefix for the models.
        """
        self.app = app
        self.db_url = db_url
        self.prefix = prefix
        self.meta = None

    def register_schema_meta(
            self,
            models: List[Any]
    ):
        """
        Register entity classes and routers to FastAPI app.

        Parameters:
        - models (List[Any]): List of entity classes.
        """
        for model in models:
            if not isinstance(model, DeclarativeMeta):
                raise Exception(f"model must be instance of DeclarativeMeta, but {model} is {type(model)}")

        tables = {
            model.__table__.name: TableMeta(
                entity=model,
                table=model.__table__,
                columns={column.name: column for column in model.__table__.columns}
            ) for model in models
        }

        add_pagination(self.app)

        self.meta = AdminMeta(tables=tables)

        self.app.include_router(MetaRouter(self.meta).router, prefix=self.prefix)

    def register_interceptor(
            self,
            table_name: str,
            before_handler: Optional[Callable[[HttpMethod, dict[str, Any], dict[str, Any]], None]] = None,
            after_handler: Optional[Callable[[Response], Response]] = None
    ):
        """
        - table_name (str): Name of the table to be intercepted.
        - before_handler (Callable[[HttpMethod, dict, dict], None], optional):
          Callback function executed before handling a request.
          Expects http method of schema router as the first parameter, dictionary of queries, and dictionary of columns.
          Does not return any value (None).
        - after_handler (Callable[[Request, Any], Any], optional):
          Callback function executed after handling a request.
          Expects a Request object as the first parameter.
          Returns the client response.
        """
        self.meta.tables[table_name].before_handler = before_handler
        self.meta.tables[table_name].after_handler = after_handler

    def register_schema_router(self):
        database = Database(self.db_url)

        for table_name, table_meta in self.meta.tables.items():
            self.app.include_router(
                SchemaRouter(table_name, table_meta, database).router,
                prefix=f"{self.prefix}/{table_name}"
            )

    def register_authentication(self, user_name: str, password: str, password_verifier: Callable[[str, str], bool]):
        asyncio.run(auth_db.create_database())

        self.meta.authentication = Authentication(user_name, password, password_verifier)

        self.app.include_router(AuthRouter(self.meta.authentication).router, prefix=self.prefix)
