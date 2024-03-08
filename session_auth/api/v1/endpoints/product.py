from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from session_auth.models.product_model import ProductModel
from session_auth.models.user_model import UserModel
from session_auth.schemas.product_schema import ProductSchema
from session_auth.core.deps import get_session, get_current_user

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def post_product(product: ProductSchema,
                       current_user: UserModel = Depends(get_current_user),
                       db: AsyncSession = Depends(get_session)):

    new_product = ProductModel(id=product.id,
                               title=product.title,
                               description=product.description,
                               url=product.url,
                               user_id=current_user.id)

    db.add(new_product)
    await db.commit()

    return new_product


@router.get('/', response_model=List[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel)
        result = await session.execute(query)
        product: List[ProductModel] = result.scalars().unique().all()

        return product


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def get_product(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == id)
        result = await session.execute(query)
        product: ProductModel = result.scalars().unique().one_or_none()

        if product:
            return product
        else:
            raise HTTPException(detail="product not found", status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ProductSchema)
async def put_product(id: int,
                      product: ProductSchema,
                      current_user: UserModel = Depends(get_current_user),
                      db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == id)
        result = await session.execute(query)
        product_to_update: ProductModel = result.scalars().unique().one_or_none()

        if product_to_update:
            if product_to_update.title:
                product_to_update.title = product.title
            if product_to_update.url:
                product_to_update.url = product.url
            if product_to_update.description:
                product_to_update.description = product.description
            if current_user.id != product_to_update.user_id:
                product_to_update.user_id = current_user.user_id

            await session.commit()

            return product_to_update
        else:
            raise HTTPException(detail="product not found", status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int,
                         current_user: UserModel = Depends(get_current_user),
                         db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProductModel).filter(ProductModel.id == id).filter(ProductModel.user_id == current_user.id)
        result = await session.execute(query)
        product_to_delete: ProductModel = result.scalars().unique().one_or_none()

        if product_to_delete:
            await session.delete(product_to_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="course not found", status_code=status.HTTP_404_NOT_FOUND)
