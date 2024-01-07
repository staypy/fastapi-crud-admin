from fastapi import APIRouter

from fastapi_admin.meta import AdminMeta
from fastapi_admin.utils.router import Router

router = APIRouter(prefix='/meta')


class MetaRouter(Router):
    def __init__(self, meta: AdminMeta):
        super().__init__(router)
        self.meta = meta

    @router.get('/tables')
    async def get_tables(self):
        return [table_name for table_name in self.meta.tables.keys()]

    @router.get('/tables/{table_name}')
    async def get_table_meta(self, table_name: str):
        table = self.meta.tables[table_name]

        return {
            'columns': [{
                'name': column.name,
                'type': str(column.type),
                'primary_key': True if column.primary_key else False,
                'nullable': True if column.nullable else False,
                'autoincrement': True if column.autoincrement != "auto" else False,
                'unique': True if column.unique else False
            } for _, column in table.columns.items()]
        }
