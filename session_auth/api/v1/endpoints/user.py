from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from session_auth.models.user_model import UserModel
from session_auth.schemas.user_schema import UserSchemaBase, UserSchemaUpdate, UserSchemaProducts, UserSchemaCreate
from session_auth.core.deps import get_session, get_current_user
from session_auth.core.security import create_hash_token
from session_auth.core.auth import auth, create_access_token

router = APIRouter()


# GET Logado
@router.get('/logged', response_model=UserSchemaBase)
def get_user(current_user: UserModel = Depends(get_current_user)):
    return current_user


# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(name=user.name,
                                    last_name=user.last_name,
                                    email=user.email,
                                    password=create_hash_token(user.password),
                                    is_admin=user.is_admin)
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='There is already a user with that email')


# GET Users
@router.get('/', response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users


# GET Usuario
@router.get('/{user_id}', response_model=UserSchemaProducts, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT User
@router.put('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, current_user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_to_update: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_to_update:
            if user_to_update.name:
                user_to_update.name = current_user.name
            if user_to_update.last_name:
                user_to_update.last_name = current_user.last_name
            if user_to_update.email:
                user_to_update.email = current_user.email
            if user_to_update.is_admin:
                user_to_update.is_admin = current_user.is_admin
            if user_to_update.password:
                user_to_update.password = create_hash_token(current_user.password)

            await session.commit()

            return user_to_update
        else:
            raise HTTPException(detail='user not found.',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE user
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserSchemaProducts = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_session)):
    user = await auth(email=form_data.username, token=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": create_access_token(sub=user.id), "token_type": "bearer"},
                        status_code=status.HTTP_200_OK)
