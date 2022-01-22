import time
import sys
import random
import pickle
import os

import Player
import Enemy
import Boss


#the game class that uses all the other classes
class Game:
    def __init__(self):
        self.player = None

    #the load/new game screen
    def begin(self):
        print("Hi! Do you want to start a 'new game' or 'load' your character?")
        command = input()

        while command != 'new game' and command != 'load':
            print("Invalid command. Please type 'new game' or 'load'.")
            command = input()

        if command == 'new game':
            self.createCharacter()
        else:
            self.loadCharacter()

    #saves the character class to a save file
    def saveCharacter(self):
        path = "./saves/{}.save".format(self.player.name)

        if not os.path.exists('./saves'):
            os.makedirs('./saves')

        with open(path, "wb+") as file:
            pickle.dump(self.player, file)
        print("Character successfully saved to {}".format(path))

    #loading the character from a save file
    def loadCharacter(self):
        print("Please tell me the name of your saved character or type 'new game' if you want to create a new one.")
        while(self.player == None):
            name = input()

            if name == 'new game':
                self.createCharacter()
                return

            try:
                with open("./saves/{}.save".format(name), "rb") as file:
                    self.player = pickle.load(file)
            except:
                print("Invalid name. Try again or type 'new game' to create a new character.")
                time.sleep(.5)

        print("Welcome back, {}!".format(self.player.name))
        time.sleep(.5)
        
        self.gameLoop()

    #the character creation
    def createCharacter(self):
        name = str(input("What do you want your character's name to be?\n"))
        self.player = Player.Player(name)
        print("Cool! Hi, {}!".format(self.player.name))
        time.sleep(1)

        self.intro()

    #a short description of the game
    def intro(self):
        sentences = [
            "I'm Ciorap, the creator of this game",
            "This is a small text RPG made for fun",
            "The goal of the game is to beat all the bosses",
            "You can do this by leveling up, getting gold and buying better gear",
            "Whenever you need help with the actions in this game, you can simply type 'help' and the list of available actions will appear",
            "That's it. Good luck now!"
        ]

        for sentence in sentences:
            print(sentence)
            time.sleep(2)

        self.gameLoop()

    #this is where the player can upgrade his equipment
    def upgrade(self):
        for item in self.player.eq:
            print("{} - level {}. Cost {} gold.".format(item, self.player.eq[item], self.player.cost[item]) )
            time.sleep(.2)
        print("You have {} gold.".format(self.player.gold))
        time.sleep(.2)

        valid = False  
        while True:
            print("Type the name of the item you wish to upgrade or 'return' if you want to return to the game.")
            command = str(input())
            if command == 'return':
                return
            for item in self.player.eq:
                if command == item:
                    valid = True
            if not valid:
                print("Invalid command.")
                time.sleep(.2)
                continue

            upgraded = False
            if self.player.gold >= self.player.cost[command]:
                self.player.eq[command] += 1
                self.player.gold -= self.player.cost[command]
                self.player.cost[command] = int(self.player.cost[command] * 1.75)
                print("You have successfully upgraded your {}".format(command))
                upgraded = True
            else:
                print("Insufficient gold.")
            time.sleep(.5)

            if upgraded:
                self.upgrade()
                break

    
    #a method that initializes a new enemy based on the player's level
    def getEnemy(self):
        firstNamesList = ["A weird ", "An old ", "A fat ", "An angry ", "A nice "]
        secondNamesList = ["goblin", "dude", "tree", "rat", "wasp", "mosquito", "kid", "zombie", "programmer"]

        enemyName = random.choice(firstNamesList) + random.choice(secondNamesList)
        enemyLevel = self.player.level + random.randint(-2, 2)
        if self.player.level <= 3:
            enemyLevel = self.player.level

        ret = Enemy.Enemy(enemyLevel, enemyName)

        if self.player.itemUses["Gold Magnet"] > 0:
            ret.gold *= 2
            self.player.itemUses["Gold Magnet"] -= 1

        if self.player.itemUses["EXP Ring"] > 0:
            self.player.itemUses["EXP Ring"] -= 1
            ret.exp *= 2 

        return ret

    #a battle with a new enemy
    def battle(self):
        enemy = self.getEnemy()

        print("{} jumped you!".format(enemy.name))
        time.sleep(.5)

        #the actual battle
        playersTurn = True
        while True:
            if self.player.dead() or enemy.dead(self.player):
                return

            if playersTurn:
                playersTurn = False
                dmg = self.player.calcDamage(enemy)
                enemy.getDamaged(dmg)
            else:
                playersTurn = True
                dmg = enemy.calcDamage(self.player)
                self.player.getDamaged(enemy, dmg)

    #here the player can buy items that give him bonuses or health potions
    def shop(self, showMessage):
        if showMessage:
            print("Hi! I'm the merchant. I sell stuff. Take a look.")
            time.sleep(1)

        #the descriptions of the items
        itemsList = {
            "Health Potion": "Heals you 100 HP.",
            "EXP Ring": "Gives you 2x Experience Points for the next 10 battles.",
            "Gold Magnet": "Gives you 2x gold for the next 10 battles."
        }

        itemsCost = {
            "Health Potion": 5,
            "EXP Ring": 20, 
            "Gold Magnet": 50
        }

        for item in itemsList:
            print ("{}: {} (costs {} gold)".format(item, itemsList[item], itemsCost[item]))
            time.sleep(.5)

        valid = False
        while True:
            print("Type the name of the item you wish to buy or 'return' if you want to get back to the game.")
            time.sleep(.2)
            command = str(input())

            if command == 'return':
                return

            for item in itemsList:
                if command == item:
                    valid = True
            if not valid:
                print("Invalid command.")
                time.sleep(.5)
                continue

            bought = False
            if self.player.gold >= itemsCost[command]:
                self.player.gold -= itemsCost[command]
                print(" You have bought a {}.".format(command))
                bought = True
                if command == "Health Potion":
                    self.player.itemUses[command] += 1
                else:
                    self.player.itemUses[command] += 10
            else:
                print("Insufficient gold.")
            time.sleep(.5)

            if bought:
                self.shop(False)
                break

    def explore(self):
        #a random number that decides what is going to happen
        prob = random.randint(1, 100)
        if prob <= 10:
            randomGold = random.randint(self.player.level, self.player.level*2)
            self.player.gold += randomGold
            print("You found some gold! Now you have {} gold.".format(self.player.gold))
        elif prob <= 40:
            print("Found nothing.")
        else:
            self.battle()
            self.player.levelUp()

    #pretty much identical to the enemy battle
    def bossBattle(self):
        boss = Boss.Boss(self.player.bossesKilled+1)

        print("{} is approaching you!".format(boss.name))
        time.sleep(2)
        print(boss.text)
        time.sleep(2)

        playersTurn = True

        while True:
            if self.player.dead() or boss.dead(self.player):
                return

            if playersTurn:
                playersTurn = False
                dmg = self.player.calcDamage(boss)
                boss.getDamaged(dmg)
            else:
                playersTurn = True
                dmg = boss.calcDamage(self.player)
                self.player.getDamaged(boss, dmg)

    #if the player has defeated the last boss
    def end(self):
        for i in range(1, 4):
            print("You have completed the game! Thanks for playing!")
            time.sleep(.5)
        time.sleep(2)
        sys.exit()


    #this is the main game loop, where the player chooses what to do
    def gameLoop(self):
        commandsList = ['help', 'explore', 'drink potion', 'boss battle', 'upgrade gear', 'shop', 'stats', 'quit', 'save']

        while True:
            if self.player.bossesKilled == 3:
                self.end()

            command = input()

            if command not in commandsList:
                print("Invalid command. Type 'help' for the list of commands.")
                continue

            if command == 'quit':
                sys.exit()

            elif command == 'help':
                for com in commandsList:
                    print("'{}'".format(com), end = " ")
                print()

            elif command == 'upgrade gear':
                self.upgrade()

            elif command == 'explore':
                self.explore()

            elif command == "stats":
                self.player.printStats()

            elif command == "shop":
                self.shop(True)

            elif command == "drink potion":
                self.player.drinkPotion()

            elif command == "save":
                self.saveCharacter()

            elif command == "boss battle":
                self.bossBattle()

            if command == "upgrade gear" or command == "shop":
                print("You returned to the dark place.")


