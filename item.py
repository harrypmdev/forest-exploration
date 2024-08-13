import random

from effect import Effect
from game_state import GameState

class Item:
    """
    An abstract class for game items. Inherited by HealthItem and Amulet.

    Public Instance Attributes:
    name: str -- the name of the item.
    description: str -- a short description of the item.
    one_time_use: bool -- whether the item starts with a durability of 1 or
                          not, True if it does, False if it doesn't.
    broken: bool -- whether the item is broken (True) or not broken (False).
    """

    def __init__(self, name: str, description: str,
                 durability: int = 1) -> None:
        """
        Constructor for Item class.

        Arguments:
        name: str -- the name of the item.
        description: str -- a short description of the item.
        durability: int -- how many times the item can be used before it
                           breaks. Default is 1.
        """
        self.name = name
        self.description = description
        self.one_time_use = durability == 1
        self.broken = False
        self._durability = durability

    def _affect_durability(self, value: int) -> None:
        # Affect the item's durability and checks if item is broken.
        self._durability += value
        if self._durability <= 0:
            self.broken = True

class HealthItem(Item):
    """
    A class for items which affect an entity's health. Extends Item.

    Public Class Attributes:
    ITEMS: tuple -- a two dimensional tuple that contains the game's items.
                    Each tuple in ITEMS holds the arguments for its HealthItem.

    Public Instance Attributes:
    target_item: bool -- Whether the item must be targeted at an entity.
                         True if must be, False if can be used without target.

    Public Methods:
    get_effect: Effect -- Decrement the item durability and 
                          return the item's effect.
    """
    ITEMS = (
        ("tomahawk", "A one-time use weapon that deals 7 damage.", -7),
        ("potion", "A potion that heals 10 health.", 10),
        ("berries", "A tasty food. Heals 3 health.", 3),
        ("sword", "A sword that will last for a short while.", -4, 5, True),
        ("katana", "A super deadly sword that deals 10 damage.", -10, 7, True),
        ("axe", "A weak but durable weapon. Deals 3 damage.", -3, 15, True)
    )

    def __init__(self, name: str, description: str, health_effect: int, 
                 durability: int = 1, target_item: bool = False) -> None:
        """
        Constructor for HealthItem class.

        Arguments:
        name: str -- the name of the item.
        description: str -- a short description of the item.
        heath_effect: int -- the health this item confers to its target.
                             HealthItems which deal damage should be passed
                             a negative value.
        durability: int -- how many times the item can be used before it
                           breaks. Default is 1.
        target_item: bool -- Whether the item must be targeted at an entity.
                             True if must be, False if can be used without target.
        """
        super().__init__(name, description, durability)
        self.target_item = target_item
        self._health_effect = health_effect

    def get_effect(self) -> str:
        """ Decrement the item durability and return the item's effect. """
        self._affect_durability(-1)
        return Effect(f"you used your {self.name}", self._health_effect)  

class Amulet(Item):
    """
    A class for the amulet item which . Extends Item.

    Public Class Attributes:
    ITEMS: tuple -- a two dimensional tuple that contains the game's items.
                    Each tuple in ITEMS holds the arguments for its HealthItem.

    Public Instance Attributes:
    target_item: bool -- Whether the item must be targeted at an entity.
                         True if must be, False if can be used without target.

    Public Methods:
    use -- apply the item's health effect to a target (an entity).
    """

    def __init__(self):
        description = (
            "Could it be... the amulet of power? " 
            "There's only one way to find out."
        )
        super().__init__("amulet", description, 1)

    def activate(self):
        return(
            "The amulet glows and shakes as you put it around you neck.\n"
            "It really is... the amulet of power! You've found it at last!\n"
        )

_ITEM_PROBABILITY = {
        "tomahawk": 0.05,
        "potion": 0.06,
        "berries": 0.08,
        "sword": 0.04,
        "katana": 0.04,
        "axe": 0.05,
    }

def generate_items(*args: str, amulet_probability = 0) -> list[Item]:
    item_list = []
    types = map(str.lower, args)
    if "healthitem" in types:
        item_list.extend(_generate_health_items())
    if "amulet" in types:
        if random.random() < amulet_probability:
            item_list.append(Amulet())
    return item_list

def _generate_health_items():
    item_list = []
    for item_args in HealthItem.ITEMS:
        item_name = item_args[0]
        if random.random() < _ITEM_PROBABILITY[item_name]:
            item_list.append(HealthItem(*item_args))
    return item_list