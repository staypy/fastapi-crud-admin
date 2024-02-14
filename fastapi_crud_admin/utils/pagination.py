from typing import TypeVar, Generic, List

from fastapi_pagination import Page
from pydantic.generics import GenericModel

T = TypeVar('T')


class Pagination(GenericModel, Generic[T]):
    next_page_num: int
    previous_page_num: int
    total: int
    items: List[T]


async def to_pagination(p: Page[T]):
    return Pagination(
        next_page_num=__build_next_page(p),
        previous_page_num=__build_previous_page(p),
        total=p.total,
        items=p.items
    )


def __build_next_page(p: Page[T]):
    if p.pages < p.page:
        return p.page

    return p.page + 1


def __build_previous_page(p: Page[T]):
    return max(1, p.page - 1)
