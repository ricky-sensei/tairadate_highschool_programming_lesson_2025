import pyxel

# pyxelを初期化：画面のサイズを２００ｘ２００ピクセルに設定
pyxel.init(200, 200)

# 四角に関する情報を定義
rect_info = {
    "x": 10,
    "y": 10,
    "w": 100,
    "h": 100,
    "col": 7
}

# update関数：四角を移動する処理をする
def update():
    rect_info["x"] = rect_info["x"] + 1

# draw関数：四角を描画する
def draw():
    # 背景色を黒にする
    pyxel.cls(0)
    # 四角を描画
    pyxel.rect(rect_info["x"], rect_info["y"], rect_info["w"], rect_info["h"], rect_info["col"])

pyxel.run(update, draw)

