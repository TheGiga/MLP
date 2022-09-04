from typing import Union

from tortoise import fields
from tortoise.models import Model
from utils.colors import ConsoleColors as clrs


class Reminder(Model):
    id = fields.IntField(pk=True)
    guild_id = fields.IntField()
    channel_id = fields.IntField(default=0)
    ping = fields.IntField(default=0)

    def __repr__(self):
        return f'Reminder({self.channel_id=}, {self.guild_id=})'


class Guild(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.IntField()

    beta = fields.BooleanField(default=False)

    async def get_or_create_reminder(self) -> Reminder:
        reminder, created = await Reminder.get_or_create(guild_id=self.discord_id)

        if created:
            print(f'{clrs.OKBLUE} Created reminder for {self.discord_id}')

        return reminder

    async def get_reminder(self) -> Union[Reminder, None]:
        reminder = await Reminder.get_or_none(guild_id=self.discord_id)
        return reminder

    def __str__(self):
        return self.discord_id

    def __repr__(self):
        return f'Guild({self.discord_id=}, {self.id=})'
