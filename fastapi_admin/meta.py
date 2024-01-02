from typing import List

from sqlalchemy import Column, Table


class TableMeta:
    def __init__(
            self,
            table: Table,
            columns: List[Column]
    ):
        self.table = table
        self.columns = columns


class AdminMeta:
    def __init__(
            self,
            tables: List[TableMeta]
    ):
        self.tables = tables
