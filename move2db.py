"""
Use this tool to move old json database to sql database
Run init before running port
Use print to check if the port was successfull
"""
import sqlite3
import json
from sys import argv

def print_all():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    print(c.fetchall())


def port():
    with open('wallets.json', 'r') as f:
        user_js = json.loads(f.read())

    user_js = {int(k):v for k, v in user_js.items()}

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    for k, v in user_js.items():
        c.execute('INSERT INTO users VALUES({}, \'\', {})'.format(k, v))

    conn.commit()

    print_all()


def init():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INT PRIMARY KEY, pwd TEXT, money INT)')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    if len(argv) >= 2:
        cmd = argv[1]
        if cmd == 'init':
            init()
        elif cmd == 'port':
            port()
        elif cmd == 'print':
            print_all()
    else:
        print('move2db.py init|port|print')
