from tortoise import Tortoise
from .colors import ConsoleColors as clrs


async def db_init():
    await Tortoise.init(
        db_url='sqlite://bot.db',
        modules={'models': ['anilibria.models.db']}
    )

    print(f'{clrs.OKBLUE}Database initialised...')

    await Tortoise.generate_schemas(safe=True)

