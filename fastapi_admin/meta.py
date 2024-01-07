from typing import Dict

from sqlalchemy import Column, Table
from sqlalchemy.orm import DeclarativeMeta


class TableMeta:
    def __init__(
            self,
            table: Table,
            columns: Dict[str, Column]
    ):
        self.table = table
        self.columns = columns


class AdminMeta:
    def __init__(
            self,
            classes: Dict[str, DeclarativeMeta],
            tables: Dict[str, TableMeta]
    ):
        self.classes = classes
        self.tables = tables
