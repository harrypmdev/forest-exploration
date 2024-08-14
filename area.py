"""A module for the Area class utilised in the Forest Exploration game."""

import random

from entity import generate_entities
from item import generate_items


class Area:
    """
    A class for areas, one of which is created for each map coordinate.

    Public Instance Attributes:
    y: int -- the y coordinate for this area on the map
    x: int -- the x coordinate for this area on the map
    items: list:[Item] -- a list of items present in the area
    entities: list[Entity] -- a list of entities present in the area

    Public Methods:
    in_battle: bool -- returns True if the area has any living hostiles
    get_description: str -- returns a detailed description of the area
    """

    def __init__(
        self, y: int, x: int, amulet_probability: float = 0, hostiles=True
    ) -> None:
        """
        Constructor for Area class.

        Arguments:
        y: int -- the y coordinate this area is located at.
        x: int -- the x coordinate this area is locatied at.
        amulet_probability: float -- the chance of an amulet being generated in
                                     this area (0 is none, 1 is definite).
        hostiles: bool -- whether this area should generate hostile entities
                          (True) or only non-hostiles (False). Default is True.
        """
        self.y = y
        self.x = x
        self.items = generate_items(
            "HealthItem", "Amulet", amulet_probability=amulet_probability
        )
        entity_types = ("animal", "enemy") if hostiles else ("animal",)
        self.entities = generate_entities(*entity_types)
        self._area_description = self._generate_area_description()

    def in_battle(self) -> bool:
        """Return True if the player is currently in battle, False if not."""
        for entity in self.entities:
            if entity.hostile and entity.alive:
                return True
        return False

    def get_description(self) -> str:
        """Return a string of a detailed description of the area."""
        entities_description = self._generate_entities_description()
        items_description = self._generate_items_description()
        battle_description = self._generate_battle_description()
        return (
            self._area_description
            + entities_description
            + items_description
            + battle_description
        )

    def _generate_battle_description(self) -> str:
        # Return a string alerting the user they are in battle if hostiles are
        # present, return an empty string if not.
        if self.in_battle():
            return "A hostile creature is present! You are in battle.\n"
        else:
            return ""

    def _generate_items_description(self) -> str:
        # Return a description of any items in the area
        if self.items:
            items_description = "On the floor lies:\n"
            for item in self.items:
                items_description += f"{item.name.capitalize()}\n"
            return items_description
        else:
            return ""

    def _generate_entities_description(self) -> str:
        # Return a description of any entities in the area
        if len(self.entities) == 1:
            return f"\nThere is {self.entities[0].detailed_name(True)}.\n"
        elif len(self.entities) > 1:
            entities_description = "\nThere are multiple creatures present:\n"
            for entity in self.entities:
                entities_description += f"{entity.detailed_name().capitalize()}\n"
            return entities_description
        else:
            return "\nThere are no living creatures present except you.\n"

    def _generate_area_description(self) -> str:
        # Return a randomly produced area description
        tree_adjectives = (
            "bushy",
            "tall",
            "short",
            "thin and white",
            "sick looking",
            "strange and contorted",
            "healthy looking",
        )
        ground_adjectives = (
            "stony and tough",
            "made up of course dirt",
            "scattered with grass patches",
            "thick with tall grass",
            "steep and uneven",
            "flat and dry",
            "damp and strange",
        )
        tree_sentence = f"The trees in this area are {random.choice(tree_adjectives)}."
        ground_sentence = f"The ground is {random.choice(ground_adjectives)}."
        return tree_sentence + " " + ground_sentence
