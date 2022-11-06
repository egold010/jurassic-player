import pyautogui, PIL, mouse, time, pytesseract, re, json, threading
from PIL import Image, ImageGrab
from Minimax import DumbAi

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
pyautogui.FAILSAFE = True
game = False

#CONFIG
pvp = True
dnaWatch = False
skipAd = True

posDict = json.load(open("Positions.json"))
def wait(delay):
    time.sleep(delay)

def click(pos):
    pyautogui.click(*tuple(pos))
    wait(.1)

class Dinosaur:
    def __init__(self, health, damage, element):
        if health <= 0 or element == "unknown":
            self.exists = False
        else:
            self.health = health
            self.damage = damage
            if element[0] > 100 and element[1] < 100 and element[2] < 100:
                self.element = "red"
            elif element[0] < 100 and element[1] > 100 and element[2] < 100:
                self.element = "green"
            elif element[0] > 100 and element[1] > 100 and element[2] < 100:
                self.element = "yellow"
            elif element[0] < 100 and element[1] > 100 and element[2] > 100:
                self.element = "blue"

    def GetInfo(self):
        return "{Health: " + str(self.health) + ", Damage: " + str(self.damage) + ", Element: " + str(self.element) + "}"

    exists = True
    health = -1
    damage = -1
    element = "unknown"

class Participant:
    def Print(self):
        [print("Dinosaur " + self.Dinosaurs[i].GetInfo()) for i in range(len(self.Dinosaurs)) if self.Dinosaurs[i].exists]
        print("Points: " + str(self.Points) + "\n")

    def Update(self, info):
        self.Dinosaurs = [Dinosaur(info["health" + str(i)], info["damage" + str(i)], info["element" + str(i)]) for i in range(1, 4)]
        for dino in self.Dinosaurs:
            if not dino.exists:
                self.Dinosaurs.remove(dino)
        self.Selected = self.Dinosaurs[0]
        self.Points = info["points"]

    Dinosaurs:list
    Selected:Dinosaur
    Points:int
    SavedPoints = 0

class Battle:
    me = Participant()
    enemy = Participant()
    meFirst = True #if mefirst, enemy turn should end at start of player turn
    turn = 0

    def Update(self):
        self.me.Update(getPlayerInfo(posDict["me"]))
        self.enemy.Update(getPlayerInfo(posDict["enemy"]))
    
    def Print(self):
        print("My dinosaurs")
        self.me.Print()
        print("Enemy dinosaurs")
        self.enemy.Print()

    def IsMyTurn(self):
        window = ImageGrab.grab(bbox=(posDict["window"])).load()
        save = window[tuple(posDict["save"])]
        block = window[tuple(posDict["block"])]
        attack = window[tuple(posDict["attack"])]
        return save[0] > 100 and block[2] > 150 and attack[0] > 150

    def PutEnemyTurn(self, attack, block):
        #turn is defined by dealing an attack and recieving an attack
        points = 0
        if self.turn == 1 and self.meFirst:
            points = 2
        else:
            points += self.turn if self.turn < 4 else 4
        points += self.enemy.SavedPoints
        points -= attack
        points -= block
        self.enemy.SavedPoints = points
        print()

    def ProcessAction(self, action):
        if action["switch"]:
            click(posDict["expand"])
            click(posDict["switch" + str(action["dinosaur"])])
            wait(3)
        for key in action["action"]:
            for i in range(action["action"][key]):
                click(posDict[key])

def getPlayerInfo(posInfo):
    result = {}
    for key in posInfo:
        if "element" in key:
            result[key] = ImageGrab.grab().load()[posInfo[key][0], posInfo[key][1]]
        else:
            org = ImageGrab.grab(bbox=(posInfo[key]))
            concat = Image.open("concat.png")
            org = org.resize((int(org.width * concat.height * 1.2 / org.height), concat.height))
            im = Image.new(mode="RGB", size=(org.width + concat.width, org.height))

            im.paste(concat)
            im.paste(org, (concat.width, 0))
            im = im.crop((160,0,im.width,im.height))

            for x in range(im.width):
                for y in range(im.height):
                    color = im.getpixel((x, y))
                    if sum(color) > 500 or color[0] > 200 or color[1] > 200:
                        im.putpixel((x, y), (255,255,255))
                    else:
                        im.putpixel((x, y), (1, 1, 1))

            toStr = pytesseract.image_to_string(im, config='--psm 10') #-c tessedit_char_whitelist=0123456789oOlLiI
            print(key + ": " + toStr.rstrip())
            toStr = toStr[4:] if len(toStr) > 4 else ""
            toStr = re.sub('[oO]', '0', toStr)
            toStr = re.sub('[\|lLiI]', '1', toStr)
            toStr = re.sub('[\[\]\|[\\\\]]', '1', toStr)
            toStr = re.sub('[A]', '4', toStr)
            toStr = re.sub('[g]', '8', toStr)
            toStr = re.sub('[\?/]', '7', toStr)
            toStr = ''.join(re.findall("[0-9]", toStr))
            result[key] = -1 if toStr == '' else int(toStr)
            im.save('C:\\Users\\Evan Goldman\\Downloads\\' + key + r'.png')
    return result

