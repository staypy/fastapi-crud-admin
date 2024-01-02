from fastapi import APIRouter

from fastapi_admin.meta import AdminMeta
from fastapi_admin.router.router import Router

router = APIRouter(prefix='/meta')


class MetaRouter(Router):
    def __init__(self, meta: AdminMeta):
        super().__init__(router)
        self.meta = meta

    @router.get('/meta/tables')
    async def get_tables(self):
        return [table_meta.table.name for table_meta in self.meta.tables]

    @router.get('/meta/tables/{table_name}')
    async def get_table_meta(self, table_name: str):
        for table in self.meta.tables:
            if table.table.name == table_name:
                return {
                    'columns': [{
                        'name': column.name,
                        'type': str(column.type),
                        'primary_key': True if column.primary_key else False,
                        'nullable': True if column.nullable else False,
                        'autoincrement': True if column.autoincrement != "auto" else False,
                        'unique': True if column.unique else False
                    } for column in table.columns]
                }

        return {'columns': []}
