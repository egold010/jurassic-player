elementRelations = {
    "red": {
        "green": "strong",
        "blue": "weak"
    },
    "green": {
        "yellow": "strong",
        "red": "weak"
    },
    "yellow": {
        "blue": "strong",
        "green": "weak"
    },
    "blue": {
        "red": "strong",
        "yellow": "weak"
    },
    "unknown": {}
}

def ElementRelation(element1, element2):
    if element2 in elementRelations[element1]:
        return elementRelations[element1][element2]
    else:
        return "neutral"

class DumbAi: #dumbai just switches if at a disadvantage and spends all points on attack
    @staticmethod
    def GetMove(battle):
        pointsToSpend = battle.me.Points

        eRelations = [ElementRelation(dino.element, battle.enemy.Selected.element) for dino in battle.me.Dinosaurs]
        result = {"switch": False, "action": None}
        if eRelations[0] == "weak" or eRelations[0] == "neutral": #should try to switch
            for i in range(len(eRelations)):
                if eRelations[i] == "strong": #should immediately change if strong
                    result["switch"] = True
                    result["dinosaur"] = i
                    break
                elif eRelations[0] == "weak" and eRelations[i] == "neutral" and not "dinosaur" in result:
                    result["switch"] = True
                    result["dinosaur"] = i

        if result["switch"]:
            pointsToSpend -= 1

        result["action"] = {
            "attack": pointsToSpend,
            "block": 0,
            "save": 0
        }

        print("Action: " + str(result))

        return result