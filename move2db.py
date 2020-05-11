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

def port2():
    """Move second table to new table with empty hash and salt instead of plaintext pwd"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('CREATE TABLE t (id INT PRIMARY KEY, hash TEXT, salt TEXT, money INT)')
    except:
        pass
    c.execute('SELECT * FROM users')
    for vals in c.fetchall():
        c.execute('INSERT INTO t VALUES({},"","",{})'.format(vals[0], vals[2]))
    c.execute('DROP TABLE users')
    c.execute('ALTER TABLE t RENAME TO users')
    c.execute('SELECT * FROM users')
    print(c.fetchall())
    conn.commit()


def init():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE users (id INT PRIMARY KEY, hash TEXT, salt TEXT, money INT)')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    if len(argv) >= 2:
        cmd = argv[1]
        if cmd == 'init':
            init()
        elif cmd == 'port':
            port()
        elif cmd == 'port2':
            port2()
        elif cmd == 'print':
            print_all()
    else:
        print('move2db.py init|port|print')
