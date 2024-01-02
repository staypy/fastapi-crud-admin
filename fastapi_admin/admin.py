from typing import List, Any

from fastapi import FastAPI
from sqlalchemy.orm import DeclarativeMeta

from fastapi_admin.meta import TableMeta, AdminMeta
from fastapi_admin.router.meta import MetaRouter


def register(
        app: FastAPI,
        models: List[Any],
        prefix: str = ''
):
    for model in models:
        if not isinstance(model, DeclarativeMeta):
            raise Exception(f"model must be instance of DeclarativeMeta, but {model} is {type(model)}")

    tables = [TableMeta(table=model.__table__, columns=model.__table__.columns) for model in models]

    meta = AdminMeta(
        tables=tables
    )

    app.include_router(MetaRouter(meta).router, prefix=prefix)
