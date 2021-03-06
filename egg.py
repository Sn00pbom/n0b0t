import random

import util
#
#  Crack the Egg
#

class Byte(object):
    def __init__(self, v=0x00):
        self._v = v & 0xff  # mask to 1 byte

    def __bool__(self):
        return self._v != 0x00

    def __str__(self):
        return "0x%0.2x" % self._v

    def __int__(self):
        return self._v

    def __add__(self, b):
        b = Byte(b) if not isinstance(b, Byte) else b
        return Byte(self._v + b._v)

    def __sub__(self, b):
        b = Byte(b) if not isinstance(b, Byte) else b
        return Byte(self._v - b._v)

    def __mul__(self, b):
        b = Byte(b) if not isinstance(b, Byte) else b
        return Byte(self._v * b._v)

    def __and__(self, b):
        b = Byte(b) if not isinstance(b, Byte) else b
        return Byte(self._v & b._v)

    def __or__(self, b):
        b = Byte(b) if not isinstance(b, Byte) else b
        return Byte(self._v | b._v)

    def __xor__(self, b):
        b = Byte(b) if not isinstance(b, Byte) else b
        return Byte(self._v ^ b._v)

    def __invert__(self):
        return Byte(~ self._v)

    def __eq__(self, b):
        if isinstance(b, int):
            return self._v == b
        elif isinstance(b, Byte):
            return self._v == b._v
        else:
            return False


class Egg(object):
    def __init__(self):
        self.instr = []

    def add_instr(self, instr_s, *args):
        self.instr.append((instr_s, args))

    def get_env(self):
        return EggEnv(self.instr)

    def ADD(self, a, b):
        self.__dict__[a] += b if isinstance(b, Byte) else self.__dict__[b]

    def SUB(self, a, b):
        self.__dict__[a] -= b if isinstance(b, Byte) else self.__dict__[b]

    def AND(self, a, b):
        self.__dict__[a] &= b if isinstance(b, Byte) else self.__dict__[b]

    def OR(self, a, b):
        self.__dict__[a] |= b if isinstance(b, Byte) else self.__dict__[b]

    def XOR(self, a, b):
        self.__dict__[a] ^= b if isinstance(b, Byte) else self.__dict__[b]

    def NOT(self, a):
        self.__dict__[a] = ~self.__dict__[a]

    def MOV(self, a, b):
        self.__dict__[a] = b if isinstance(b, Byte) else self.__dict__[b]

    def CMP(self, a, b):
        # TODO fix implement
        t = self.__dict__[a] - self.__dict__[b]
        t &= 0x80
        if t:
            self.sf = 1
            self.zf = 0
        else:
            self.sf = 0
            self.zf = 0


class EggEnv(Egg):
    def __init__(self, instr):
        self.instr = instr  # instruction list
        self.ax = Byte()  # ax register
        self.bx = Byte()  # bx register
        self.cx = Byte()  # cx register
        self.dx = Byte()  # dx register
        self.sf = Byte()  # sign flag
        self.zf = Byte()  # zero flag
        self.ip = 0  # instruction pointer
        self.done = False

    def step(self):
        sinstr, sargs = self.instr[self.ip]
        instr = getattr(self, sinstr)

        if len(sargs) is 1:
            args = sargs
        else:
            arg1, arg2 = sargs
            args = [arg1, self.__dict__[arg2] if not isinstance(arg2, Byte) else arg2]

        instr(*args)

        self.ip += 1
        self.done = self.ip >= len(self.instr)

    def run(self):
        while not self.done:
            self.step()


