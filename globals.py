import json

from discord.ext.commands import Bot

from voting import Counsel
from currency import CurrencyManager, MineTimer
from data import UserDB


PREFIX = '.'
user_contexts = {}  # user : context_id


client = Bot(command_prefix=PREFIX)

userdb = UserDB()
counsel = Counsel()
curr_man = CurrencyManager(client, userdb)
mine_timer = MineTimer(curr_man)