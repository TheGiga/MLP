import time

import discord
from utils import async_get
from typing import Union

from .models import Title
from .api_config import API_ENDPOINT, TITLE_FILTER


class Api:
    def __init__(self, discord_instance: discord.Bot):
        self.discord = discord_instance
        self.latest_call = int(time.time())

    @staticmethod
    async def get_title(title_id: int) -> Union[Title, None]:
        data = await async_get(
            f'{API_ENDPOINT}/getTitle',
            params={
                'id': title_id,
                'filter': TITLE_FILTER
            }
        )

        if data is None:
            return None

        title = Title.parse_obj(data)
        return title

    async def get_updates(self) -> list[Title]:
        data = await async_get(
            f'{API_ENDPOINT}/getUpdates',
            params={
                'filter': TITLE_FILTER,
                'since': self.latest_call
            }
        )

        titles = []

        for title in data:
            ttl_obj = Title.parse_obj(title)
            titles.append(ttl_obj)

        self.latest_call = int(time.time())

        return titles
