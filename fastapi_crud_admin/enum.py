from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    @staticmethod
    def parse(url_method: str):
        if url_method == "get":
            return HttpMethod.GET
        elif url_method == "create":
            return HttpMethod.POST
        elif url_method == "update":
            return HttpMethod.PUT
        elif url_method == "delete":
            return HttpMethod.DELETE
        else:
            raise Exception(f"method {url_method} is not supported")
