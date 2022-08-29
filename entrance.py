import pyxel
pyxel.init(160, 120)
    

class App:
    def __init__(self):
        # 初期化
        self.x = 0
        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):
        # 更新
        self.x = (self.x + 1) % pyxel.width
 
    def draw(self):
        # 描画
        # 画面を消去
        pyxel.cls(0)
        # 矩形を描画
        pyxel.rect(self.x, 0, self.x + 7, 7, 9)

App()