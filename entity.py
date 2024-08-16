"""
A module for the Entity and Enemy classes utilised in the Forest exploration
game and the generate_entities function.

Classes:
Entity -- A class for the game entities, which includes all living creatures.
Enemy -- A class for the game enemies, creatures that attack the player.

Functions:
generate_entities -- Randomly generate game entities.
"""

import random
import math

from effect import Effect
from item import Item, generate_items


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
    cured: bool -- whether entity has been cured of sickness of not (True
                   if cured, False if not). Constructor always sets to False.

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
        self.cured = False
        self._searched = False
        self._sick = health <= 2

    def apply_effect(self, effect: Effect) -> str:
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
        sickness_changed = ""
        if self._update_sickness():
            sickness_changed = " Its sickness was cured."
        sickness_changed = " Its sickness was cured." if self._update_sickness() else ""
        target_text = "on yourself" if self.name == "player" else f"on {self.name}"
        effect_text = (
            f"restoring {effect.value} health"
            if effect.value >= 0
            else f"dealing {abs(effect.value)} damage"
        )
        return (
            f"{effect.name.capitalize()} {target_text} {effect_text}!{sickness_changed}"
        )

    def detailed_name(self, indefinite=False) -> str:
        """
        Return the 'detailed name' of the entity.
        This includes whether the entity is dead, hostile, sick or searched.

        Arguments:
        indefinite: bool -- Whether the indefinite article should be added to
                            the return string. True if yes, False if not.
                            Default False.

        Returns a string.
        """
        sick_string = ""
        searched_string = ""
        hostile_string = ""
        article = ""
        dead_string = f"dead {self.name}"
        if self.hostile:
            hostile_string = " (hostile)"
        if self.alive:
            dead_string = f"{self.name}"
        if indefinite:
            article = self._indefinite(dead_string) + " "
        if self._sick:
            sick_string = " (it looks sick and weak)"
        if not self.alive and self.hostile and self._searched:
            searched_string = " (searched)"
        if not self.alive and self.hostile and not self._searched:
            searched_string = " (not searched)"
        hostile_string = " (hostile)" if self.hostile and self.alive else ""
        return (
            f"{article}{dead_string}{hostile_string}" f"{sick_string}{searched_string}"
        )

    def print_status(self) -> None:
        # Print the entity's status (health, sickness, living state).
        sick_status = " It looks sick and weak." if self._sick else ""
        if self.health == 0:
            print(f"\n{self.name.capitalize()} is dead.\n")
        else:
            print(
                f"\n{self.name.capitalize()} has {self.health} health.{sick_status}\n"
            )

    def _update_sickness(self) -> bool:
        # Update sick and cured attributes based on entity health. Return false.
        if self.health > 2 and self._sick:
            self._sick = False
            self.cured = True
            return True

    def _die(self, effect: Effect) -> str:
        # Change alive attribute to false and return string describing death.
        self.alive = False
        return (
            f"The {self.name} died!\nIt ran out of health "
            f"when {effect.name} causing {abs(effect.value)} damage!"
        )

    def _indefinite(self, name: str) -> str:
        # Return the indefinite article for the given name string.
        vowels = ("a", "e", "i", "o", "u")
        if name[0] in vowels:
            return "an"
        return "a"


class Enemy(Entity):
    """
    A class for the game enemies, creatures that attack the player at the
    end of each turn. Extends Entity.

    Public Class Attributes:
    ENEMIES: dict -- a dictionary of enemy names (keys) and their respective
                     attack names (values) for use in generating enemies.

    Public Methods:
    get_attack -- return the enemy's attack as an Effect.
    search -- return the enemy loot as a list of Item objects,
              set _searched attribute to True.
    attack_chance -- randomly return either True if an attack hits,
                     or False if it misses according to the enemy's
                     hit accuracy.
    """

    ENEMIES = {
        "ogre": "was clubbed",
        "vampire": "had their blood sucked",
        "scorpion": "got stung",
        "slime": "got slimed",
        "wyvern": "got burnt",
        "goblin": "got clawed and scratched",
    }

    def __init__(
        self, health: int, name: str, attack_name: str, max_damage: int, accuracy: float
    ):
        """
        Constructor for Enemy class.

        Arguments:
        health: int -- the health of the entity.
        name: str -- the entity's name.
        attack_name: str -- the name of the enemy's attack e.g 'got stung'
        max_damage: int -- the maximum attack damage this enemy can produce
                           when generating an attack in get_attack method
        accuracy: float -- the probability of an attack hitting its target,
                           from 0 (not at all) to 1 (definitely).
        """
        super().__init__(health, name, hostile=True)
        self._max_damage = max_damage
        self._accuracy = accuracy
        self._attack_name = attack_name
        self._loot = generate_items("HealthItem", multiplier=2.55)

    def get_attack(self) -> Effect:
        """Return the enemy's attack as an Effect."""
        damage = math.ceil(self._max_damage * (random.random() * self._accuracy))
        attack = Effect(f"{self._attack_name} by {self.name}", -damage)
        return attack

    def search(self) -> list[Item]:
        """
        Search the enemy for loot, returning a list of items.
        Sets private bool attribute _searched to True so only returns
        the enemy's loot once, otherwise returns an empty list.
        """
        if self._searched:
            return []
        else:
            self._searched = True
            return self._loot

    def attack_chance(self) -> bool:
        """
        Randomly return either True if an attack hits,
        or False if it misses according to the enemy's hit accuracy.
        """
        return True if random.random() < self._accuracy else False


def generate_entities(*args: str):
    """
    Randomly generate game entities.

    Arguments:
    *args: str -- variable number of string arguments which denote the entity
                  types that should be generated, e.g "animal", "enemy".

    Returns a list of Entity objects.
    """
    entity_list = []
    types = [arg.lower() for arg in args]
    if "animal" in types:
        entity_list.extend(_generate_animals())
    if "enemy" in types:
        entity_list.extend(_generate_enemies())
    return entity_list


def _generate_animals():
    # Return a list of randomly generated animals
    animal_list = []
    for name in Entity.ANIMAL_NAMES:
        if random.random() < 0.10:
            health = random.randrange(1, 7)
            animal = Entity(health, name)
            animal_list.append(animal)
    return animal_list


def _generate_enemies():
    # Return a list of randomly generated enemies
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
