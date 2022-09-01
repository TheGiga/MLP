import discord

import config


class InfoCommand(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.description = "Информационная команда."

    @discord.slash_command(name='info', description='Базовая информация о боте.')
    async def information(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(colour=discord.Colour.embed_background(), timestamp=discord.utils.utcnow())

        embed.description = '**MLP**, "оповещалка" о новых сериях аниме на `anilibria.tv`, от `gigalegit-#0880`.\n' \
                            'Сделал я его в первую очередь для себя, ибо удобно, но пользоваться могут все.\n\n' \
                            '**Для добавления бота к себе:** Открываешь Профиль бота > Кликаешь `Большую синюю кнопку`'
        embed.title = config.PROJECT_NAME

        embed.add_field(name='👥 User Count', value=str(len(self.bot.users)))
        embed.add_field(name='📁 Guild Count', value=str(len(self.bot.guilds)))

        embed.set_thumbnail(url=self.bot.user.avatar.url)

        await ctx.respond(embed=embed)


def setup(bot: discord.Bot):
    bot.add_cog(InfoCommand(bot=bot))
