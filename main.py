import datetime

import discord
import os

from discord import ExtensionNotFound, HTTPException
from dotenv import load_dotenv
from tortoise import run_async

import anilibria
import config
from utils.database import db_init

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)
api = anilibria.Api(discord_instance=bot)


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")


@bot.event
async def on_guild_join(guild: discord.Guild):
    db_guild_object, created = await anilibria.Guild.get_or_create(discord_id=guild.id)

    embed = discord.Embed(colour=discord.Colour.gold(), timestamp=discord.utils.utcnow())
    embed.description = f"""
**Спасибо за добавление MLP! **

Этот бот умеет работать с API `anilibria.tv`, узнать больше информации можно командой </info:1015015152644542486>.
Для установки оповещений о выходе новых серий ваших любимых тайтлов - используйте </reminder set:1014820755021770772>.

Разработчик - `gigalegit-#0880`, бот НЕ ЯВЛЯЕТСЯ официальным и никак не относится к `anilibria.tv` ⚠

{'Бот добавлен впервые! ✅' if created else ''}
    """

    embed.set_footer(icon_url=bot.user.avatar.url, text=config.DEFAULT_FOOTER)

    support_server_button = discord.ui.Button(url=config.SUPPORT_SERVER, label='Сервер Тех. Поддержки', emoji='🔧')
    view = discord.ui.View()
    view.add_item(support_server_button)

    try:
        await guild.system_channel.send(embed=embed, view=view)
    except HTTPException:
        pass


if __name__ == "__main__":
    for cog in config.COGS:
        try:
            bot.load_extension(cog)
        except ExtensionNotFound:
            print(f'Extension {cog} not found.')
            continue

    run_async(db_init())
    bot.run(os.getenv("TOKEN"))
