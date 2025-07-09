import pyxel
from Character import *

class App:
    def __init__(self):
        pyxel.init(235, 235)
        self.table = Table(15, 15, 15)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            col = (mx - self.table.offset) // self.table.cell_size
            row = (my - self.table.offset) // self.table.cell_size
            self.table.toggle_cell(col, row)

    def draw(self):
        pyxel.cls(0)  # 背景黒
        self.table.draw()

App()