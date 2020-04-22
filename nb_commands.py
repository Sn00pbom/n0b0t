import random
import re

import discord
from discord.ext import commands

from globals import client, counsel, curr_man
from memeviolation import MemeViolation


async def insufficient_funds(context):
    await context.message.channel.send("{} is once again asking for your financial support. (insufficient funds)"
                                       .format(context.message.author.mention))

@client.command(name='paytable', pass_context=True)
async def paytable_command(context):
    author = context.message.author
    dm_ch = await author.create_dm()
    await dm_ch.send(file=discord.File('assets/paytable.png'))
    await context.message.delete()

@client.command(name='spin', pass_context=True)
async def spin_command(context):
    author = context.message.author
    args = context.message.content.split(' ')
    if len(args) > 1:
        try:
            SPIN_COST = int(args[1])
            assert 0 < SPIN_COST <=3
        except:
            return
        
    else:
        SPIN_COST = 1

    # check author wallet and remove cost
    if not curr_man.user_has_value(author.id, SPIN_COST):
        await insufficient_funds(context)
        return
    else:
        curr_man.wallets[str(author.id)] -= SPIN_COST

    pay_1 = [4000, 100, 75, 30, 20, 10, 5, 2]
    pay_2 = [8000, 200, 150, 60, 40, 20, 10, 4]
    pay_3 = [12000, 300, 255, 90, 60, 30, 15, 6]
    pay = [pay_1, pay_2, pay_3][SPIN_COST-1]

    # tier 1 is 0
    tier2 = range(1, 3)
    tier3 = range(3, 6)
    tier4 = range(6, 10)
    tier5 = range(10, 15)
    tier6 = range(15, 22)

    def wheel_vals(i):
        vals = [
            ':peach:',
            ':japanese_goblin:',
            ':watermelon:',
            ':eggplant:',
            ':pick:',
            ':poo:',
            ':middle_finger:'
            # ':teddy_bear:',
            # ':earth_americas:',
            # ':moyai:',
            # ':man_mage:'
        ]
        if i is 0: pass
        elif i in tier2: i = 1
        elif i in tier3: i = 2
        elif i in tier4: i = 3
        elif i in tier5: i = 4
        elif i in tier6: i = 5
        else: i = 6
        return vals[i]

    N_VALUES = 50
    # wheel outcome values
    w1 = random.choice(range(N_VALUES))
    w2 = random.choice(range(N_VALUES))
    w3 = random.choice(range(N_VALUES))
    frmts = ''
    if w1 is 0 and w2 is 0 and w3 is 0:  # jackpot case (tier 1)
        frmts += ':rotating_light: ' \
                 ':regional_indicator_j: :regional_indicator_a: :regional_indicator_c: :regional_indicator_k:' \
                 ':b: :regional_indicator_o: :regional_indicator_t:' \
                 ' :rotating_light: @everyone\n'
        o = pay[0]
    elif w1 in tier2 and w2 in tier2 and w3 in tier2:
        o = pay[1]
    elif w1 in tier3 and w2 in tier3 and w3 in tier3:
        o = pay[2]
    elif w1 in tier4 and w2 in tier4 and w3 in tier4:
        o = pay[3]
    elif w1 in tier5 and w2 in tier5 and w3 in tier5:
        o = pay[4]
    elif w1 in tier6 and w2 in tier6 and w3 in tier6:
        o = pay[5]
    elif (w1 in tier6 and w2 in tier6) or (w2 in tier6 and w3 in tier6) or (w1 in tier6 and w3 in tier6):
        o = pay[6]
    elif w1 in tier6 or w2 in tier6 or w3 in tier6:
        o = pay[7]
    else:
        o = 0

    if o is 0:
        payfs = 'Better luck next time!'
    else:
        payfs = '→ Paying {} {}{}'.format(author.mention, curr_man.CURRENCY_SYMBOl, o)

    frmts += '╔══════════╗\n║ {} ║ {} ║ {}  ║ {}\n╚══════════╝'

    curr_man.wallets[str(author.id)] += o
    await context.message.channel.send(frmts.format(
        wheel_vals(w1), wheel_vals(w2), wheel_vals(w3), payfs
    ))


@client.command(name='pay', pass_context=True)
async def pay_command(context):
    author = context.message.author
    args = context.message.content.split(' ')
    # check inputs
    try:
        amount = int(args[2])
        assert amount > 0
        converter = commands.MemberConverter()
        target_user = await converter.convert(context, args[1])
    except:
        return

    curr_man.check_user(author.id)
    curr_man.check_user(target_user.id)
    if curr_man.user_has_value(author.id, amount):
        curr_man.wallets[str(target_user.id)] += amount
        curr_man.wallets[str(author.id)] -= amount
        await context.message.channel.send("{} paid {} {}{}!".format(
            author.mention, target_user.mention, curr_man.CURRENCY_SYMBOl, amount))
    else:
        await insufficient_funds(context)


@client.command(name='balance', pass_context=True, aliases = ['wallet'])
async def balance_command(context):
    author = context.message.author
    channel = await author.create_dm()
    try:
        quantity = curr_man.wallets[str(author.id)]
    except:
        quantity = 0
    await channel.send("Your wallet contains: " + curr_man.CURRENCY_SYMBOl + str(quantity))
    await context.message.delete()


@client.command(name='claim', pass_context=True)
async def claim_command(context):
    msg = context.message.content
    p = re.compile(r'([a-zA-Z0-9]+)')
    matches = p.findall(msg)

    if(len(matches) == 2):
        author = context.message.author
        mid = matches[1]
        await curr_man.claim_shekel(str(author.id), mid, context.message)


@client.command(name='coinflip', pass_context=True, aliases=['coin', 'flip', 'cf'])
async def coinflip_coinflip_alias(context):
    await context.message.channel.send(
        "{} flipped a coin! It's {}!".format(context.message.author.mention,
                                             "heads" if random.randint(0,1) == 0 else "tails"))


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


@client.command(name='delete',
                pass_context=True)
async def delete_command(context):
    author = context.message.author
    message = context.message.content
    argv = message.split(' ')
    if len(argv) >= 2:
        # parse id from link
        pat = re.compile(r'.*/(\d+)')
        r = pat.findall(argv[1])
        try:
            rid = r[0]
        except:
            rid = argv[1]

        async def remove_msg():
            try:
                msg = await context.message.channel.fetch_message(rid)
                await msg.delete()
            except:
                print('invalid message')
        message = "{} {}".format(argv[0], rid)
        counsel.try_vote_act(message, remove_msg, 'delete')
        await counsel.query(message, author, 'delete', context.message.channel)
        

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
