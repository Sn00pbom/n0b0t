import sqlite3

class UserDB(object):
    """Singleton class to do SQL database transactions"""
    DEFAULTS = "{}, '', 0"
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()

    def add_user(self, uid):
        try:
            defaults = self.DEFAULTS.format(uid)  # id with no pw and no money
            self.c.execute("INSERT INTO users VALUES({})".format(defaults))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('User {} already in database'.format(uid))

    def has_user(self, uid):
        self.c.execute('SELECT * FROM users WHERE id={}'.format(uid))
        return len(self.c.fetchall())

    def do_transaction(self, uid, amount, succ=lambda: None, fail=lambda: None):
        """
        Modify a user's money value by amount (+/-)
        Checks if user has sufficient funds if amount is negative

        Parameters:
        uid (int/str): User's id
        amount (int): Amount to modify user's value by
        succ (fun): Success callback function
        fail (fun): Failure callback function

        Returns:
        success (bool)
        """

        if not self.has_user(uid):
            fail()
            self.add_user(uid)
            return False

        self.c.execute('SELECT money FROM users WHERE id={}'.format(uid))
        money = self.c.fetchone()[0]

        if amount < 0 and money < abs(amount):  # Negative amount case with insuff funds
            fail()
            return False
        
        self.c.execute('UPDATE users SET money={} WHERE id={}'.format(money + amount, uid))
        succ()
        return True

    def print(self):
        """Debugging print"""
        self.c.execute('SELECT * FROM users')
        print(self.c.fetchall())

        

