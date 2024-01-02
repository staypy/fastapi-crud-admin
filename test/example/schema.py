from sqlalchemy import Column, Integer, String

from test.example.config import Base


class Example(Base):
    __tablename__ = 'tb_example'
    index = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=200), nullable=False)
