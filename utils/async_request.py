import aiohttp
from typing import Union
import utils.colors


async def get(string: str, params: dict) -> Union[dict, None]:
    async with aiohttp.ClientSession() as session:
        async with session.get(string, params=params) as resp:

            print(f'{utils.colors.ConsoleColors.OKBLUE}Fetching...')

            if resp.status == 404:
                return None

            return await resp.json()
