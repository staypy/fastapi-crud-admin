import asyncio

import nest_asyncio
import uvicorn
from fastapi import FastAPI

from fastapi_admin.admin import register
from test.example.config import db
from test.example.schema import Example

nest_asyncio.apply()


def create_app() -> FastAPI:
    _app = FastAPI()

    """ Define Admin """
    register(
        app=_app,
        models=[Example]
    )

    return _app


app = create_app()


@app.on_event("startup")
async def startup():
    """ Initialize Database """
    asyncio.run(db.create_database())


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)