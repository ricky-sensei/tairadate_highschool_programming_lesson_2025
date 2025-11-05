import pyxel

character_info = {
    "x": 10
}

pyxel.init(200, 200)
# character.pyxresファイルをロード(読み込み)
pyxel.load("character.pyxres")
def update():
    character_info["x"] = character_info["x"] + 1

def draw():
    # 画面上の（character_info["x"], 10）の座標に、イメージバンクの0番目の画像のx＝０，　ｙ＝０の位置から、16x16ピクセルで表示
    pyxel.blt(character_info["x"], 10, 0, 0, 0, 16, 16)

pyxel.run(update, draw)

