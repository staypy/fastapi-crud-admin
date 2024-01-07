from typing import List, Any

from fastapi import FastAPI
from sqlalchemy.orm import DeclarativeMeta

from fastapi_admin.meta import TableMeta, AdminMeta
from fastapi_admin.router.meta import MetaRouter
from fastapi_admin.router.schema import SchemaRouter
from fastapi_admin.utils.database import Database


def register(
        app: FastAPI,
        models: List[Any],
        db_url: str,
        prefix: str = ''
):
    for model in models:
        if not isinstance(model, DeclarativeMeta):
            raise Exception(f"model must be instance of DeclarativeMeta, but {model} is {type(model)}")

    classes = {model.__table__.name: model for model in models}
    tables = {
        model.__table__.name: TableMeta(
            table=model.__table__,
            columns={column.name: column for column in model.__table__.columns}
        ) for model in models
    }

    meta = AdminMeta(
        classes=classes,
        tables=tables
    )

    database = Database(db_url)

    app.include_router(MetaRouter(meta).router, prefix=prefix)
    app.include_router(SchemaRouter(meta, database).router, prefix=prefix)
