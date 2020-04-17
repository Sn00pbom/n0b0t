import json

from discord.ext.commands import Bot

from voting import Counsel
from currency import CurrencyManager, MineTimer


PREFIX = '.'
user_contexts = {}  # user : context_id


client = Bot(command_prefix=PREFIX)

counsel = Counsel()
curr_man = CurrencyManager(client)
mine_timer = MineTimer(curr_man)