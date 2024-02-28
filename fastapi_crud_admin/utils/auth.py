from typing import Callable
from uuid import uuid4

from fastapi import Cookie, HTTPException, status
from sqlalchemy import Column, String, select, insert

from fastapi_crud_admin.utils.database import Database

auth_db = Database(db_url="sqlite+aiosqlite:///./auth.db")


class Session(auth_db.base):
    __tablename__ = "_session"
    session_id = Column(String(length=255), primary_key=True, default=lambda: str(uuid4()))


async def __get_db_session(session_id: str):
    async with auth_db.async_session_maker() as db_session:
        try:
            result = await db_session.execute(select(Session).where(Session.session_id == session_id))
            session = result.scalars().one_or_none()
            if session is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="session not found")

            return session
        finally:
            await db_session.close()


async def get_session(session_id: str = Cookie(None)):
    try:
        return await __get_db_session(session_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="session not found")


class Authentication:
    def __init__(
            self,
            user_name: str,
            password: str,
            password_verifier: Callable[[str, str], bool]
    ):
        self.user_name = user_name
        self.password = password
        self.password_verifier = password_verifier

    async def login(self, username: str, password: str):
        if username == self.user_name and self.verify_password(password):
            async with auth_db.async_session_maker() as db_session:
                try:
                    session_id = str(uuid4())
                    await db_session.execute(insert(Session).values({Session.session_id: session_id}))
                    await db_session.commit()
                    return session_id
                except Exception as e:
                    await db_session.rollback()
                    raise e
                finally:
                    await db_session.close()

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="login failed")

    def verify_password(self, password: str):
        if self.password_verifier is not None:
            return self.password_verifier(password, self.password)
        return password == self.password
