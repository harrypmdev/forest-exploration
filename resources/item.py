"""A module for the Item class utilised in the Forest exploration game, its child classes
and the generate_items function.

Classes:
Item -- An abtract class for the game's items inherited by
        HealthItem and Amulet.
HealthItem -- A class for items that effect an entity's health.
Amulet -- A class for the amulet item which ends the game.

Functions:
generate_items -- Randomly generate items.
"""

import random
from abc import ABC

from resources.effect import Effect


class Item(ABC):
    """An abstract class for game items. Inherited by HealthItem and Amulet.

    Public Instance Attributes:
    name: str -- the name of the item.
    description: str -- a short description of the item.
    one_time_use: bool -- whether the item starts with a durability of 1 or
                          not, True if it does, False if it does not.
    broken: bool -- whether the item is broken (True) or not broken (False).
    """

    def __init__(self, name: str, description: str, durability: int = 1) -> None:
        """Constructor for Item class.

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
    """A class for items which affect an entity's health. Extends Item.

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
        ("axe", "A weak but durable weapon. Deals 3 damage.", -3, 15, True),
    )

    def __init__(
        self,
        name: str,
        description: str,
        health_effect_value: int,
        durability: int = 1,
        target_item: bool = False,
    ) -> None:
        """Constructor for HealthItem class.

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
        self._health_effect_value = health_effect_value

    def get_effect(self) -> Effect:
        """Decrement the item durability and return the item's effect."""
        self._affect_durability(-1)
        return Effect(f"you used your {self.name}", self._health_effect_value)


class Amulet(Item):
    """A class for the amulet item which ends the game. Extends Item.

    Public Methods:
    activate -- return the amulet activation message.
    """

    def __init__(self) -> None:
        """Constructor for Amulet class."""
        description = (
            "Could it be... the amulet of power? " "There's only one way to find out."
        )
        super().__init__("amulet", description, 1)

    def activate(self) -> str:
        """Return the amulet activation message."""
        return (
            "The amulet glows and shakes as you put it around you neck.\n"
            "It really is... the amulet of power! You've found it at last!\n"
        )


_ITEM_GEN_PROBABILITY = {
    "tomahawk": 0.07,
    "potion": 0.06,
    "berries": 0.08,
    "sword": 0.04,
    "katana": 0.04,
    "axe": 0.05,
}


def generate_items(
    *args: str, amulet_probability: float = 0, multiplier: float = 1.0
) -> list[Item]:
    """Randomly generate game items.

    Arguments:
    *args: str -- variable number of string arguments which denote the item
                  types that should be generated, e.g "healthitem", "amulet".
    amulet_probability: float -- the probability of an amulet generating, from
                                 0 (not at all) to 1 (definitely). Default 0.
    multiplier: float -- how much more likely than the default items are to
                         generate. Default is 1.

    Returns a list of Item objects.
    """
    item_list = []
    types = [arg.lower() for arg in args]
    if "healthitem" in types:
        item_list.extend(_generate_health_items(multiplier))
    if "amulet" in types:
        if random.random() < amulet_probability:
            item_list.append(Amulet())
    return item_list


def _generate_health_items(probability: float = 1.0) -> list[HealthItem]:
    # Return a randomly generated list of health items
    item_list = []
    for item_args in HealthItem.ITEMS:
        item_name = item_args[0]
        if random.random() < _ITEM_GEN_PROBABILITY[item_name] * probability:
            item_list.append(HealthItem(*item_args))
    return item_list
