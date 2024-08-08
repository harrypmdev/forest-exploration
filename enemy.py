import random
import math
from entity import Entity
from effect import Effect
from item import Amulet

class Enemy(Entity):

    def __init__(self, health, name, game_state, item_field, max_damage, accuracy, attack_name):
        super().__init__(health, name, game_state, hostile=True)
        self.max_damage = max_damage
        self.item_field = item_field
        self.accuracy = accuracy
        self.attack_name = attack_name
        self.loot = self.generate_loot()

    def generate_loot(self):
        loot = []
        for item in self.item_field:
            if random.random() < self.item_field[item] and item.name != "amulet":
                loot.append(item)
        return loot
        
    def get_attack(self, target) -> Effect:
        if random.random() < self.accuracy:
            damage = math.ceil(self.max_damage * (random.random() * self.accuracy))
            attack = Effect(f"{self.attack_name} by {self.name}", -damage)
            print(f"{self.name.capitalize()} attacked and it hit!")
            print(f"{target.name.capitalize()} {attack.name} for {str(damage)} damage.\n")
            target.affect_health(attack, False)
        else:
            print(f"{self.name.capitalize()} attacked and it missed!\n")
        
    def search(self, player):
        self.searched = True
        for item in self.loot:
            player.inventory.append(item)
        return self.loot