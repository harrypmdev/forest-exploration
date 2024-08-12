import random

from entity import GenerateEntities
from item import Amulet, GenerateItems

class Area:

    def __init__(self, y, x, game_state, hostiles = True):
        self.y = y
        self.x = x
        self.game_state = game_state
        self.items = self._generate_items()
        self._area_description = self._generate_area_description()
        entity_types = ("animal", "enemy") if hostiles else ("animal",)
        self.entities = GenerateEntities.generate(entity_types)

    def in_battle(self) -> bool:
        """ 
        Check if the player is currently in battle (hostile entities are present).
        Returns True if in battle, False if not.
        """
        for entity in self.entities:
            if entity.hostile and entity.alive:
                return True
        return False
    
    def get_description(self) -> str:
        entities_description = self._generate_entities_description()
        items_description = self._generate_items_description()
        battle_description = self._generate_battle_description()
        return (
            self._area_description 
            + entities_description 
            + items_description
            + battle_description
        )

    def _generate_battle_description(self):
        if self.in_battle():
            return "A hostile creature is present! You are in battle.\n"
        else:
            return ""


    def _generate_items_description(self):
        if self.items:
            items_description = "On the floor lies:\n"
            for item in self.items:
                items_description += f"{item.name.capitalize()}\n"
            return items_description
        else:
            return ""

    def _generate_entities_description(self):    
        if len(self.entities) == 1:
            return f"\nThere is {self.entities[0].detailed_name(True)}.\n"
        elif len(self.entities) > 1:
            entities_description = "\nThere are multiple creatures present:\n"
            for entity in self.entities:
                entities_description += f"{entity.detailed_name().capitalize()}\n"
            return entities_description
        else:
            return "\nThere are no living creatures present except you.\n"

    def _generate_area_description(self):
        tree_adjectives = ("bushy", "tall", "short", "thin and white", 
        "sick looking", "strange and contorted", "healthy looking")
        ground_adjectives = ("stony and tough", "made up of course dirt", "scattered with grass patches",
        "thick with tall grass", "steep and uneven", "flat and dry", "damp and strange")
        tree_sentence = f"The trees in this area are {random.choice(tree_adjectives)}."
        ground_sentence = f"The ground is {random.choice(ground_adjectives)}."
        return tree_sentence + " " + ground_sentence
    
    def _generate_items(self):
        items = GenerateItems.generate(("HealthItem", "Amulet"), self.game_state)
        if any(isinstance(item, Amulet) for item in items):
            self.game_state.amulet_generated = True
        return items