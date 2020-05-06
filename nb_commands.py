import random
import re
from io import BytesIO

import discord
from discord.ext import commands

from globals import client, counsel, curr_man, userdb
from memeviolation import MemeViolation


async def insufficient_funds(context):
    await context.message.channel.send("{} is once again asking for your financial support. (insufficient funds)"
                                       .format(context.message.author.mention))


@client.command(name='pwd', pass_context=True)
async def pwd_command(context):
    channel = context.message.channel
    args = context.message.content.split(' ')
    args.pop(0)

    async def usg():
        await channel.send('Usage: .pwd [get|set] PWD\n(Must be in a DM!)')

    if not isinstance(channel, discord.DMChannel):
        await usg()
        return

    if len(args):
        cmd = args.pop(0)
        uid = context.message.author.id
        if cmd == 'get':
            p = userdb.get_user_value(uid, 'pwd')
            if p != '':
                await channel.send('Current password: {}'.format(p))
            else:
                await channel.send('No password set!')

        elif cmd == 'set':
            if not len(args):
                await usg()
                return
            userdb.set_user_value(uid, 'pwd', args.pop(0))
            await channel.send('Password set!')
        else:
            await usg()
    else:
        await usg()
        return


@client.command(name='anonymize', pass_context=True, aliases=['anon', 'mail'])
async def anonymize_command(context):
    ANON_COST = 2
    author = context.author
    args = context.message.content.split(' ')
    try:
        assert len(args) >= 3
        converter = commands.MemberConverter()
        recipient = await converter.convert(context, args[1])
    except:
        await context.message.channel.send('Usage: .anonymize @RECIPIENT *MSG')
        return

    async def send_msg():
        usr_msg = "Received anon message!\n```\n{}\n```".format(' '.join(args[2::]))
        rec_dm = await recipient.create_dm()
        await rec_dm.send(usr_msg)
        auth_dm = await author.create_dm()
        await context.message.delete()
        await auth_dm.send("Message Sent to {}! Thank you for your business!".format(recipient.mention))
    
    await curr_man.do_transaction(author.id, -ANON_COST, succ=send_msg, fail=lambda: insufficient_funds(context))


@client.command(name='paytable', pass_context=True)
async def paytable_command(context):
    await context.message.channel.send(file=discord.File('assets/paytable.png'))


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

    async def do_spin():
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

        await curr_man.do_transaction(author.id, o)  # add money to user
        await context.message.channel.send(frmts.format(
            wheel_vals(w1), wheel_vals(w2), wheel_vals(w3), payfs
        ))

    await curr_man.do_transaction(author.id, -SPIN_COST, succ=do_spin, fail=lambda: insufficient_funds(context))


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
    
    async def pay_target():
        await curr_man.do_transaction(target_user.id, amount)
        for _ in range(3): args.pop(0)
        reason_msg = ' for "{}"'.format(' '.join(args)) if len(args) != 0 else '!'
        await context.message.channel.send("{} paid {} {}{}{}".format(
            author.mention, target_user.mention, curr_man.CURRENCY_SYMBOl, amount, reason_msg))

    await curr_man.do_transaction(author.id, -amount,
        succ=pay_target,
        fail=lambda: insufficient_funds(context))


@client.command(name='buypin', pass_context=True)
async def buypin_command(context):
    author = context.message.author
    args = context.message.content.split(' ')
    if len(args) == 1:
        await context.message.channel.send('Usage: .buypin [MESSAGE]')
        return
    COST = 10
    async def do_pin():
        pin_content = context.message.content[context.message.content.find(' '):len(context.message.content)] + "\n -" + author.mention
        msg = await context.message.channel.send(pin_content)
        await msg.pin()

    await curr_man.do_transaction(author.id, -COST, succ=do_pin, fail=lambda: insufficient_funds(context))
        

@client.command(name='buypinremoval', pass_context=True)
async def buypinremoval_command(context):
    author = context.message.author
    argv = context.message.content.split(' ')
    if len(argv) == 1:
        await context.message.channel.send('Usage: .buypinremoval [MESSAGE ID]')
        return
    
    pat = re.compile(r'.*/(\d+)')
    r = pat.findall(argv[1])
    try:
        rid = r[0]
    except:
        rid = argv[1]
    
    COST = 15 #arbitrary. i dont know how much this should cost
    
    try:
        msg = await context.message.channel.fetch_message(rid)
        async def do_rmpin():
            await msg.unpin()
            await context.message.channel.send("{} paid to remove pin: ".format(author.name)) 
            await context.message.channel.send(">>> {}".format(msg.content)) 

        await curr_man.do_transaction(author.id, -COST, succ=do_rmpin, fail=lambda: insufficient_funds(context))

    except:
        await context.message.channel.send('Usage: .buypinremoval [MESSAGE ID]')
    
        
 #--------------------------------------------
#experimental. lets see where this goes...
@client.command(name='revolutionary', pass_context=True)
async def revolutionary_command(context):
    return
    author = context.message.author
    args = context.message.content.split(' ')
    
    if len(args) == 1:
        await context.message.channel.send('Usage : .revolutionary [1/0 become revolutionary yes/no]')
        return
    
    try:
        rev_status = int(args[1])
        if rev_status < 1:
                rev_status = 0
                await context.message.channel.send('{} has betrayed the worker\'s of the server & turned his back on the revolution.'.format(author.name))
        else:
                rev_status = 1
                await context.message.channel.send('{} has joined the revolution & given up their tokens to fight for the proletariat!'.format(author.name))
        
        curr_man.revolutionary_status[str(author.id)] = rev_status
    except:
        await context.message.channel.send('Usage : .revolutionary [1/0 become revolutionary yes/no]')
        return
#--------------------------------------------


@client.command(name='balance', pass_context=True, aliases = ['wallet', 'bal', 'money'])
async def balance_command(context):
    author = context.message.author
    channel = await author.create_dm()
    quantity = curr_man.get_money(author.id)
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
        await curr_man.claim_shekel(author.id, mid, context.message)


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
    async def post_help():
        m = """```
1: Madding Too Fast
2: Louding Too Fast
3: Background Shit
4: Gay Porn Too Gay
5: Unironic XD
6: Rapid Head Expansion
7: Global Elite Syndrome
8: Spoilers
9: Unidentified Sucking Noises
0: Other: *MSG

Example Usage:
    .memeviolation @targetsName 1
    .memeviolation @targetsName 2345
    .memeviolation @targetsName 0 *MSG```
        """
        await context.message.channel.send(m)

    if len(args) >= 2:
        target = args.pop(0)
        code = args.pop(0)
        try:
            code = int(code)
            code = list(str(code))
            code = [int(v) for v in code]
            converter = commands.MemberConverter()
            target = await converter.convert(context, target)
        except ValueError:
            await post_help()
            return

        async def send_mv():
            PENALTY = 15
            other_text = ' '.join(args)
            mv = MemeViolation(code, sender, other_text=other_text)
            img = mv.generate()
            with BytesIO() as img_bin:
                img.save(img_bin, 'PNG')
                img_bin.seek(0)
                await context.message.channel.send(":rotating_light: MEME VIOLATION :rotating_light:\nIssued to -> {}! penalized {}{}".format(target.mention, curr_man.CURRENCY_SYMBOl, PENALTY),
                                                    file=discord.File(fp=img_bin, filename='mv.png'))
            await curr_man.do_transaction(target.id, -PENALTY)

        counsel.try_vote_act(msg, send_mv, 'memeviolation')
        await counsel.query(msg, sender, 'memeviolation', context.message.channel)
    else:
        await post_help()
