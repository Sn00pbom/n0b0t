import json

from discord import Game

import globals  # register first

from globals import client, CONFIG
import nb_commands

if __name__ == '__main__':
    @client.event
    async def on_ready():
        await client.change_presence(activity=Game(CONFIG['activity']))


    print('Starting n0b0t...')

    token = CONFIG['token']
    client.run(token)

