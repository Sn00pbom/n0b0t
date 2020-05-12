import random
import string

def gen_address():
    vals = string.ascii_letters + string.digits
    v = ''
    for _ in range(16):
        v += random.choice(vals)
    return v

