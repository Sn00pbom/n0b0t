import random
import string
import json
from os import path
from shutil import copyfile

CONFIG = None
CONFIG_VERSION = "1.0"  # Update this as changes to default config.json are made

def gen_address():
    vals = string.ascii_letters + string.digits
    v = ''
    for _ in range(16):
        v += random.choice(vals)
    return v

def get_config():
    global CONFIG
    if not path.exists('config.json'):  # copy default config if file doesn't exist
        copyfile('defaults/config.json', 'config.json')

    with open('config.json', 'r') as f:
        CONFIG = json.loads(f.read())
        if CONFIG['.version'] != CONFIG_VERSION:  # exit if config version mismatch
            print('NO CONFIG VERSION')
            exit(1)
        # check config still has default values
        if CONFIG['token'] == 'YOUR BOT TOKEN' or\
                CONFIG['chat-channel-id'] == 1234567890 or\
                CONFIG['tree-channel-id'] == 1234567890:  # exit if default values remain
            print('CHANGE VALUES IN config.json')
            exit(1)
