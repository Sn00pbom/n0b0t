import random


class Player(object):
    def __init__(self):
        # Attributes
        self._actions = 0
        self._hp = 100
        self._hp_max = 100
        self._mp = 100
        self._mp_max = 100
        self._mp_regen = 10  # amount of mp gained back during regen
        self._speed = 100  # used in determining turn order at beginning of round
        self._crit_chance = 0.0
        self._crit_dmg = 1.0  # crits deal 100% more damage at base
        self._cost_reduction_flat = 0
        self._cost_reduction_percent = 0.0
        self._melee_chance = 0.5
        self._range_chance = 0.5
        self._magic_dmg_reduction_flat = 0
        self._magic_dmg_reduction_percent = 0.0
        self._physical_dmg_reduction_flat = 0
        self._physical_dmg_reduction_percent = 0.0

        # Mechanics
        self.effects = []
        self.modifiers = []
        self.actives = []

    #
    # Begin Property Functions (Modifiers)
    # The paradigm is that all changes to the initial stats are stored as modifiers.
    # This includes even changes to HP, MP etc.
    #
    def _apply_mods(self, k):
        o = self.__dict__[k]
        for mod in self.modifiers:
            o += mod.__dict__[k]
        return o

    @property
    def actions(self): return self._apply_mods('_actions')

    @property
    def hp(self): return self._apply_mods('_hp')

    @property
    def hp_max(self): return self._apply_mods('_hp_max')

    @property
    def mp(self): return self._apply_mods('_mp')
   
    @property
    def mp_max(self): return self._apply_mods('_mp_max')
   
    @property
    def mp_regen(self): return self._apply_mods('_mp_regen')
   
    @property
    def speed(self): return self._apply_mods('_speed')
   
    @property
    def crit_chance(self): return self._apply_mods('_crit_chance')
   
    @property
    def crit_dmg(self): return self._apply_mods('_crit_dmg')
   
    @property
    def cost_reduction_flat(self): return self._apply_mods('_cost_reduction_flat')
   
    @property
    def cost_reduction_percent(self): return self._apply_mods('_cost_reduction_percent')
   
    @property
    def melee_dmg_reduction_flat(self): return self._apply_mods('_melee_dmg_reduction_flat')
   
    @property
    def melee_dmg_reduction_percent(self): return self._apply_mods('_melee_dmg_reduction_percent')
   
    @property
    def magic_dmg_reduction_flat(self): return self._apply_mods('_magic_dmg_reduction_percent')
   
    @property
    def magic_dmg_reduction_percent(self): return self._apply_mods('_magic_dmg_reduction_percent')

    #
    # End Property Functions
    #

    #
    # Begin Event Functions (Effects)
    #
    def do_turn_start(self, context):
        pass

    def do_turn_end(self, context):
        pass

    def do_act(self, context):
        pass

    def do_spawn(self, context):
        pass

    def do_death(self, context):
        pass

    def do_heal(self, context):
        pass

    def do_attack(self, context):
        pass

    def do_deal_dmg(self, context):
        pass

    def do_take_dmg(self, context):
        pass

    def do_regen_mp(self, context):
        pass

    def do_forget_active(self, context):
        pass

    #
    # End Event Functions
    #