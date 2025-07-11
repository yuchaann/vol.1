import pyxel
from Character import *

class App:
    def __init__(self):
        pyxel.init(500, 400, display_scale=2)
        self.table = Table(15, 15, 15)
        self.cleared = False
        self.has_solution = False
        self.showing_answer = False

        self.mistakes = []
        self.buttons = []
        
        show_button = Button(
            x=400,
            y=230,
            w=50,
            h=40,
            label="Show",
            on_click=self.toggle_answer)

        self.buttons.append(show_button)

        # All Clearボタン作成
        clear_button = Button(
            x=400,
            y=50,
            w=50,
            h=40,
            label="All Clear",
            on_click=self.table.clear_all  # 関数を渡す
        )

        self.buttons.append(clear_button)

        translate_button = Button(
            x=400,
            y=110,
            w=50,
            h=40,
            label="Translate",
             on_click=self.on_translate
        )
        self.buttons.append(translate_button)

         # Answerボタン
        answer_button = Button(
            x=400,
            y=170,
            w=50,
            h=40,
            label="Answer",
            on_click=self.on_answer
        )
        self.buttons.append(answer_button)

        pyxel.mouse(True)
        self.dragging = False          # ドラッグ中フラグ
        self.start_col = None          # ドラッグ開始セル（列）
        self.start_row = None          # ドラッグ開始セル（行）
        pyxel.run(self.update, self.draw)

    def update(self):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            col = (mx - self.table.offset_x) // self.table.cell_size
            row = (my - self.table.offset_y) // self.table.cell_size

            # ボタンの処理（先に処理しとく）
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                for button in self.buttons:
                    if button.handle_click(mx, my):
                        return  # ボタン押されたらここで終了

            # 左クリックドラッグで塗る
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.dragging = True
                self.drag_button = 'left'
                self.start_col = col
                self.start_row = row
                self.modified_cells = set()
                if 0 <= col < self.table.cols and 0 <= row < self.table.rows:
                    self.table.toggle_cell(col, row)
                    self.modified_cells.add((col, row))
                    self.has_solution = False

            elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.dragging and self.drag_button == 'left':
                if 0 <= col < self.table.cols and 0 <= row < self.table.rows:
                    if col == self.start_col:
                        r1, r2 = sorted([self.start_row, row])
                        for r in range(r1, r2 + 1):
                            if (col, r) not in self.modified_cells:
                                self.table.toggle_cell(col, r)
                                self.modified_cells.add((col, r))
                                self.has_solution = False
                    elif row == self.start_row:
                        c1, c2 = sorted([self.start_col, col])
                        for c in range(c1, c2 + 1):
                            if (c, row) not in self.modified_cells:
                                self.table.toggle_cell(c, row)
                                self.modified_cells.add((c, row))
                                self.has_solution = False

            # 右クリックドラッグで×印つける
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                self.dragging = True
                self.drag_button = 'right'
                self.start_col = col
                self.start_row = row
                self.modified_cells = set()
                if 0 <= col < self.table.cols and 0 <= row < self.table.rows:
                    self.table.toggle_mark(col, row)
                    self.modified_cells.add((col, row))
                    self.has_solution = False

            elif pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) and self.dragging and self.drag_button == 'right':
                if 0 <= col < self.table.cols and 0 <= row < self.table.rows:
                    if col == self.start_col:
                        r1, r2 = sorted([self.start_row, row])
                        for r in range(r1, r2 + 1):
                            if (col, r) not in self.modified_cells:
                                self.table.toggle_mark(col, r)
                                self.modified_cells.add((col, r))
                                self.has_solution = False
                    elif row == self.start_row:
                        c1, c2 = sorted([self.start_col, col])
                        for c in range(c1, c2 + 1):
                            if (c, row) not in self.modified_cells:
                                self.table.toggle_mark(c, row)
                                self.modified_cells.add((c, row))
                                self.has_solution = False

            # ドラッグ終了判定
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT):
                self.dragging = False
                self.drag_button = None
                self.start_col = None
                self.start_row = None

            # クリア判定してるフラグを使った処理
            if self.cleared and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_game()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, f"Misses: {self.table.miss_count}", 7)

        if self.cleared is True:
            # print("クリアしとります")
            pyxel.text(250, 200, "CLEAR!", pyxel.frame_count % 30)
            pyxel.text(250, 240, "Click to restart", 15)
        else:
            self.table.draw()
            for button in self.buttons:
                button.draw()

    def reset_game(self):
        self.table.clear_all()
        self.cleared = False
        self.has_solution = False  # 追加
        self.table.row_hints = [[0] for _ in range(self.table.rows)]  # ← 行の数だけ0入れておく
        self.table.col_hints = [[0] for _ in range(self.table.cols)]  # ← 列も同様

    def on_translate(self):
        self.table.set_solution_from_grid()  # 正解を保存
        self.table.generate_hints()
        self.table.clear_all()               # 盤面リセット（全部黒）
        self.cleared = False
        self.has_solution = True

    def on_answer(self):
        self.table.evaluate_mistakes()
        if self.table.is_cleared():
            self.cleared = True
            print("クリア！")
        else:
            print(f"ミスがあります。ミス数: {self.table.miss_count}")

    def toggle_answer(self):
        self.showing_answer = not self.showing_answer
        self.table.set_show_answer(self.showing_answer)
App()