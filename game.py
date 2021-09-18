import random
import math
import os
player = [100,3,-1,0,[1,1,1,0],[False]] #[hp,potions,rounds,gold,level]
enemy = [0]
difficluty = -1
name = ["Novice", "Easy" , "Normal" , "Hard", "Expert", "Impossible"]
dmg = [[30,25,20,16,14,8],[8,14,20,28,36,50]]
hp = [[200,180,160,135,100,60],[100,120,140,165,190,300]]
potion = [7,5,3,3,2,1]
eb = 1.05
mi = [8,6,4,0,0,0]

def init():
    global player
    global enemy
    player[0] = hp[0][difficluty]*hmul()
    player[1] = potion[difficluty]
    enemy = [int(hp[1][difficluty] * ( eb ** (player[2] ** 2))/player[4][1])]

def init2():
    global player
    global enemy
    player[0] = hp[0][difficluty]*hmul()
    player[1] = potion[difficluty]
    player[2] = -1
    player[4] = [1,1,1,0]
    enemy = [int(hp[1][difficluty])]

def start():
    global difficluty
    global enemy
    global player
    print("What difficulty do you want to start on?")
    print("1. Novice")
    print("2. Easy")
    print("3. Normal")
    print("4. Hard")
    print("5. Expert")
    a = input("> ").lower()
    if "novice" in a or a == "1":
        difficluty = 0
    elif "easy" in a or a == "2":
        difficluty = 1
    elif "normal" in a or a == "3":
        difficluty = 2
    elif "hard" in a or a == "4":
        difficluty = 3
    elif "expert" in a or a == "5":
        difficluty = 4
    elif "impossible" in a or a == "6":
        difficluty = 5
    else: 
        print("difficluty not recognized")
        start2()
    print("good choice")
    print("on " + name[difficluty] +" mode")
    print("you stats are " + str(dmg[0][difficluty]) + " dmg and " + str(hp[0][difficluty] * hmul()) + " hp")
    print("and also you start with " + str(potion[difficluty]) + " potions")
    print("enemy stats are " + str(dmg[1][difficluty]) + " dmg and " + str(hp[1][difficluty]) + " hp")
    init()
    return

def pscreen():
    j = ""
    global player
    print("------------------------------------------")
    print("Round " + str(player[2] + 1))
    print("                                 Enemy")
    print("                             Hp: " + str(int(enemy[0])) + "/" + str(int(hp[1][difficluty] *  eb ** (player[2] ** 2) / (player[4][1]))))
    print("")
    print("")
    print("     You")
    print("Hp: " + str(int(player[0])) + "/" + str(int(hp[0][difficluty] * hmul())) + " dmg: " + str(int(dmg[0][difficluty]* player[4][0])) + " gold: " + str(player[3]))
    print("You have " + str(player[1]) + " potions") 
    print("------------------------------------------")
    return att()

def att():
    print("Type")
    print("1 to do 1x dmg with 100%c chance" % "%")
    print("2 to do 1.5x dmg with 80%c chance" % "%")
    print("3 to do 2.5x dmg with 60%c chance" % "%")
    print("4 to do 20x dmg with 6%c chance" % "%")
    print("5 to use 1 potion to heal for 50 hp")
    print("break to close the game")
    while  not j.isnumeric() and j != 'break':
        j = input("> ")
    if j == 'break':
        return [-1,-1]
    j = int(j)
    dm = [0,0]
    if random.random() < ( 0.75 + difficluty * 0.05 + player[2] * 0.01 - player[4][3] * 0.25):
        dm[0] = int(dmg[1][difficluty] * ( 0.7 + random.random() * 0.6) * ( eb ** (player[2] ** 2)))
        print("The enemy attacks for " + str(dm[0]) + " damage")
    else:
        dm[0] = 0
        print("The enemy misses")
    dm[1] = int(dmg[0][difficluty] * player[4][0])
    print("")
    if j == 2:
        if random.random() < 0.8:
            dm[1] *= 1.5
        else:
            dm[1] = 0
    elif j == 3:
        if random.random() < 0.6:
            dm[1] *= 2.5
        else:
            dm[1] = 0
    elif j == 4:
        if random.random() < 0.06:
            dm[1] *= 20  
        else:
            dm[1] = 0
    elif j == 5:
        dm[1] = 0
        if player[1] > 0:    
            if difficluty == 5:
                print("You full healed")
                player[0] = 60
                player[1] -= 1
            else:
                player[0] += 50
                player[1] -= 1
                if player[0] > hmax():
                    player[0] = hmax()
                    print("You full healed")
                else:
                    print("You healed 50 hp")
        else:
            print("You don't have potions and wasted a turn")
        return dm
    elif j == 6:
        if random.random() < 0.001:
            dm[1] = 2 ** 1023
        else:
            dm[1] = 0
    else:
        print("You have no idea what you did")
        dm[1] = 0
    if dm[1] == 0:
        print("You missed")
    else:
        print("You did " + str(dm[1]) + " damage to the enemy")
    return dm


