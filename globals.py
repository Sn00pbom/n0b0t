import json

from discord.ext.commands import Bot

from voting import Counsel


PREFIX = '.'
user_contexts = {}  # user : context_id

counsel = Counsel()

client = Bot(command_prefix=PREFIX)