battle = Battle()
game = True

enemyActionQueue = {
    "attack": 0,
    "block": 0
}
def EnemyActionListener():
    while game:
        #screenshot and check if enemy made an action and queue to enemyActionQueue
        wait(.1)

def WatchAd():
    #wait for ad to finish (variable time)
    #wait(20)
    #close ad
    wait(5)
    while True:
        im = ImageGrab.grab(bbox=(posDict["closeAdRegion"]))
        for x in range(im.width):
            for y in range(im.height):
                color = im.getpixel((x, y))
                if sum(color) > 500:
                    im.putpixel((x, y), (255,255,255))
                else:
                    im.putpixel((x, y), (1, 1, 1))
        im.save('C:\\Users\\Evan Goldman\\Downloads\\close.png')
        result = pytesseract.image_to_string(im, config='--psm 10 -c tessedit_char_whitelist=xX»').lower().rstrip()
        if result != "":
            print(result)
        if 'x' in result or result == '»':
            click(posDict["closeAd"])
            if result != '»':
                break
        wait(1)
    wait(3)

if dnaWatch:
    while True:
        click(posDict["dnaMenu"])
        wait(.5)
        click(posDict["dnaWatch"])
        WatchAd()

while True: #infinite loop
    if not skipAd:
        #press menu and go to battle screen
        click(posDict["menu"])
        wait(1)
        click(posDict["pvp" if pvp else "pve"])
        wait(1)
        click(posDict["challenge"])
        wait(1)
        #for first 3 dinosaurs
        selectedDinos = 0
        repeat = True
        while repeat:
            for i in range(7):
                pix = ImageGrab.grab().load()[posDict["dino1"][0] + posDict["dinoOffset"] * i, posDict["dino1"][1]]
                """
                while pix[1] / sum(pix) >= .5 or pix[2] / sum(pix) >= .5:
                    click([posDict["dino1"][0] + posDict["dinoOffset"] * i, posDict["dino1"][1]])
                    wait(1)
                    if pix[2] / sum(pix) >= .5:
                        click(posDict["confirmAd"])
                        WatchAd()
                    pix = ImageGrab.grab().load()[posDict["dino" + str(i)][0], posDict["dino" + str(i)][1]]
                click([posDict["dino1"][0] + posDict["dinoOffset"] * i, posDict["dino1"][1]])
                """
                if pix[2] / sum(pix) < .5:
                    wait(1)
                    click([posDict["dino1"][0] + posDict["dinoOffset"] * i, posDict["dino1"][1]])
                    selectedDinos += 1
                    if selectedDinos == 3:
                        break
            repeat = selectedDinos < 3

        wait(1)
        click(posDict["start"])
        if pvp:
            WatchAd()
    
    while game:
        print("waiting for turn")
        while not battle.IsMyTurn():
            #check for game over
            wait(1)
        if not game:
            break

        battle.turn += 1

        battle.PutEnemyTurn(enemyActionQueue["attack"], enemyActionQueue["block"])
        enemyActionQueue["attack"] = 0
        enemyActionQueue["block"] = 0

        click(posDict["expand"])
        battle.Update()
        battle.Print()
        click(posDict["expand"])

        if battle.turn == 1:
            battle.meFirst = battle.me.Points == 1
        
        #determine and make action
        action = DumbAi.GetMove(battle)
        battle.ProcessAction(action)

    if pvp:
        #claim pvp reward
        pass
    else:
        #claim ai reward
        pass

    break #temp