import pyxel
from Character import *

class App:
    def __init__(self):
        pyxel.init(235, 235)
        self.table = Table(15, 15, 15)
        pyxel.mouse(True)
        self.dragging = False          # ドラッグ中フラグ
        self.start_col = None          # ドラッグ開始セル（列）
        self.start_row = None          # ドラッグ開始セル（行）
        pyxel.run(self.update, self.draw)

    def update(self):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        col = (mx - self.table.offset) // self.table.cell_size
        row = (my - self.table.offset) // self.table.cell_size

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # ドラッグ開始
            self.dragging = True
            self.start_col = col
            self.start_row = row
            self.modified_cells = set()  # 毎回リセット
            self.table.toggle_cell(col, row)
            self.modified_cells.add((col, row))

        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.dragging:
            # ドラッグ中
            if col == self.start_col:
                # 縦方向移動
                r1, r2 = sorted([self.start_row, row])
                for r in range(r1, r2 + 1):
                     if (col, r) not in self.modified_cells:
                        self.table.toggle_cell(col, r)
                        self.modified_cells.add((col, r))
            elif row == self.start_row:
                # 横方向移動
                c1, c2 = sorted([self.start_col, col])
                for c in range(c1, c2 + 1):
                    if (c, row) not in self.modified_cells:
                        self.table.toggle_cell(c, row)
                        self.modified_cells.add((c, row))
            # 斜め移動は何もしない（無視）

        elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            # ドラッグ終了
            self.dragging = False
            self.start_col = None
            self.start_row = None

    def draw(self):
        pyxel.cls(0)
        self.table.draw()

App()