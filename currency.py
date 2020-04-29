import asyncio
import random
import datetime

import util


class CurrencyManager(object):
    CURRENCY_SYMBOl = '₪'
    CH_ID = 699673275986608228

    def __init__(self, client):
        self.client = client
        self.posts = {}
        self.wallets = {}

    def check_user(self, uid):
        uid = str(uid)
        if uid not in self.wallets.keys():
            self.wallets[uid] = 0
            return False
        return True

    def user_has_value(self, uid, amount):
        if not self.check_user(uid): return False
        uid = str(uid)
        return self.wallets[uid] >= amount

    async def post_shekel(self):
        channel = self.client.get_channel(self.CH_ID)
        quantity = random.randint(5, 10)
        address = util.gen_address()
        msg_handle = await channel.send('Shekels dropped! {}{} @ {}'.format(self.CURRENCY_SYMBOl, quantity, address))
        self.posts[address] = (quantity, msg_handle)
        with open('money_log.txt', 'a') as f:
            f.write('[POST] {} -> {}, {}\n'.format(datetime.datetime.now(), quantity, address))

    async def claim_shekel(self, user_id, shekel_id, claim_msg):
        try:
            quantity, msg_handle = self.posts[shekel_id]
            del self.posts[shekel_id]
            if not user_id in self.wallets.keys():
                self.wallets[user_id] = 0
            self.wallets[user_id] += quantity
            await msg_handle.delete()
            await claim_msg.delete()
            with open('money_log.txt', 'a') as f:
                f.write('[CLAIM] {} -> {}, {}, {}\n'.format(datetime.datetime.now(), user_id, quantity, shekel_id))

        except:
            return


class MineTimer(object):
    def __init__(self, curr_man):
        self._curr_man = curr_man
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while True:
            await asyncio.sleep(random.randint(20, 45) * 60)
            await self._curr_man.post_shekel()

    def cancel(self):
        self._task.cancel()
