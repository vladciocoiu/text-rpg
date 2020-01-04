import time
import sys
import random
import pickle

import Player
import Enemy


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
        self.gameLoop()

    #the character creation
    def createCharacter(self):
        name = str(input("What do you want your character's name to be?\n"))
        self.player = Player.Character(name)
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

    #the list of commands
    #TODO make a proper *list* of commands
    def helpMessage(self):
        print("'help', 'explore', 'drink potion', 'bossfight', 'upgrade gear', 'shop', 'stats', 'quit', 'save'\n")

    #this is where the player can upgrade his equipment
    def upgrade(self):
        for item in self.player.eq:
            print("{} - level {}. Cost {} gold.".format(item, self.player.eq[item], self.player.cost[item]) )
            time.sleep(.2)
        print("You have {} gold.".format(self.player.gold))
        time.sleep(.2)

        #this doesn't look too good and clean
        valid = False  
        sufficientGold = False 
        while not valid or not sufficientGold:
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

            if valid and self.player.gold >= self.player.cost[command]:
                sufficientGold = True

            if sufficientGold:
                self.player.eq[command] += 1
                self.player.gold -= self.player.cost[command]
                self.player.cost[command] = int(self.player.cost[command] * 1.75)
                print("You have successfully upgraded your {}".format(command))
                time.sleep(.2)
                self.upgrade()
            else:
                print("Insufficient gold.")
                time.sleep(.2)
    
    #a battle with a new enemy
    def battle(self):
        firstNamesList = ["A weird ", "An old ", "A fat ", "An angry ", "A nice "]
        secondNamesList = ["goblin", "dude", "tree", "rat", "wasp", "mosquito", "kid", "zombie", "programmer"]
        enemyName = firstNamesList[random.randint(0, len(firstNamesList)-1)] + secondNamesList[random.randint(0, len(secondNamesList)-1)]
        enemyLevel = self.player.level + random.randint(-2, 2)
        if self.player.level <= 3:
            enemyLevel = self.player.level

        enemy = Enemy.Enemy(enemyLevel, enemyName)

        if self.player.itemUses["Gold Magnet"] > 0:
            enemy.gold *= 2
        if self.player.itemUses["EXP Ring"] > 0:
            enemy.exp *= 2 

        print("{} jumped you!".format(enemy.name))
        time.sleep(.5)

        #the actual battle
        playersTurn = True
        while True:
            if self.player.dead():
                return
            if enemy.dead():
                if self.player.itemUses["Gold Magnet"] > 0:
                    self.player.itemUses["Gold Magnet"] -= 1
                self.player.gold += enemy.gold

                if self.player.itemUses["EXP Ring"] > 0:
                    self.player.itemUses["EXP Ring"] -= 1
                self.player.exp += enemy.exp
                
                self.player.battlesWon += 1

                return

            if playersTurn:
                playersTurn = False
                dmg = self.player.calcDamage(enemy)
                enemy.getDamaged(dmg)
            else:
                playersTurn = True
                dmg = enemy.calcDamage(self.player)
                self.player.getDamaged(dmg)

    #here the player can buy items that give him bonuses or health potions
    def shop(self):
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

        #same thing, doesn't look that clean
        valid = False
        sufficientGold = False
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
            if valid and self.player.gold >= itemsCost[command]:
                sufficientGold = True
            if sufficientGold:
                self.player.gold -= itemsCost[command]
                print(" You have bought a {}.".format(command))
                if command == "Health Potion":
                    self.player.itemUses[command] += 1
                else:
                    self.player.itemUses[command] += 10
            else:
                print("Insufficient gold.")

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

    #TODO boss battles

    #this is the main game loop, where the player chooses what to do
    def gameLoop(self):
        print("You wake up in a forest")
        while True:
            command = input()
            if command == 'quit':
                sys.exit()
            elif command == 'help':
                self.helpMessage()
            elif command == 'upgrade gear':
                self.upgrade()
            elif command == 'explore':
                self.explore()
            elif command == "stats":
                self.player.printStats()
            elif command == "shop":
                self.shop()
            elif command == "drink potion":
                self.player.drinkPotion()
            elif command == "save":
                self.saveCharacter()

