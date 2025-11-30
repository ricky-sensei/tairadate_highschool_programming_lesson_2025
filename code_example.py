import pyxel

character_info = {
    "x": 10,
    "y": 150,
    "jump": 10,
    "jump_status": False
}



pyxel.init(200, 200)
# character.pyxresファイルをロード(読み込み)
pyxel.load("character.pyxres")
def update():
    if character_info["jump"] == 10:
        if pyxel.btnp(pyxel.KEY_SPACE):
            character_info["jump_status"] = True
    
    if character_info["jump_status"] == True:
        character_info["y"] = character_info["y"] - character_info["jump"]
        if character_info["y"] > 150:
            character_info["y"] = 150
            character_info["jump_status"] = False
            character_info["jump"] = 10
        else:
            character_info["jump"] = character_info["jump"] - 1

        

def draw():
    pyxel.cls(0)
    # 画面上の（10, 10）の座標に、イメージバンクの0番目の画像のx＝０，　ｙ＝０の位置から、16x16ピクセルで表示
    pyxel.blt(character_info["x"], character_info["y"], 0, 0, 0, 16, 16)

pyxel.run(update, draw)
