from fastapi import APIRouter
import random
import re
from schemas.user_schemas import UserCreate, UserCreateResponse
from models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from settings import async_session

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


auth_router = APIRouter()


@auth_router.post("/signup", response_model=UserCreateResponse)
async def create_user(body: UserCreate) -> UserCreateResponse:
    return await _create_new_user(body)
