import sqlite3
import inspect


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
        self.c.execute('UPDATE users SET {}={} WHERE id={}'.format(field, value, uid))
        self.conn.commit()
