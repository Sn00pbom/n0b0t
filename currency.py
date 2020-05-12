import asyncio
import random
import datetime

import util
from globals import CONFIG


class CurrencyManager(object):

    def __init__(self, client, userdb):
        self.client = client
        self.posts = {}
        self.userdb = userdb

    def get_money(self, uid):
        return self.userdb.get_user_value(uid, 'money')

    async def post_shekel(self):
        channel = self.client.get_channel(CONFIG['tree-channel-id'])
        quantity = random.randint(*CONFIG['tree-drop-value-range'])
        address = util.gen_address()
        msg_handle = await channel.send('{}s dropped! {}{} @ {}'.format(CONFIG['curr-name'],
                                                                        CONFIG['curr-symbol'],
                                                                        quantity, address))
        self.posts[address] = (quantity, msg_handle)
        with open('money_log.txt', 'a') as f:
            f.write('[POST] {} -> {}, {}\n'.format(datetime.datetime.now(), quantity, address))

    async def claim_shekel(self, uid, shekel_id, claim_msg):
        try:
            quantity, msg_handle = self.posts[shekel_id]
            del self.posts[shekel_id]
            await self.do_transaction(uid, quantity)
            await msg_handle.delete()
            await claim_msg.delete()
            with open('money_log.txt', 'a') as f:
                f.write('[CLAIM] {} -> {}, {}, {}\n'.format(datetime.datetime.now(), uid, quantity, shekel_id))

        except:
            return

    async def do_transaction(self, uid, amount, succ=None, fail=None):
        """
        Modify a user's money value by amount (+/-)
        Checks if user has sufficient funds if amount is negative

        Parameters:
        uid (int/str): User's id
        amount (int): Amount to modify user's value by
        succ (async fun): Success callback function
        fail (async fun): Failure callback function

        Returns:
        success (bool)
        """
        udb = self.userdb
        if not udb.has_user(uid):
            if fail: await fail()
            udb.add_user(uid)
            return False

        money = udb.get_user_value(uid, 'money')
        if amount < 0 and money < abs(amount):  # Negative amount case with insuff funds
            if fail: await fail()
            return False
        
        if succ: await succ()
        udb.set_user_value(uid, 'money', money + amount)
        return True


class MineTimer(object):
    def __init__(self, curr_man):
        self._curr_man = curr_man
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while True:
            await asyncio.sleep(random.randint(*CONFIG['tree-drop-time-range']) * 60)
            await self._curr_man.post_shekel()

    def cancel(self):
        self._task.cancel()
