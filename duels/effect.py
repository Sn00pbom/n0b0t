

class Effect(object):
    def __init__(self):
        super().__init__()

        self.id = 0

        # Handler definitions
        self.on_turn_start = lambda: None
        self.on_turn_end = lambda: None
        self.on_heal = lambda: None
        self.on_act = lambda: None
        self.on_deal_damage = lambda: None
        self.on_take_damage = lambda: None
        self.on_attack = lambda: None
        self.on_spawn = lambda: None
        self.on_death = lambda: None
