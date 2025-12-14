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
    "direction": 1,
    "HP": 100
}


a_x = character["tama"][i][0]
        tama_y = character["tama"][i][1]
        # 当たり判定：弾と敵の矩形が重なっているかチェック
        if (
           def update():
    print(character["tama"])

    # 一番古い弾のデータをチェック
    if len(character["tama"]) and character["tama"][0][1] <= -16:
        character["tama"].pop(0)
    # 敵に当たった弾を削除
    for i in range(len(character["tama"]) - 1, -1, -1):
        tam tama_x < enemy["x"] + 16
            and tama_x + 16 > enemy["x"]
            and tama_y < enemy["y"] + 16
            and tama_y + 16 > enemy["y"]
        ):
            character["tama"].pop(i)

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
