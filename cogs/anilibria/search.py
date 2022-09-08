import discord
from discord import SlashCommandGroup
from main import api


class ALSearch(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    search = SlashCommandGroup(name='search', description="Поиск аниме.")

    @search.command(name='id', description='Поиск по айди. (для разработчка)')
    async def search_id(
            self, ctx: discord.ApplicationContext,
            title_id: discord.Option(int, name='айди', description='Айди тайтла)')
    ):
        title = await api.get_title(title_id=title_id)

        if title is None:
            return await ctx.respond(content=f"❌ Аниме с айди `{title_id}` не найдено.", ephemeral=True)

        embed = title.form_embed()

        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(ALSearch(bot=bot))
