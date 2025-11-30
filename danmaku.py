import pyxel
pyxel.init(120, 120)
pyxel.load("danmaku.pyxres")

character = {
    "x": 120 / 2 - 16 / 2,
    "y": 90
}
enemy = {
    "x": 120 / 2 - 16 / 2,
    "y": 20,
    "direction": 1
}


def update():
    print()
    enemy["x"] = enemy["x"] + enemy["direction"]
    if enemy["x"] >= 120 - 16 or enemy["x"] <= 16:
        enemy["direction"] = enemy["direction"] * -1
    
    if pyxel.KEY_RIGHT == True:
        character["x"] = character["x"] + 1
        print("rifht")
    elif pyxel.KEY_LEFT == True:
        character["x"] = character["x"] - 1


        

def draw():
    pyxel.cls(0)
    pyxel.blt(character["x"], character["y"], 0, 0, 0, 16, 16, 0)
    pyxel.blt(enemy["x"], enemy["y"], 0, 16, 0, 16, 16, 0)

pyxel.run(update, draw)
