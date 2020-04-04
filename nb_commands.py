import random

import discord
from discord.ext import commands

from globals import client, counsel
from memeviolation import MemeViolation


async def coinflip(context):
    await context.message.channel.send(
        "{} flipped a coin! It's {}!".format(context.message.author.mention,
                                             "heads" if random.randint(0,1) == 0 else "tails"))


@client.command(name='coinflip', pass_context=True)
async def coinflip_coinflip_alias(context): await coinflip(context)


@client.command(name='coin', pass_context=True)
async def coin_coinflip_alias(context): await coinflip(context)


@client.command(name='flip', pass_context=True)
async def flip_coinflip_alias(context): await coinflip(context)


@client.command(name='cf', pass_context=True)
async def cf_coinflip_alias(context): await coinflip(context)


@client.command(name='roll',
                pass_context=True)
async def roll_command(context):
    args = context.message.content.split(' ')
    try:
        top = int(args[1])
        assert top > 0
    except:
        top = 100

    await context.message.channel.send("{} rolls {} (1-{})".format(context.message.author.mention,
                                                                   random.randint(1, top), top))


@client.command(name='anoint',
                pass_context=True)
async def anoint_command(context):
    author = context.message.author
    message = context.message.content
    perm = False
    for role in author.roles:
        if role.name == 'pleb':
            perm = True
            pleb_role = role
            break

    args = message.split(' ')
    if perm and len(args) == 2:
        try:

            converter = commands.MemberConverter()
            member = await converter.convert(context, args[1])

            async def make_pleb():
                await member.add_roles(pleb_role)

            message = message.replace('!', '')  # for some reason user @ themselves adds !
            counsel.try_vote_act(message, make_pleb, 'anoint')
            await counsel.query(message, author, 'anoint', context.message.channel)

        except:
            print('invalid user')

    else:
        print('invalid anoint"{}"'.format(message))


@client.command(name='mum',
                pass_context=True)
async def mum_command(context):
    response = [
        " you're mum gey HA",
        " Thine mother art a delectable, fine woman and a scholar, good sir."
    ]
    await context.message.channel.send(context.message.author.mention + random.choice(response))

@client.command(name='n0b0t',
                pass_context=True)
async def nobot_command(context):
    await context.message.channel.send(':robot: I AM __n0b0t__ HEAR ME REE :robot:')


@client.command(name='stop',
                pass_context=True)
async def stop_command(context):
    await context.voice_client.disconnect()


@client.command(name='rage',
                pass_context=True)
async def rage_command(context):
    user = context.message.author
    if user.voice:
        voice_channel = user.voice.channel
        # await context.message.channel.send(channel)

        if context.voice_client is None:
            await voice_channel.connect()
        elif context.voice_client.channel != voice_channel:
            await context.voice_client.disconnect()
            await voice_channel.connect()

        source = discord.FFmpegPCMAudio(source='./assets/soletmegetthisstraight.wav')
        context.voice_client.play(source, after=lambda e: print('Finished Audio'))
    else:
        await context.message.channel.send(context.message.author.mention + " haHA u wis u had musicks :japanese_goblin:")


@client.command(name='memeviolation',
                pass_context=True)
async def memeviolation_command(context):
    sender = context.message.author
    msg = context.message.content
    args = msg.split(' ')
    args.pop(0)
    if len(args) >= 2:
        target = args.pop(0)
        code = args.pop(0)
        try:
            code = int(code)
            code = list(str(code))
            code = [int(v) for v in code]
        except ValueError as e:
            print(e)
            return

        other_text = ' '.join(args)
        mv = MemeViolation(code, sender, other_text=other_text)
        img = mv.generate()
        # img_bytes = io.BytesIO()
        img.save('pil_text.png')
        # img_bytes = img_bytes.getvalue()
        # pic = discord.File(img_bytes)
        pic = discord.File('pil_text.png')
        await context.message.channel.send(file=pic)

    else:
        return



    # change user context

    # send prompt

    # get user response

    # generate meme violation
    # send meme violation in chat and personal message to offendee
