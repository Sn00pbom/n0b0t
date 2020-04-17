import json

from discord.ext.commands import Bot

from voting import Counsel
from currency import CurrencyManager


PREFIX = '.'
user_contexts = {}  # user : context_id


client = Bot(command_prefix=PREFIX)

counsel = Counsel()
curr_man = CurrencyManager(client)