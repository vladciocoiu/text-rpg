import time
import sys
import random

import Game
import Enemy
import Boss


class Player:
    def __init__(self, name):
        self.name = name
        self.bossesKilled = 0
        self.battlesWon = 0
        self.gold = 99
        self.hp = 100
        self.totalHp = 100
        self.level = 1
        self.exp = 0
        self.maxExp = 100
        self.baseAttack = 5

        #the level of the equipment
        self.eq = {
            "sword": 1,
            "armor": 0
        }

        #the cost of the equipment
        self.cost = {
            "sword": 3,
            "armor": 2
        }

        #uses left on every item
        self.itemUses = {
            "Health Potion": 0,
            "EXP Ring": 0,
            "Gold Magnet": 0
        }

    def calcAttack(self):
        return self.baseAttack + self.eq["sword"]*10

    def calcDefense(self):
        return self.eq["armor"] * 7

    #this levels the player up
    def levelUp(self):
        if self.exp >= self.maxExp:
            self.maxExp += 10*self.level
            self.exp = 0
            self.level += 1
            self.totalHp += 20
            self.hp = self.totalHp
            self.baseAttack += 5
            print("You leveled up! You are now level {}, your base attack increased to {} and your HP increased to {}".format(self.level, self.baseAttack, self.totalHp))      

    #death check and gold loss
    def dead(self):
        if self.hp <= 0:
            goldLost = int(random.randrange(25, 50) / 100 * self.gold)
            self.gold -= goldLost
            self.hp = self.totalHp

            print("You died and lost {} gold!".format(goldLost))
            time.sleep(2)

            print("You wake up in a dark place.")

            return True
        return False

    #calculate the damage given to the enemy in a single turn of a battle
    def calcDamage(self, other):
        attack = self.calcAttack() 
        defense = other.defense
        dmg = random.randint(-int(attack / 10), int(attack / 10)) + attack - defense
        if dmg < 0:
            dmg = 0
        return dmg

    #here the player takes damage after the enemy's turn in a battle
    def getDamaged(self, enemy, dmg):
        self.hp -= dmg
        if type(enemy) is Boss.Boss:
            print("{} attacked you, dealing {} damage! {}/{} HP left.".format(enemy.name, dmg, self.hp, self.totalHp))
        else:
            print("The enemy attacked you, dealing {} damage! {}/{} HP left.".format(dmg, self.hp, self.totalHp))
        time.sleep(.5)

    #restore HP after the player drinks a health potion
    def drinkPotion(self):
        time.sleep(.2)
        if self.itemUses["Health Potion"] > 0:
            self.itemUses["Health Potion"] -= 1
            if self.hp + 100 > self.totalHp:
                self.hp = self.totalHp
            else:
                self.hp += 100
            print("You drank a Health Potion and now have {}/{} HP.".format(self.hp, self.totalHp))
        else:
            print("You do not have any Health Potions.")

    def printStats(self):
        print("Character name: {}".format(self.name))
        print("HP: {}/{}".format(self.hp, self.totalHp))
        print("Level {}. {}/{} experience.".format(self.level, self.exp, self.maxExp))
        print("Gold: {}".format(self.gold))
        print("Battles won: {}".format(self.battlesWon))
        print("Sword: level {}, {}-{} damage".format(self.eq["sword"], int(self.calcAttack() * 9 / 10), int(self.calcAttack() * 11 / 10)))
        print("Armor: level {}, {} defense".format(self.eq["armor"], self.calcDefense()))
        for item in self.itemUses:
            if self.itemUses[item] > 0:
                print("{}: {} uses left".format(item, self.itemUses[item]))