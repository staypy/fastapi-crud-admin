# fastapi-crud-admin

[![Python](https://img.shields.io/pypi/pyversions/fastapi-crud-admin.svg?color=%2334D058)](https://pypi.org/project/fastapi-crud/)
[![CI](https://github.com/staypy/fastapi-crud-admin/actions/workflows/ci.yml/badge.svg)](https://github.com/staypy/fastapi-crud-admin/actions/workflows/ci.yml)
[![pypi](https://img.shields.io/pypi/v/fastapi-crud-admin?color=%2334D058)](https://pypi.org/project/fastapi-crud-admin/)

## Install

---
```bash
> pip install fastapi-crud-admin
```

## Dependencies

---
- FastAPI
- SqlAlchemy
- SqlLite

## Features

---
- CRUD API of all tables of SqlAlchemy with FastAPI
- Custom interceptor for each CRUD API
- Custom authentication

## Example

---
**1. Create a FastAPI Admin instance**
```python
from fastapi import FastAPI
from fastapi_crud_admin.admin import FastAPIAdmin

_app = FastAPI()

admin = FastAPIAdmin(
    app=_app,
    db_url="sqlite+aiosqlite:///./test.db"
)
```

**2. Register sqlalchemy models in admin and create crud router for models**
```python
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Example(Base):
    __tablename__ = 'tb_example'
    index = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=200), nullable=False)

admin.register_schema_meta(models=[Example])
admin.register_schema_router()
```

**3. (Optional) Register custom interceptor for crud router**
```python
from fastapi_crud_admin.enum import HttpMethod
from fastapi.responses import Response

def before_handler(http_method: HttpMethod, queries: dict, columns: dict) -> None:
    print(f"Before handler. Method: {http_method}")
    print(f"queries: {queries}")
    print(f"columns: {columns}")


def after_handler(response: Response) -> Response:
    print(f"After handler. Result: {response}")
    return response

admin.register_interceptor(table_name="tb_example", before_handler=before_handler, after_handler=after_handler)
```

**4. (Optional) Register custom authentication for crud router**
```python
import bcrypt

def password_verifier(src: str, dest: str) -> bool:
    return bcrypt.checkpw(dest.encode('utf-8'), src.encode('utf-8'))

admin.register_authentication(
    user_name="admin",
    password=bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    password_verifier=password_verifier
)
```