from effect import Effect

class Item:

    def __init__(self, name, description, durability = 1):
        self.name = name
        self.description = description
        self.durability = durability
        self.break_message = durability > 1

    def affect_durability(self, user, value):
        self.durability += value
        if self.durability <= 0:
            user.inventory.remove(self)
            if self.break_message:
                print(f"{self.name.capitalize()} broke!")

class HealthItem(Item):

    def __init__(self, name, description, health_effect, durability = 1, target_item = False):
        super().__init__(name, description, durability)
        self.health_effect = health_effect
        self.target_item = target_item

    def use(self, user, target):
        effect = Effect(f"you used your {self.name}", self.health_effect)
        if target.affect_health(effect):
            user.score += 10
        self.affect_durability(user, -1)

class Amulet(Item):

    def __init__(self, name, description, durability = 1):
        super().__init__(name, description, durability)

    def use(self, user, target):
        print(
            "\nThe amulet glows and shakes as you put it around you neck.\n"
            "It really is... the amulet of power! You've found it at last!\n"
        )
        user.win()
