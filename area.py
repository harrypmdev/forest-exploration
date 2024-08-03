import random
from entity import Entity

class Area:

    def __init__(self, y, x, board):
        self.y = y
        self.x = x
        self.board = board
        self.description = self.generate_description()
        self.entities = []
        self.generate_benign_entities(0.5)
    
    def generate_description(self):
        tree_adjectives = ("bushy", "tall", "short", "thin and white", 
        "sick looking", "strange and contorted", "healthy looking")
        ground_adjectives = ("stony and tough", "made up of course dirt", "scattered with grass patches",
        "thick with tall grass", "steep and uneven", "flat and dry", "damp and strange")
        tree_sentence = f"The trees in this area are {random.choice(tree_adjectives)}."
        ground_sentence = f"The ground is {random.choice(ground_adjectives)}."
        return tree_sentence + " " + ground_sentence
    
    def generate_benign_entities(self, chance):
        if random.random() < chance:
            entity_names = ["rabbit", "squirrel", "horse", "fox", "badger", "raccoon", "wild dog"]
            for entity in self.entities:
                if entity.name in entity_names:
                    entity_names.remove(entity.name)
            if len(entity_names) > 0:
                entity_health = random.randrange(1, 12)
                animal = Entity(entity_health, random.choice(entity_names), self.board, entity_health <= 2)
                self.entities.append(animal)
                self.generate_benign_entities(chance*0.7)
