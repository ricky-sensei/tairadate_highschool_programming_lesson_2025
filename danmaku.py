import pyxel
pyxel.init(120, 120)
pyxel.load("danmaku.pyxres")

character = {
    "x": 120 / 2 - 16 / 2,
    "y": 90,
    "tama": []
}
enemy = {
    "x": 120 / 2 - 16 / 2,
    "y": 20,
    "direction": 1
}

    


def update():
    print(character["tama"])
    enemy["x"] = enemy["x"] + enemy["direction"]
    if enemy["x"] >= 120 - 16 or enemy["x"] <= 16:
        enemy["direction"] = enemy["direction"] * -1
    
    if pyxel.btn(pyxel.KEY_RIGHT) == True:
        character["x"] = character["x"] + 1
        
    elif pyxel.btn(pyxel.KEY_LEFT) == True:
        character["x"] = character["x"] - 1

    if pyxel.btnp(pyxel.KEY_SPACE) == True:
       character["tama"].append([character["x"], character["y"] - 16])

    for i in character["tama"]:
        i[1] = i[1] - 1
    
    


def draw():
    pyxel.cls(0)
    pyxel.blt(character["x"], character["y"], 0, 0, 0, 16, 16, 0)
    pyxel.blt(enemy["x"], enemy["y"], 0, 16, 0, 16, 16, 0)
    
    for i in character["tama"]:
        pyxel.blt(i[0], i[1], 0, 32, 0, 16, 16, 0)
    
    
pyxel.run(update, draw)
