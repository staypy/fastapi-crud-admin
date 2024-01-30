from functools import wraps

from starlette.requests import Request

from fastapi_crud_admin.enum import HttpMethod


def api_interceptor(route_func):
    @wraps(route_func)
    async def wrapper(instance, _request: Request, *args, **kwargs):
        if instance.table_meta.before_handler:
            http_method = HttpMethod.parse(str(_request.url).split("/")[-1])

            if http_method == HttpMethod.GET:
                instance.table_meta.before_handler(http_method, kwargs.get("queries"), {})
            elif http_method == HttpMethod.POST:
                instance.table_meta.before_handler(http_method, {}, kwargs.get("columns"))
            elif http_method == HttpMethod.PUT:
                instance.table_meta.before_handler(http_method, kwargs.get("queries"), kwargs.get("columns"))
            elif http_method == HttpMethod.DELETE:
                instance.table_meta.before_handler(http_method, kwargs.get("queries"), {})

        response = await route_func(instance, _request, *args, **kwargs)

        if instance.table_meta.after_handler:
            response = instance.table_meta.after_handler(response)

        return response

    return wrapper
