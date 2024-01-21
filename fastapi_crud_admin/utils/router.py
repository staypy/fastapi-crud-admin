from fastapi import APIRouter


class Router:
    def __init__(self, router: APIRouter) -> None:
        self._router = router

    @property
    def router(self):
        for route in self._router.routes:
            func = route.endpoint
            if hasattr(func, '__get__'):
                route.endpoint = func.__get__(self, self.__class__)
        return self._router
