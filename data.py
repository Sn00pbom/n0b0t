import sqlite3
import hashlib

import util


class UserDB(object):
    """Singleton class to do SQL database transactions"""
    DEFAULTS = "{}, '', '', 0"  # id, hash, salt, money
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

    def get_user_data(self, uid):
        if self.has_user(uid):
            self.c.execute('SELECT * FROM users WHERE id={}'.format(uid))
            return self.c.fetchone()
        else:
            self.add_user(uid)
            return 0

    def get_user_value(self, uid, field):
        if self.has_user(uid):
            self.c.execute('SELECT {} FROM users WHERE id={}'.format(field, uid))
            return self.c.fetchone()[0]
        else:
            self.add_user(uid)
            return 0

    def set_user_value(self, uid, field, value):
        if not self.has_user(uid): self.add_user(uid)
        command = 'UPDATE users SET {} = "{}" WHERE id={}'.format(field, value, uid)
        self.c.execute(command)
        self.conn.commit()

    def set_user_pwd(self, uid, pwd):
        salt = util.gen_address()
        self.set_user_value(uid, 'salt', salt)
        h = self._compute_user_hash(uid, pwd)
        self.set_user_value(uid, 'hash', h)

    def check_user_pwd(self, uid, pwd):
        h = self._compute_user_hash(uid, pwd)
        saved = self.get_user_value(uid, 'hash')
        return h == saved

    def _compute_user_hash(self, uid, pwd) -> str:
        salt = self.get_user_value(uid, 'salt')
        v = '{}{}'.format(pwd, salt).encode('utf-8')
        h_func = hashlib.sha256()
        h_func.update(v)
        h = h_func.hexdigest()
        return h

    def print(self):
        """Debugging print"""
        self.c.execute('SELECT * FROM users')
        print(self.c.fetchall())

