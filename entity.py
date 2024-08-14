""" A module for the Entity class utilised in Forest Exploration. """
import random
import math

from effect import Effect
from item import Item, HealthItem, Amulet, generate_items

class Entity:
    """
    A class for the game entities, which includes all living creatures.
    Inherited by Player and Enemy classes.

    Public Class Attributes:
    ANIMAL_NAMES: tuple[str] -- a tuple of animals that can be used when
                                generating entities.

    Public Instance Attributes:
    health: int -- the health of the entity.
    name: str -- the entity's name.
    hostile: bool - whether the entity will attack the player when the turn
                    ends (True if so, False if not). Default False.
    alive: bool -- whether the entity is alive or not (True if alive, False
                   if not). Constructor always sets to True.

    Public Methods:
    apply_health_effect -- apply an effect to the entity and return a
                           string description of the action.
    detailed_name -- return a detailed version of the entity's name.
    print_status -- print the entity's status.
    """
    ANIMAL_NAMES = ("rabbit", "squirrel", "horse", "fox", "badger", "raccoon", "dog")
        
    def __init__(self, health: int, name: str, hostile: bool = False) -> None:
        """
        Constructor for Entity class.

        Arguments:
        health: int -- the health of the entity.
        name: str -- the entity's name.
        hostile: bool - whether the entity will attack the player when the turn
                        ends (True if so, False if not). Default False.
        """
        self.health = health
        self.name = name
        self.hostile = hostile
        self.alive = True
        self._searched = False
        self._sick = health <= 2
        self._cured = False

    def apply_health_effect(self, effect: Effect) -> str:
        """ 
        Apply an Effect object to the entity.
        Potentially alters entity's health and alive attributes.

        Arguments:
        effect: Effect -- the effect that should be applied to the entity.

        Returns a string describing the outcome.
        """
        if not self.alive:
            return f"The {self.name} is dead, so nothing happens."
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            return self._die(effect)
        sickness_changed = " Its sickness was cured." if self._update_sickness() else ""
        target_text = "on yourself" if self.name == "player" else f"on {self.name}"
        effect_text = f"restoring {effect.value} health" if effect.value >= 0 else f"dealing {abs(effect.value)} damage"
        return f"{effect.name.capitalize()} {target_text} {effect_text}!{sickness_changed}"
    
    def detailed_name(self, indefinite = False) -> str:
        """
        Return the 'detailed name' of the entity.
        This includes whether the entity is dead, hostile, sick or searched.

        Arguments:
        indefinite: bool -- Whether the indefinite article should be added to
                            the return string. True if yes, False if not.
                            Default False.
        
        Returns a string.
        """
        article = self._indefinite() + " " if indefinite else ""
        dead_string = f"{article}{self.name}" if self.alive else f"{article}dead {self.name}"
        sick_string = " (it looks sick and weak)" if self.sick else ""        
        searched_string = ""
        if not self.alive and self.hostile:
            searched_string = " (searched)" if self.searched else " (not searched)"
        hostile_string = " (hostile)" if self.hostile and self.alive else ""
        return f"{dead_string}{hostile_string}{sick_string}{searched_string}"

    def print_status(self):
        # Print the entity's status (health, sickness, living state).
        sick_status = " It looks sick and weak." if self.sick == True else ""
        if self.health == 0:
            print(f"\n{self.name.capitalize()} is dead.\n")
        else:
            print(f"\n{self.name.capitalize()} has {self.health} health.{sick_status}\n")

    def _update_sickness(self):
        # Update sick and cured attributes based on entity health.
        if self.health > 2 and self.sick:
            self.sick = False
            self.cured = True
            return True
    
    def _die(self, effect):
        # Change alive attribute to false and return string describing death.
        self.alive = False
        return (f"The {self.name} died! It ran out of health "
                 "when {effect.name} causing {abs(effect.value)} damage!")
    
    def _indefinite(self):
        # Return the indefinite article for the entity
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
        self.loot = generate_items("HealthItem")

    def get_attack(self) -> Effect:
        damage = math.ceil(self.max_damage * (random.random() * self.accuracy))
        attack = Effect(f"{self.attack_name} by {self.name}", -damage)
        return attack
        
    def search(self) -> list[Item]:
        self._searched = True
        return self.loot

def generate_entities(*args: str):
    entity_list = []
    types = [arg.lower() for arg in args]
    if "animal" in types:
        entity_list.extend(_generate_animals())
    if "enemy" in types:
        entity_list.extend(_generate_enemies())
    return entity_list

def _generate_animals():
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

def _generate_enemies():
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