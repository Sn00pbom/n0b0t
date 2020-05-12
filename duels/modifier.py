

class Modifier(object):
    def __init__(self):
        super().__init__()

        self.id = -1

        # Modifier definitions
        self._actions = 0
        self._hp = 0
        self._hp_max = 0
        self._mp = 0
        self._mp_max = 0
        self._mp_regen = 0
        self._speed = 0
        self._crit_chance = 0.0
        self._crit_dmg = 0.0
        self._cost_reduction_flat = 0
        self._cost_reduction_percent = 0.0
        self._melee_chance = 0.0
        self._range_chance = 0.0
        self._magic_dmg_reduction_flat = 0
        self._magic_dmg_reduction_percent = 0.0
        self._physical_dmg_reduction_flat = 0
        self._physical_dmg_reduction_percent = 0.0