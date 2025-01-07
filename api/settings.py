from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from envparse import Env

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent

env = Env()


REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres",
)


engine = create_async_engine(REAL_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class AuthJWT(BaseModel):

    private_key_path: Path = BASE_DIR / "api" / "jwt_auth" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "api" / "jwt_auth" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    pass


class Settings(BaseSettings):

    auth_jwt: AuthJWT = AuthJWT()



path_settings = Settings()