def loop():
    global player
    global enemy
    a = pscreen()
    if a == [-1,-1]:
        return -1
    player[0] -= a[0]
    if player[0] <= 0:
        return
    enemy[0] -= a[1]
    return

def game():
    a = 0
    while player[0] > 0 and enemy[0] > 0 and a != -1:
        a = loop()
    if a == -1:
        return 2
    if enemy[0] <= 0:
        return 1
    else:
        return 0

def r():
    global player
    start()
    a = 1
    while a == 1:
        player[2] += 1
        init()
        a = game()
        if a == 0 or a == 2:
            break
        gain()
    if a == 2:
        return -1
    if player[2] > mi[difficluty]:
        g = difficluty ** 2 * player[2]
    else:
        g = 0
    print("You got to round " + str(player[2]) + " on " + name[difficluty] + " good job")
    print("And you also got " + str(g) + " gold" )
    return g

def rgame():
    global player
    load()
    while True:
        g = r()
        if g == -1:
            break
        player[3] = player[3] + g
        save()
        pscreen2()
        save()
        init2()

def start2():
    global difficluty
    print("What difficulty do you want to start on?")
    print("1. Novice")
    print("2. Easy")
    print("3. Normal")
    print("4. Hard")
    print("5. Expert")
    a = input("> ").lower()
    if "novice" in a or a == "1":
        difficluty = 0
    elif "easy" in a or a == "2":
        difficluty = 1
    elif "normal" in a or a == "3":
        difficluty = 2
    elif "hard" in a or a == "4":
        difficluty = 3
    elif "expert" in a or a == "5":
        difficluty = 4
    elif "impossible" in a or a == "6":
        difficluty = 5
    else: 
        print("difficluty not recognized")
        start2()
    return

def gain():
    global eb
    a = ""
    q = 1.1 + player[2] / 7.5
    if q > 1.5:
        q = ( q / 1.5 ) ** 0.75 * 1.5
    if q > 2:
        q = math.log(q) / math.log(2) * 2
    if q > 3:
        q = ( q / 3 ) ** 0.25 * 3,1
    q = rk(q,2)
    print("Choose an upgrade to get")
    print("Type 1 to multiply your damage by " + str(q))
    print("Type 2 to divide enemy hp by " + str(q))
    print("Type 3 to multiply your hp by " + str(q))
    if player[2] % 5 == 0 and player[2] > 0:
        print("Type 4 to reduce enemy scaling")
    while not a.isnumeric():
        a = input("> ")
    a = int(a)
    if a == 1:
        player[4][0] *= q
    elif a == 2:
        player[4][1] *= q
    elif a == 3:
        player[4][2] *= q
    elif a == 4 and player[2] % 5 == 0 and player[2] > 0:
        eb -=   0.05 / (( 1 + player[4][3] / 2 ) ** 2 ) / ( (2 * math.pi ** 2 - 6) / 3 )
        print("You were dumb and did nothing")
    return

def rk(a,b):
    a *= 10 ** b
    a = round(a)
    a /= 10 ** b
    return a

def cf():
    return os.path.exists("game.txt")

def save():
    pq = open("game.txt","w")
    pq.write(str(player[3])+"\n")
    if player[5][0]:
        pq.write("1" + "\n")
    else:
        pq.write("0" + "\n")

def load():
    if cf():
        fi = open("game.txt")
        a = fi.readlines()
        a[0] = int(a[0])
        player[3] = a[0]
        if a[1] == "1\n":
            player[5][0] = True
        return
    else:
        return

def pscreen2():
    a = "a"
    print("------------------------------------------")
    print("Welcome to the shop.")
    print("Type the upgrade number to buy it")
    print("Type any other number to leave")
    print("You have " + str(player[3]) + " gold")
    print("------------------------------------------")
    print("Upgrade 1: You have 50% more hp")
    if player[5][0]:
        print("Cost: 100 gold [Bought]")
    else:
        print("Cost: 100 gold")
    print("------------------------------------------")
    while not a.isnumeric():
        a = input("> ")
    if a == "1":
        buy(1)
    print("see you next time")

def hmul():
    ret = 1
    ret *= player[4][2]
    if player[5][0]:
        ret *= 1.5
    return ret

def hmax():
    return hp[0][difficluty] * hmul()

def buy(a):
    global player
    if a == 1 and player[3] >= 100:
        player[3] -= 100
        player[5][0] = True
        print("Hp increased by 50%")
        return


rgame()