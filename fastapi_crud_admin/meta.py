from typing import Dict

from sqlalchemy import Column, Table
from sqlalchemy.orm import DeclarativeMeta


class TableMeta:
    def __init__(
            self,
            entity: DeclarativeMeta,
            table: Table,
            columns: Dict[str, Column]
    ):
        self.entity = entity
        self.table = table
        self.columns = columns
        self.before_handler = None
        self.after_handler = None


class AdminMeta:
    def __init__(
            self,
            tables: Dict[str, TableMeta]
    ):
        self.tables = tables
