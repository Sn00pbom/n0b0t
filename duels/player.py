import random


class Player(object):

    def __init__(self):
        self.hp_max = 100
        self.hp = 100
        self.mp = 100
        self.moves = []
        self.hit_chance_mod = 0
        self.crit_chance_mod = 0
        self.crit_dmg_mod = 1.0 

    def calc_crit(self, dmg):
        return self.crit_dmg_mod * (2 * dmg)
