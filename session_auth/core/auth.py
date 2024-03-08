from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt
from session_auth.models.user_model import UserModel
from session_auth.core.configs import settings
from session_auth.core.security import validate_token

from pydantic import EmailStr

# creates an endpoint for the user authentication
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)


async def auth(email: str, token: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select((UserModel)).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not validate_token(token, user.password):
            return None

        return user


def _create_token(token_type: str, ttl: timedelta, sub: str) -> str:
    payload = {}
    time_zone = timezone('Portugal')
    expires = datetime.now(tz=time_zone) + ttl

    payload["type"] = token_type
    payload["exp"] = expires
    payload["iat"] = datetime.now(tz=time_zone)
    payload["sub"] = str(sub)

    return jwt.encode(claims=payload, key=settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    """
    https://jwt.io
    :param sub:
    :return:
    """

    return _create_token(
        token_type='access_token',
        ttl=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE),
        sub=sub
    )




