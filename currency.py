import asyncio
import random
import string



class CurrencyManager():
    CURRENCY_SYMBOl = '₪'

    def __init__(self, client):
        self.client = client
        self.posts = {}
        self.wallets = {}

    async def post_shekel(self):
        # ch_id = 699673275986608228
        ch_id = 694325538671689799
        channel = self.client.get_channel(ch_id)
        quantity = random.randint(5, 10)
        address = gen_address()
        msg_handle = await channel.send('Shekels dropped! {}{} @ {}'.format(self.CURRENCY_SYMBOl, quantity, address))
        self.posts[address] = (quantity, msg_handle)

    async def claim_shekel(self, user_id, shekel_id, claim_msg):
        try:
            quantity, msg_handle = self.posts[shekel_id]
            del self.posts[shekel_id]
            if not user_id in self.wallets.keys():
                self.wallets[user_id] = 0
            self.wallets[user_id] += quantity
            print(user_id, '->', self.wallets[user_id], 'shekels')
            await msg_handle.delete()
            await claim_msg.delete()

        except:
            return


class MineTimer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()


async def timeout_callback():
    await asyncio.sleep(0.1)
    print('echo!')


def gen_address():
    vals = string.ascii_letters + string.digits
    v = ''
    for _ in range(16):
        v += random.choice(vals)
    return v


