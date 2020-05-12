

class Effect(object):
    def __init__(self):
        super().__init__()

        self.id = -1 

        # Handler definitions
        self.on_turn_start = lambda *args: None
        self.on_turn_end = lambda *args: None
        self.on_heal = lambda *args: None
        self.on_act = lambda *args: None
        self.on_deal_damage = lambda *args: None
        self.on_take_damage = lambda *args: None
        self.on_attack = lambda *args: None
        self.on_spawn = lambda *args: None
        self.on_death = lambda *args: None
