from tortoise import fields
from tortoise.models import Model


class Guild(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.IntField()
    reminder_channel_id = fields.IntField(default=0)

    beta = fields.BooleanField(default=False)
    reminder_ping = fields.BooleanField(default=False)

    def __str__(self):
        return self.discord_id

    def __repr__(self):
        return f'Guild({self.discord_id=}, {self.id=})'
