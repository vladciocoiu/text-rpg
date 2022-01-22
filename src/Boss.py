import time
import sys
import random

import Player
import Game
import Enemy

class Boss:
    def __init__(self, number):
        #initializing the boss depending on how many bosses the player has killed before
        if number == 1:
            self.name = "The Slime"
            self.hp = 200
            self.defense = 20
            self.attack = 30
            self.text = "You cannot defeat me, noob!"
            self.winningText = "I warned you." 
            self.defeatText = "I'm always the weakest one....."

        elif number == 2:
            self.name = "The Meme God"
            self.hp = 6900
            self.defense = 911
            self.attack = 420
            self.text = "My goals are beyond your understanding."
            self.winningText = "I could tell you my secret but, you wouldn't get it. " 
            self.defeatText = "Ok boomer."

        else:
            self.name = "Ciorap"
            self.hp = 99999
            self.defense = -1
            self.attack = 1
            self.text = "I'm not that great at this, please don't kill me!"
            self.winningText = "Well, maybe next time, sorry." 
            self.defeatText = "Okay you weren't supposed to defeat me. No, I'm not bad, shut up, this is definitely a bug."

    #death check
    def dead(self, player):
        if self.hp <= 0:
            print(self.defeatText)
            time.sleep(2)
            print("You have defeated {}!".format(self.name))
            time.sleep(2)
            player.bossesKilled += 1
            return True
        return False

    #damage done to the player
    def calcDamage(self, player):
        attack = self.attack 
        defense = player.calcDefense()
        dmg = random.randint(-int(attack/10), int(attack/10))+ attack - defense
        if dmg < 0:
            dmg = 0
        return dmg

    #damage done by the player to the boss
    def getDamaged(self, dmg):
        self.hp -= dmg
        print("You dealt {} damage to {}! {} HP left.".format(dmg, self.name, self.hp))
        time.sleep(.5)