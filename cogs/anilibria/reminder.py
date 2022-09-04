import discord
from discord import SlashCommandGroup, guild_only, NotFound
from discord.ext import tasks
from discord.ext.commands import has_permissions

import config
from anilibria.api_config import AL_TITLE, AL_URL
from anilibria import Guild
from main import api
from utils import ConsoleColors as clrs


class ALReminder(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.reminder_loop.start()

    reminder = SlashCommandGroup("reminder", "Оповещения о новых релизах.")

    @guild_only()
    @has_permissions(manage_guild=True)
    @reminder.command(name='disable', description='Отключить отправку оповещений.')
    async def slash_disable(
            self, ctx: discord.ApplicationContext
    ):
        db_guild_object, created = await Guild.get_or_create(discord_id=ctx.guild.id)

        if created:
            print(f'Created object for guild {ctx.guild}({ctx.guild.id}), not in `on_guild_join`.')

        if db_guild_object.reminder_channel_id == 0:
            return await ctx.respond(
                content="Оповещения уже отключены, используйте </reminder set:1015015152644542485> для их включения.",
                phemeral=True
            )

        db_guild_object.reminder_channel_id = 0
        await db_guild_object.save()

        await ctx.respond(
            content=f'✅ Оповещения о выходе новых серий успешно отключены.', ephemeral=True
        )

    @guild_only()
    @has_permissions(manage_guild=True)
    @reminder.command(name='set', description='Включить отправку оповещений.')
    async def slash_set(
            self, ctx: discord.ApplicationContext, channel: discord.Option(
                discord.TextChannel, name='канал', description='Канал в который будут отправляться оповещения.'
            )
    ):
        db_guild_object, created = await Guild.get_or_create(discord_id=ctx.guild.id)

        if created:
            print(f'Created object for guild {ctx.guild}({ctx.guild.id}), not in `on_guild_join`.')

        if not channel.can_send():
            return await ctx.respond(
                '❌ **У бота недостаточно прав для отправления сообщений в данный канал!** \n'
                'Выдайте следующие права: `Send Messages`, `Embed Links`; Либо используйте другой канал.',
                ephemeral=True
            )

        db_guild_object.reminder_channel_id = channel.id
        await db_guild_object.save()

        embed = discord.Embed(colour=discord.Colour.embed_background(), timestamp=discord.utils.utcnow())
        embed.description = """
**Данный канал установлен для получения уведомлений о выходе новых серий аниме на сайте `anilibria.tv`**.

Для отключения уведомлений пропишите </reminder disable:1015015152644542485>
        """

        embed.set_footer(icon_url=self.bot.user.avatar.url, text=config.DEFAULT_FOOTER)

        await ctx.respond(
            content=f'✅ Канал {channel.mention} успешно установлен для получения оповещений!', ephemeral=True
        )
        await channel.send(embed=embed)

    @tasks.loop(minutes=5)
    async def reminder_loop(self):
        if not self.bot.is_ready():
            return

        to_post = await api.get_updates()

        if len(to_post) == 0:
            print(f'{clrs.WARNING}No updates.')
            return

        print(f'{clrs.OKGREEN}There is updates, processing...')

        db_guilds = await Guild.exclude(reminder_channel_id=0)

        print(f'{clrs.OKCYAN}Guilds (raw): {db_guilds}')

        for db_guild_object in db_guilds:
            guild = self.bot.get_guild(db_guild_object.discord_id)
            if guild is None:
                try:
                    guild = await self.bot.fetch_guild(db_guild_object.discord_id)
                except NotFound:
                    print(f"{clrs.FAIL}Guild with ID {db_guild_object.discord_id} not found!")
                    continue

            channel = guild.get_channel(db_guild_object.reminder_channel_id)

            if channel is None:
                try:
                    await guild.fetch_channel(db_guild_object.reminder_channel_id)
                except NotFound:
                    print(f"{clrs.FAIL}Channel with ID {db_guild_object.reminder_channel_id} not found!")
                    continue

            for update in to_post:
                embed = discord.Embed(colour=discord.Colour.red(), timestamp=discord.utils.utcnow())

                title_desc = update.description
                description = (title_desc[:200] + '..') if len(title_desc) > 200 else title_desc

                embed.description = f"""
                {description}
                
                {f'⚠ **{update.announce}**' if len(update.announce) >= 1 else ''}
                """

                embed.title = f'{update.names.get("ru")} `({update.type.get("full_string")})`'

                embed.add_field(name='🧾 Серия', value=str(update.player['series'].get('last')))
                embed.add_field(name='ℹ️ Статус', value=str(update.status.get('string')))

                embed.set_image(url=f'{AL_URL}{update.posters["original"].get("url")}')

                view = discord.ui.View()
                watch_episode = discord.ui.Button(label='Смотреть серию', emoji="🖥️", url=AL_TITLE.format(update.code))
                view.add_item(watch_episode)

                await channel.send(embed=embed, view=view)

            print(f'{clrs.OKGREEN}Posted to {guild.name}')


def setup(bot: discord.Bot):
    bot.add_cog(ALReminder(bot=bot))
