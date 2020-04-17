import json
from discord import Game
from globals import client, curr_man
import nb_commands

if __name__ == '__main__':
    @client.event
    async def on_ready():
        await client.change_presence(activity=Game('a pirated copy of Minecraft'))


    print('Starting n0b0t...')

    with open('wallets.json', 'r') as f:
        curr_man.wallets = json.loads(f.read())

    with open('token.txt', 'r') as f:
        try:
            client.run(f.read())
        finally:
            with open('wallets.json', 'w') as f:
                f.write(json.dumps(curr_man.wallets, indent=4))


