import asyncio
import random
import datetime

import util


class CurrencyManager(object):
    CURRENCY_SYMBOl = '₪'
    CH_ID = 699673275986608228

    def __init__(self, client, userdb):
        self.client = client
        self.posts = {}
        self.userdb = userdb

    # def check_user(self, uid):
    #     """DEPRECATED - Use UserDB"""
    #     return self.userdb.has_user(uid)

    # def user_has_value(self, uid, amount):
    #     """DEPRECATED - Use UserDB"""
    #     # c = sqlite3.connect('users.db').cursor()
    #     # c.execute('SELECT money FROM users WITH id={}'.format(uid))
    #     # a = c.fetchall()
    #     # return a[0] >= amount


    #     if not self.check_user(uid): return False
    #     uid = str(uid)
    #     return self.wallets[uid] >= amount
    def get_money(self, uid):
        return self.userdb.get_user_value(uid, 'money')

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
            self.do_transaction(uid, quantity)
            await msg_handle.delete()
            await claim_msg.delete()
            with open('money_log.txt', 'a') as f:
                f.write('[CLAIM] {} -> {}, {}, {}\n'.format(datetime.datetime.now(), user_id, quantity, shekel_id))

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
        
        udb.set_user_value(uid, 'money', money + amount)
        if succ: await succ()
        return True


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
