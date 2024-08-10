import random
import copy
from entity import Entity
from enemy import Enemy
from item import HealthItem, Amulet

class Area:

    def __init__(self, y, x, game_state, hostiles = True):
        self.y = y
        self.x = x
        self.game_state = game_state
        self.items = self.generate_items()
        self.description = self.generate_description()
        self.entities = []
        animal_names = ["rabbit", "squirrel", "horse", "fox", "badger", "raccoon", "dog"]
        enemy_names = ["ogre", "vampire", "scorpion", "slime", "wyvern", "goblin"]
        self.generate_entities(0.25, animal_names, 1, 10, Entity)
        if hostiles:
            self.generate_entities(0.6, enemy_names, 4, 17, Enemy, )
    
    def get_description(self) -> str:
        entities_sentence = "\nThere are no living creatures present except you.\n"
        if len(self.entities) == 1:
            entities_sentence = f"\nThere is {self.entities[0].detailed_name(True)}.\n"
        if len(self.entities) > 1:
            entities_sentence = "\nThere are multiple creatures present:\n"
            for entity in self.entities:
                entities_sentence += f"{entity.detailed_name().capitalize()}\n"
        item_sentence = ""
        if self.items:
            item_sentence = "On the floor lies:\n"
            for item in self.items:
                item_sentence += f"{item.name.capitalize()}\n"
        return self.description + entities_sentence + item_sentence

    def generate_description(self):
        tree_adjectives = ("bushy", "tall", "short", "thin and white", 
        "sick looking", "strange and contorted", "healthy looking")
        ground_adjectives = ("stony and tough", "made up of course dirt", "scattered with grass patches",
        "thick with tall grass", "steep and uneven", "flat and dry", "damp and strange")
        tree_sentence = f"The trees in this area are {random.choice(tree_adjectives)}."
        ground_sentence = f"The ground is {random.choice(ground_adjectives)}."
        return tree_sentence + " " + ground_sentence
    
    def generate_items(self):
        items = []
        for item_args in HealthItem.ITEMS:
            item_name = item_args[0]
            if random.random() < self.game_state.item_probabilites[item_name]:
                items.append(HealthItem(*item_args))
        if random.random() < self.game_state.item_probabilites["amulet"]:
            items.append(Amulet(self.game_state))
            self.game_state.amulet_generated = True
        return items
    
    def generate_entities(self, chance, names, health_min, health_max, EntityType):
        attack_names = {
            "ogre": "was clubbed", 
            "vampire": "had their blood sucked", 
            "scorpion": "got stung", 
            "slime": "got slimed", 
            "wyvern": "got burnt", 
            "goblin": "got clawed and scratched"}
        local_names = names[:]
        if random.random() < chance:
            for entity in self.entities:
                if entity.name in local_names:
                    local_names.remove(entity.name)
            if len(local_names) > 0:
                entity_health = random.randrange(health_min, health_max)
                if EntityType == Enemy:
                    max_damage = random.randrange(3, 12)
                    accuracy = random.randrange(50, 100) / 100
                    name_choice = random.choice(local_names)
                    attack_name = attack_names[name_choice]
                    entity = EntityType(
                        entity_health, 
                        name_choice, 
                        self.game_state,
                        max_damage,
                        accuracy,
                        attack_name
                    )
                else:
                    entity = EntityType(
                        entity_health, 
                        random.choice(local_names), 
                        self.game_state, 
                        entity_health <= 2,
                    )
                self.entities.append(entity)
                self.generate_entities(chance*0.3, local_names, health_min, health_max, EntityType)
    
