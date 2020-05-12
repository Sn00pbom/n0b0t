import random


class Player(object):
    def __init__(self):
        # Attributes
        self.hp = 100
        self.hp_max = 100
        self.mp = 100
        self.mp_max = 100
        self.mp_regen = 10  # amount of mp gained back during regen
        self.speed = 100  # used in determining turn order at beginning of round
        self.crit_chance = 0.0
        self.crit_dmg = 1.0  # crits deal 100% more damage at base
        self.cost_reduction_flat = 0
        self.cost_reduction_percent = 0.0
        self.melee_chance = .5
        self.range_chance = .5
        self.magic_dmg_reduction_flat = 0
        self.magic_dmg_reduction_percent = 0.0
        self.physical_dmg_reduction_flat = 0
        self.physical_dmg_reduction_percent = 0.0

        # Mechanics
        self.effects = []
        self.modifiers = []
        self.actives = []
