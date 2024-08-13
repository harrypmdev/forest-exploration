""" A module for the Entity class utilised in Forest Exploration. """
import random
import math

from effect import Effect
from item import Item, HealthItem, Amulet, GenerateItems

class Entity:
    """
    A class for the game entities, which includes all living creatures.
    Inherited by Player and Enemy classes.

    Instance Attributes:
    health: int -- the health of the entity
    name: str -- the entity's name
    board: GameBoard -- the board the entity is on
    player: Player -- the player for which moves are being parsed.
    

    Public Methods:
    parse_move -- parse a raw move from the user
    """
    ANIMAL_NAMES = ("rabbit", "squirrel", "horse", "fox", "badger", "raccoon", "dog")
        
    def __init__(self, health: int, name: str, hostile: bool = False):
        self.name = name
        self.health = health
        self.alive = True
        self.sick = health <= 2
        self.cured = False
        self.searched = False
        self.hostile = hostile

    def affect_health(self, effect: Effect) -> str:
        if not self.alive:
            return f"The {self.name} is dead, so nothing happens."
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            return self._die(effect)
        sickness_changed = " Its sickness was cured." if self._update_sickness() else ""
        target_text = "on yourself" if self.name == "player" else f"on {self.name}"
        effect_text = f"restoring {effect.value} health" if effect.value >= 0 else f"dealing {abs(effect.value)} damage"
        return f"{effect.name.capitalize()} {target_text} {effect_text}!{sickness_changed}"
    
    def detailed_name(self, indefinite = False):
        article = self._indefinite() + " " if indefinite else ""
        dead_string = f"{article}{self.name}" if self.alive else f"{article}dead {self.name}"
        sick_string = " (it looks sick and weak)" if self.sick else ""        
        searched_string = ""
        if not self.alive and self.hostile:
            searched_string = " (searched)" if self.searched else " (not searched)"
        hostile_string = " (hostile)" if self.hostile and self.alive else ""
        return f"{dead_string}{hostile_string}{sick_string}{searched_string}"

    def print_status(self):
        sick_status = " It looks sick and weak." if self.sick == True else ""
        if self.health == 0:
            print(f"\n{self.name.capitalize()} is dead.\n")
        else:
            print(f"\n{self.name.capitalize()} has {self.health} health.{sick_status}\n")

    def _update_sickness(self):
        if self.health > 2 and self.sick:
            self.sick = False
            self.cured = True
            return True
    
    def _die(self, effect):
        self.alive = False
        return (f'The {self.name} died! It ran out of health when {effect.name} causing {abs(effect.value)} damage!')
    
    def _indefinite(self):
        vowels = ("a", "e", "i", "o", "u")
        if self.name[0] in vowels:
            return "an"
        return "a"

class Enemy(Entity):
    ENEMIES = {
        "ogre": "was clubbed", 
        "vampire": "had their blood sucked", 
        "scorpion": "got stung", 
        "slime": "got slimed", 
        "wyvern": "got burnt", 
        "goblin": "got clawed and scratched"
    }

    def __init__(self, health, name, attack_name, max_damage, accuracy):
        super().__init__(health, name, hostile=True)
        self.max_damage = max_damage
        self.accuracy = accuracy
        self.attack_name = attack_name
        self.loot = GenerateItems.generate("HealthItem")

    def get_attack(self) -> Effect:
        damage = math.ceil(self.max_damage * (random.random() * self.accuracy))
        attack = Effect(f"{self.attack_name} by {self.name}", -damage)
        return attack
        
    def search(self) -> list[Item]:
        self.searched = True
        return self.loot

class GenerateEntities:

    @classmethod
    def generate(cls, *args: str):
        entity_list = []
        types = map(str.lower, args)
        if "animal" in types:
            entity_list.extend(cls._generate_animals())
        if "enemy" in types:
            entity_list.extend(cls._generate_enemies())
        return entity_list

    @classmethod
    def _generate_animals(cls):
        animal_list = []
        for name in Entity.ANIMAL_NAMES:
            if random.random() < 0.10:
                health = random.randrange(1, 7)
                animal = Entity(
                        health, 
                        name
                )
                animal_list.append(animal)
        return animal_list

    @classmethod
    def _generate_enemies(cls):
        enemy_list = []
        gen_chance = 0.10
        for name, attack_name in Enemy.ENEMIES.items():
            if random.random() < gen_chance:
                gen_chance -= 0.02
                max_damage = random.randrange(3, 12)
                accuracy = random.randrange(50, 100) / 100
                health = random.randrange(4, 17)
                enemy = Enemy(
                        health, 
                        name, 
                        attack_name,
                        max_damage,
                        accuracy,
                )
                enemy_list.append(enemy)
        return enemy_list