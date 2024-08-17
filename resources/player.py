"""A module for the Player class utilised in Forest Exploration."""

from resources.entity import Entity
from resources.utility import border
from resources.item import Item
from resources.effect import Effect


class Player(Entity):
    """
    A class for the player of the Forest Exploration game.

    Public Attributes:
    inventory: list[Items] -- a list of Items that the player can use.

    Public Methods:
    print_status -- Print the player's status
    print_inventory -- Print the player's inventory
    """

    def __init__(self, health: int, inventory: list[Item] = []) -> None:
        """
        Constructor for Player class.

        Arguments:
        health: int -- the player's starting health.
        inventory: list[Item] -- the player's starting items. Default
                                 is empty list.
        """
        super().__init__(health, "player")
        self.inventory = inventory

    def print_status(self, score: int) -> bool:
        """Print the player's status (health and score). Always returns False."""
        print(f"\nYou have {self.health} health. " f"Your score is {str(score)}\n")
        return False

    def print_inventory(self) -> bool:
        "Print the player's inventory. Always returns False."
        if not self.inventory:
            print("\nYour inventory is empty.\n")
            return False
        print("\nYour inventory:")
        item_names = []
        for item in self.inventory:
            item_names.append(item.name)
        for item_name in sorted(item_names):
            print(f"{item_name}")
        print("")
        return False

    @border
    def _die(self, effect: Effect) -> None:
        print(
            f"You died! Player {effect.name} causing"
            f"\n{abs(effect.value)} damage and ran out of health!"
        )
        self.alive = False
