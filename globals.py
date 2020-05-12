import json
from os import path
from shutil import copyfile

from discord.ext.commands import Bot


CONFIG_VERSION = "1.0"

#
# Begin Load Config
#

if not path.exists('config.json'):  # copy default config if file doesn't exist
    copyfile('defaults/config.json', 'config.json')

with open('config.json', 'r') as f:
    CONFIG = json.loads(f.read())
    if CONFIG['.version'] != CONFIG_VERSION:  # exit if config version mismatch
        print('NO CONFIG VERSION')
        exit(1)
    # check config still has default values
    if CONFIG['token'] == 'YOUR BOT TOKEN' or \
            CONFIG['chat-channel-id'] == 1234567890 or \
            CONFIG['tree-channel-id'] == 1234567890:  # exit if default values remain
        print('CHANGE VALUES IN config.json')
        exit(1)
#
# End Load Config
#

#
# Begin create instances
#
from voting import Counsel
from currency import CurrencyManager, MineTimer
from data import UserDB


client = Bot(command_prefix=CONFIG['prefix'])

userdb = UserDB()
counsel = Counsel()
curr_man = CurrencyManager(client, userdb)
mine_timer = MineTimer(curr_man)
#
# End create instances
#
