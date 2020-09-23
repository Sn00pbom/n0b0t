import json

from discord import Game

import globals  # register first

from globals import client, CONFIG
import nb_commands

if __name__ == '__main__':
    @client.event
    async def on_ready():
        await client.change_presence(activity=Game(CONFIG['activity']))

        # Scrub dead links on start
        channel = client.get_channel(CONFIG['tree-channel-id'])
        async for message in channel.history(limit=1000):
            if message.author == client.user:
                await message.delete()


    print('Starting n0b0t...')

    token = CONFIG['token']
    client.run(token)

