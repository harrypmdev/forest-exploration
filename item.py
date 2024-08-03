from effect import Effect

class Item:

    def __init__(self, name, description):
        self.name = name
        self.description = description

class HealthItem(Item):

    def __init__(self, name, description, health_effect):
        super().__init__(name, description)
        self.health_effect = health_effect

    def use(self, target):
        effect = Effect(f"you used {self.name}", self.health_effect)
        target.affect_health(effect)