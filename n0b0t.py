from discord import Game
from globals import client
import nb_commands

if __name__ == '__main__':
    @client.event
    async def on_ready():
        print('Started!')
        await client.change_presence(activity=Game('a pirated copy of Minecraft'))


    print('Starting n0b0t...')

    with open('token.txt', 'r') as f:
        client.run(f.read())
