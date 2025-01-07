from fastapi import APIRouter, HTTPException
import random
import re

from schemas.user_schemas import (
    UserCreate,
    UserCreateResponse,
    TokenCreate,
    TokenResponse,
)
from models.user_model import User

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from settings import async_session
from fastapi.security import HTTPBearer

from jwt_auth.utils import encode_jwt

http_bearer = HTTPBearer()

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.confirmation_code = None

    async def create_user(self, email: str, username: str) -> User:
        confirmation_code = str(random.randint(100000, 999999))
        new_user = User(
            email=email, username=username, confirmation_code=confirmation_code
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.send_confirmation_email(email, confirmation_code)
        return new_user

    async def send_confirmation_email(self, email: str, confirmation_code: str) -> None:
        print(f"Sending confirmation email to {email} with code: {confirmation_code}")


async def _create_new_user(body: UserCreate) -> UserCreateResponse:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(email=body.email, username=body.username)
            return UserCreateResponse(email=user.email, username=user.username)


async def _get_token(username: str, confirmation_code: str) -> dict:
    async with async_session() as session:
        async with session.begin():
            # Выполняем запрос для получения пользователя по имени
            result = await session.execute(select(User).filter_by(username=username))
            user = result.scalar_one_or_none()  # Получаем пользователя или None

            # Проверяем наличие пользователя и корректность кода подтверждения
            if not user or user.confirmation_code != confirmation_code:
                raise HTTPException(
                    status_code=400, detail="Invalid username or confirmation code"
                )

            # Создание токена доступа
            # access_token = create_access_token(data={"sub": user.username})
            access_token = encode_jwt(payload={"username": user.username})

            return {"token": access_token}


auth_router = APIRouter()


@auth_router.post("/signup", response_model=UserCreateResponse)
async def create_user(body: UserCreate) -> UserCreateResponse:
    return await _create_new_user(body)


@auth_router.post("/token", response_model=TokenResponse)
async def get_token(body: TokenCreate):
    return await _get_token(body.username, body.confirmation_code)
