import time
import sys
import random

import Player
import Game
import Boss



class Enemy:
    #an enemy with semi-random stats based on the player's level
    def __init__(self, level, name):
        self.name = name
        self.level = level
        self.totalHp = 100 + 20 * (self.level - 1)
        self.hp = self.totalHp
        self.attack = int(random.randrange(5, 10) * self.level)
        self.defense = (self.level - 1) * 7
        self.gold = self.level + random.randint(-int(self.level/2), int(self.level/2))
        self.exp = 20 * self.level ** 2 + random.randint(-int(self.level), int(self.level))

    #death check
    def dead(self, player):
        if self.hp <= 0:
            player.gold += self.gold
            player.exp += self.exp 
            player.battlesWon += 1

            print("You won the battle!")
            time.sleep(.5)
            print("You earned {} gold and {} experience points!".format(self.gold, self.exp))
            
            return True
        return False

    #damage that is dealt to the player
    def calcDamage(self, player):
        attack = self.attack 
        defense = player.calcDefense()
        dmg = random.randint(-int(attack/10), int(attack/10)) + attack - defense
        if dmg < 0:
            dmg = 0
        return dmg

    #this is how the enemy takes damage
    def getDamaged(self, dmg):
        self.hp -= dmg
        print("You dealt {} damage to the enemy! {}/{} HP left.".format(dmg, self.hp, self.totalHp))
        time.sleep(.5)