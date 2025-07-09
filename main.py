import pyxel
from Character import *

class App:
    def __init__(self):
        pyxel.init(300, 235)
        self.table = Table(15, 15, 15)

        self.buttons = []

        # All Clearボタン作成
        clear_button = Button(
            x=240,
            y=50,
            w=50,
            h=40,
            label="All Clear",
            on_click=self.table.clear_all  # 関数を渡す
        )

        self.buttons.append(clear_button)

        pyxel.mouse(True)
        self.dragging = False          # ドラッグ中フラグ
        self.start_col = None          # ドラッグ開始セル（列）
        self.start_row = None          # ドラッグ開始セル（行）
        pyxel.run(self.update, self.draw)

    def update(self):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        col = (mx - self.table.offset) // self.table.cell_size
        row = (my - self.table.offset) // self.table.cell_size

    # --- ボタンの処理 ---
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for button in self.buttons:
                if button.handle_click(mx, my):
                    return  # ボタンが押された場合、ここで処理終了！

    # --- 以下はマスの処理 ---
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # ドラッグ開始
            self.dragging = True
            self.start_col = col
            self.start_row = row
            self.modified_cells = set()
            if 0 <= col < self.table.cols and 0 <= row < self.table.rows:
                self.table.toggle_cell(col, row)
                self.modified_cells.add((col, row))

        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.dragging:
            # ドラッグ中
            if 0 <= col < self.table.cols and 0 <= row < self.table.rows:
                if col == self.start_col:
                    r1, r2 = sorted([self.start_row, row])
                    for r in range(r1, r2 + 1):
                        if (col, r) not in self.modified_cells:
                            self.table.toggle_cell(col, r)
                            self.modified_cells.add((col, r))
                elif row == self.start_row:
                    c1, c2 = sorted([self.start_col, col])
                    for c in range(c1, c2 + 1):
                        if (c, row) not in self.modified_cells:
                            self.table.toggle_cell(c, row)
                            self.modified_cells.add((c, row))

        elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            # ドラッグ終了
            self.dragging = False
            self.start_col = None
            self.start_row = None
        

    def draw(self):
        pyxel.cls(0)
        self.table.draw()

        for button in self.buttons:
            button.draw()

App()