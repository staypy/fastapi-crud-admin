import asyncio

import nest_asyncio
import uvicorn
from fastapi import FastAPI
from starlette.responses import Response

from fastapi_crud_admin.admin import FastAPIAdmin
from fastapi_crud_admin.enum import HttpMethod
from test.example.config import db
from test.example.schema import Example, Test

nest_asyncio.apply()


def before_handler(http_method: HttpMethod, queries: dict, columns: dict) -> None:
    """
    Custom before handler.

    Parameters:
    - http_method (fastapi_crud_admin.enum.HttpMethod): http method of schema router.
    - queries (dict): query dictionary used in the where clause.
    - columns (dict): dictionary to be stored in a row.
    """
    print(f"Before handler. Method: {http_method}")
    print(f"queries: {queries}")
    print(f"columns: {columns}")


def after_handler(response: Response) -> Response:
    """
    Custom after handler.

    Parameters:
    - response (starlette.response.Response): The FastAPI response object.
    """
    print(f"After handler. Result: {response}")
    return response


def create_app() -> FastAPI:
    _app = FastAPI()

    """ Define Admin """
    admin = FastAPIAdmin(
        app=_app,
        db_url="sqlite+aiosqlite:///./test.db"

    )
    admin.register_schema_meta(models=[Example, Test])
    admin.register_interceptor(table_name="tb_example", before_handler=before_handler, after_handler=after_handler)
    admin.register_schema_router()

    return _app


app = create_app()


@app.on_event("startup")
async def startup():
    """ Initialize Database """
    asyncio.run(db.create_database())


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
