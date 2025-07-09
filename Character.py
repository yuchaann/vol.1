import pyxel

class Table:
    def __init__(self, cols, rows, cell_size):
        self.cols = cols
        self.rows = rows
        self.offset = 5
        self.cell_size = cell_size
        # 0 = 白、1 = 黒 の2次元リストを初期化
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def toggle_cell(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row][col] = 1 - self.grid[row][col]

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.offset
                y = row * self.cell_size + self.offset
                color = 0 if self.grid[row][col] == 0 else 7
                pyxel.rect(x, y, self.cell_size, self.cell_size, color)
                pyxel.rectb(x, y, self.cell_size, self.cell_size, 13)
    
    def clear_all(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = 0  # 全部黒にする（1 = 黒）

    def generate_hints(self):
        # 行ヒント（row_hints）を作成
        self.row_hints = []
        for row in self.grid:
            hints = []
            count = 0
            for cell in row:
                if cell == 1:
                    count += 1
                elif count > 0:
                    hints.append(count)
                    count = 0
            if count > 0:
                hints.append(count)
            self.row_hints.append(hints if hints else [0])  # 空なら0入れる

        # 列ヒント（col_hints）を作成
        self.col_hints = []
        for col_index in range(self.cols):
            hints = []
            count = 0
            for row_index in range(self.rows):
                cell = self.grid[row_index][col_index]
                if cell == 1:
                    count += 1
                elif count > 0:
                    hints.append(count)
                    count = 0
            if count > 0:
                hints.append(count)
            self.col_hints.append(hints if hints else [0])


class Button:
    def __init__(self, x, y, w, h, label, on_click):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.on_click = on_click  # ボタン押下時に呼ばれる関数

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 8)  # ボタンの背景（灰色）
        pyxel.text(self.x + 5, self.y + self.h // 2 - 3, self.label, 7)  # ボタンの文字

    def handle_click(self, mx, my):
        if self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h:
            self.on_click()
            return True
        return False



