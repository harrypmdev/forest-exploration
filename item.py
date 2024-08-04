from effect import Effect

class Item:

    def __init__(self, name, description, durability = 1):
        self.name = name
        self.description = description
        self.durability = durability

    def affect_durability(self, user, value):
        self.durability += value
        if self.durability <= 0:
            user.inventory.remove(self)

class HealthItem(Item):

    def __init__(self, name, description, health_effect, durability = 1):
        super().__init__(name, description, durability)
        self.health_effect = health_effect

    def use(self, user, target):
        effect = Effect(f"you used {self.name}", self.health_effect)
        if target.affect_health(effect):
            user.score += 10
        self.affect_durability(user, -1)
