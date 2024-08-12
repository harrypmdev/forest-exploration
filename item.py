import random

from effect import Effect
from game_state import GameState

class Item:

    def __init__(self, name, description, durability = 1):
        self.name = name
        self.description = description
        self.durability = durability
        self.one_time_use = durability == 1
        self.broken = False

    def affect_durability(self, value):
        self.durability += value
        if self.durability <= 0:
            self.broken = True

class HealthItem(Item):
    ITEMS = (
        ("tomahawk", "A one-time use weapon that deals 7 damage.", -7),
        ("potion", "A potion that heals 10 health.", 10),
        ("berries", "A tasty food. Heals 3 health.", 3),
        ("sword", "A sword that will last for a short while.", -4, 5, True),
        ("katana", "A super deadly sword that deals 10 damage.", -10, 7, True),
        ("axe", "A weak but durable weapon. Deals 3 damage.", -3, 15, True)
    )

    def __init__(self, name, description, health_effect, durability = 1, target_item = False):
        super().__init__(name, description, durability)
        self.health_effect = health_effect
        self.target_item = target_item

    def use(self, target):
        self.affect_durability(-1)
        effect = Effect(f"you used your {self.name}", self.health_effect)  
        return target.affect_health(effect)

class Amulet(Item):

    def __init__(self, game_state):
        super().__init__(
            "amulet", 
            "Could it be... the amulet of power? There's only one way to find out.", 
            1)
        self.game_state = game_state

    def activate(self):
        print(
            "\nThe amulet glows and shakes as you put it around you neck.\n"
            "It really is... the amulet of power! You've found it at last!\n"
        )
        self.game_state.win()

class GenerateItems:

    @staticmethod
    def generate(types: tuple[str], 
                game_state: GameState = GameState()) -> list[Item]:
        item_list = []
        types = map(str.lower,types)
        if "healthitem" in types:
            for item_args in HealthItem.ITEMS:
                item_name = item_args[0]
                if random.random() < game_state.item_probabilites[item_name]:
                    item_list.append(HealthItem(*item_args))
        if "amulet" in types:
            if random.random() < game_state.item_probabilites["amulet"]:
                item_list.append(Amulet(game_state))
        return item_list