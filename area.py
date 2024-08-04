import random
from entity import Entity
from enemy import Enemy

class Area:

    def __init__(self, y, x, board, hostiles = True):
        self.y = y
        self.x = x
        self.board = board
        self.description = self.generate_description()
        self.entities = []
        animal_names = ["rabbit", "squirrel", "horse", "fox", "badger", "raccoon", "wild dog"]
        enemy_names = ["ogre", "vampire bat", "giant scorpion", "slime", "dwarf wyvern", "goblin"]
        self.generate_entities(0.25, animal_names, 1, 10, Entity)
        if hostiles:
            self.generate_entities(0.4, enemy_names, 4, 17, Enemy, )
    
    def generate_description(self):
        tree_adjectives = ("bushy", "tall", "short", "thin and white", 
        "sick looking", "strange and contorted", "healthy looking")
        ground_adjectives = ("stony and tough", "made up of course dirt", "scattered with grass patches",
        "thick with tall grass", "steep and uneven", "flat and dry", "damp and strange")
        tree_sentence = f"The trees in this area are {random.choice(tree_adjectives)}."
        ground_sentence = f"The ground is {random.choice(ground_adjectives)}."
        return tree_sentence + " " + ground_sentence
    
    def generate_entities(self, chance, names, health_min, health_max, EntityType):
        attack_names = {
            "ogre": "was clubbed", 
            "vampire bat": "had their blood sucked", 
            "giant scorpion": "got stung", 
            "slime": "got slimed", 
            "dwarf wyvern": "got burnt", 
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
                        self.board, 
                        max_damage,
                        accuracy,
                        attack_name
                    )
                else:
                    entity = EntityType(
                        entity_health, 
                        random.choice(local_names), 
                        self.board, 
                        entity_health <= 2,
                    )
                self.entities.append(entity)
                self.generate_entities(chance*0.3, local_names, health_min, health_max, EntityType)
    
