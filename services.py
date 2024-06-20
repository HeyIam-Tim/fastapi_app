import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, delete, select, insert, update, Table

from typing import Union

from models import link, counter
from schemas import LinkResponse


class ImageRequest:
    """Запрос на изображение."""

    url = 'https://dog.ceo/api/breeds/image/random'

    async def get_dog_image(self) -> LinkResponse:
        """Получает ссылку на изображение."""

        async with aiohttp.ClientSession() as session:
            response = await session.get(url=self.url)
            image_link = await response.json()
            return LinkResponse(**image_link)


class CounterHandler:
    """Счетчик."""

    counter = counter

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
        return

    async def update_counter(self, counter: Row) -> Row:
        """Обновляет количество запросов."""

        stmt = update(self.counter).where(
            self.counter.c.id == counter.id).values(count=counter.count + 1)
        await self.commit_to_db(stmt=stmt)
        return await self.get_counter()

    async def create_counter(self) -> None:
        """Сохраняет количетво запросов в бд."""

        stmt = insert(self.counter).values(count=1)
        await self.commit_to_db(stmt=stmt)
        return

    async def get_counter(self) -> Union[Row, None]:
        """Получает количетво запросов из бд."""

        result = await self.db_session.execute(select(self.counter))
        counter = result.first()
        if counter:
            return counter
        else:
            return

    async def commit_to_db(self, stmt):
        """Коммитит в бд."""

        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return


class Image:
    """Для работы с изображениями."""

    image_request = ImageRequest()
    link = link

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
        self.counter_handler = CounterHandler(db_session=db_session)
        return

    async def get_dog_image(self) -> LinkResponse:
        """Получает ссылку на изображение."""

        image_link = await self.image_request.get_dog_image()

        counter = await self.counter_handler.get_counter()
        if counter:
            counter = await self.counter_handler.update_counter(
                counter=counter)
            if not counter.count % 5 == 0:
                await self.create_link(url=image_link.message)
        else:
            await self.counter_handler.create_counter()

        await self.delete_first_link()
        return image_link

    async def create_link(self, url: str) -> Table:
        """Сохраняет ссылку в бд."""

        stmt = insert(self.link).values(url=url)
        await self.commit_to_db(stmt=stmt)
        return

    async def get_first_link(self) -> Union[Row, None]:
        """Получает первую ссылку."""

        result = await self.db_session.execute(select(self.link))
        link = result.first()
        return link

    async def delete_link(self, link: Row) -> None:
        """Удаляет ссылку."""

        if link:
            stmt = delete(self.link).where(self.link.c.id == link.id)
            await self.commit_to_db(stmt=stmt)
            return
        else:
            return

    async def delete_first_link(self) -> None:
        """Удаляет первую ссылку."""

        first_link = await self.get_first_link()
        return await self.delete_link(link=first_link)

    async def commit_to_db(self, stmt):
        """Коммитит в бд."""

        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return
