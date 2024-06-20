from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from schemas import LinkResponse
from services import Image


router = APIRouter(
    prefix="/dog-link",
    tags=["Link"],
)


@router.get('/')
async def get_dog_link(
        db_session: AsyncSession = Depends(get_async_session)) -> LinkResponse:
    """Получает ссылку на изображение."""

    print('GET DOG LINK')
    image_service = Image(db_session=db_session)
    image_link = await image_service.get_dog_image()
    return image_link
