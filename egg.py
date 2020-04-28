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


if __name__ == "__main__":
    egg = Egg()
    egg.add_instr('MOV', 'ax', Byte(0xec))
    egg.add_instr('NOT', 'ax')
    egg.add_instr('MOV', 'bx', Byte(0x23))
    egg.add_instr('AND', 'bx', 'ax')
    egg.add_instr('ADD', 'cx', 'bx')
    egg.add_instr('ADD', 'cx', 'ax')
    egg.add_instr('SUB', 'ax', Byte(0x2))
    env = egg.get_env()
    print(env.ax, env.bx, env.cx, env.dx)
    while not env.done:
        env.step()
        print(env.ax, env.bx, env.cx, env.dx)

