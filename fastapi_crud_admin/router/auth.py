from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import Response

from fastapi_crud_admin.utils.auth import Authentication
from fastapi_crud_admin.utils.router import Router

router = APIRouter(prefix='/admin-auth')


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthRouter(Router):
    def __init__(
            self,
            auth: Authentication
    ):
        super().__init__(router)
        self.auth = auth

    @router.post('/login')
    async def login(self, req: LoginRequest):
        session = await self.auth.login(req.username, req.password)

        response = Response()
        response.set_cookie(key="session_id", value=session)
        return response
