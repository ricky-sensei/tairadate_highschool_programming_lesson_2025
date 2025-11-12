import pyxel
pyxel.init(120, 120)
pyxel.load("danmaku.pyxres")

def update():
    pass
def draw():
    pyxel.bltm()
pyxel.run(update, draw)