class EggBuilder(object):
    REGS = [
        'ax',
        'bx',
        'cx',
        'dx',
    ]

    def __init__(self, egg=None):
        self.egg = egg if egg else Egg()

    def build_rand_line(self, n=1):
        for _ in range(n):
            f = random.choice(EggBuilder.BUILDER_FUNCS())
            self.egg.add_instr(*f())

    @staticmethod
    def BUILDER_FUNCS():
        return [
            EggBuilder.build_ADD,
            EggBuilder.build_SUB,
            EggBuilder.build_AND,
            EggBuilder.build_OR,
            EggBuilder.build_XOR,
            EggBuilder.build_ADD,
            EggBuilder.build_NOT,
            EggBuilder.build_MOV,
        ]

    @staticmethod
    def rand_source():
        if random.randint(0, 1):
            return random.choice(EggBuilder.REGS)
        else:
            return Byte(random.randint(0, 255))

    @staticmethod
    def build_ADD():
        dest = random.choice(EggBuilder.REGS)
        source = EggBuilder.rand_source()
        return 'ADD', dest, source
        
    @staticmethod
    def build_SUB():
        dest = random.choice(EggBuilder.REGS)
        source = EggBuilder.rand_source()
        return 'SUB', dest, source

    @staticmethod
    def build_AND():
        dest = random.choice(EggBuilder.REGS)
        source = EggBuilder.rand_source()
        return 'AND', dest, source
    
    @staticmethod
    def build_OR():
        dest = random.choice(EggBuilder.REGS)
        source = EggBuilder.rand_source()
        return 'OR', dest, source

    @staticmethod
    def build_XOR():
        dest = random.choice(EggBuilder.REGS)
        source = EggBuilder.rand_source()
        return 'XOR', dest, source

    @staticmethod
    def build_NOT():
        dest = random.choice(EggBuilder.REGS)
        return 'NOT', dest

    @staticmethod
    def build_MOV():
        dest = random.choice(EggBuilder.REGS)
        source = EggBuilder.rand_source()
        return 'MOV', dest, source


class EggManager(object):
    """Singleton global object to keep track of active eggs and their attempts"""
    
    def __init__(self):
        self.eggs = {}

    def has_id(self, egg_id):
        return egg_id in self.eggs.keys()

    def check_soln(self, egg_id, regs):
        if not self.has_id(egg_id): return

        egg = self.eggs[egg_id][1]
        for i in range(len(regs)):  # cast all regs strings to int
            r = regs[i]
            if r.startswith('0x'):  # check if hex string
                regs[i] = int(r, 0)
            else:
                regs[i] = int(r)

        env = egg.get_env()
        env.ax = Byte(regs[0])
        env.bx = Byte(regs[1])
        env.cx = Byte(regs[2])
        env.dx = Byte(regs[3])
        env.run()

        results = self.eggs[egg_id][2]

        self.eggs[egg_id][0] += 1

        if env.ax == results[0] and env.bx == results[1] and env.cx == results[2] and env.dx == results[3]:
            del(self.eggs[egg_id])
            return True
        else:
            if self.eggs[egg_id][0] == 3:
                print('egg exhausted @ {}'.format(egg_id))
                del(self.eggs[egg_id])  # remove exhausted egg

            return False
        
    def _spawn(self, spawn_func, payout):
        egg = Egg()
        builder = EggBuilder(egg)

        spawn_func(builder)

        env = egg.get_env()
        env.ax = Byte(random.randint(0, 9))
        env.bx = Byte(random.randint(0, 9))
        env.cx = Byte(random.randint(0, 9))
        env.dx = Byte(random.randint(0, 9))
        env.run()
        result = [env.ax, env.bx, env.cx, env.dx]
        uid = util.gen_address()
        self.eggs[uid] = [0, egg, result, payout]  # put attempts, egg obj, results into eggs@id
        return uid

    def spawn_T0(self):
        PAYOUT = 0
        def build(builder):
            builder.build_rand_line()  # build 1 line for tutorial

        return self._spawn(build, PAYOUT)



if __name__ == "__main__":
    # Just a test

    egg_man = EggManager()
    uid = egg_man.spawn_T0()
    while not egg_man.eggs[uid][0] == 3:
        regs = str(input('enter regs:')).split(' ')
        print(egg_man.check_soln(uid, regs))


    # egg = Egg()
    # builder = EggBuilder(egg)
    
    # builder.build_rand_line()

    # for _ in range(1):
    #     env = egg.get_env()
    #     # Random initial register vals
    #     env.ax = Byte(random.randint(1, 3))
    #     env.bx = Byte(random.randint(10, 12))
    #     env.cx = Byte(random.randint(35, 38))
    #     env.dx = Byte(random.randint(-6, -3))
    #     print('initial:', env.ax, env.bx, env.cx, env.dx)
    #     while not env.done:
    #         env.step()
    #     for v in egg.instr:
    #         print(v)
    #     print('final:', env.ax, env.bx, env.cx, env.dx)


