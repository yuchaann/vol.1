import pyxel

class Table:
    def __init__(self, cols, rows, cell_size):
        # 既存の初期化コード
        self.cols = cols
        self.rows = rows
        self.offset_x = 130
        self.offset_y = 130
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # ここで正解用の2次元リストも用意（初期は全部0でOK）
        self.solution = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def is_cleared(self):
        return self.grid == self.solution
    
    def set_solution_from_grid(self):
        # gridの状態をsolutionにコピーする
        self.solution = [row[:] for row in self.grid]

    def toggle_cell(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row][col] = 1 - self.grid[row][col]

    def draw(self):
        pyxel.cls(0)

        max_hint = 8  # 7→8に変更

        # 行ヒント（左）
        for row in range(self.rows):
            hints = self.row_hints[row] if hasattr(self, 'row_hints') else []
            for i in range(max_hint):
                x = self.offset_x - (max_hint - i) * self.cell_size
                y = self.offset_y + row * self.cell_size
                pyxel.rect(x, y, self.cell_size, self.cell_size, 1)  # 空マス背景
                if i < len(hints):
                    pyxel.text(x + 3, y + 4, str(hints[i]), 7)

        # 列ヒント（上）
        for col in range(self.cols):
            hints = self.col_hints[col] if hasattr(self, 'col_hints') else []
            for i in range(max_hint):
                x = self.offset_x + col * self.cell_size
                y = self.offset_y - (max_hint - i) * self.cell_size
                pyxel.rect(x, y, self.cell_size, self.cell_size, 1)  # 空マス背景
                if i < len(hints):
                    pyxel.text(x + 3, y + 4, str(hints[i]), 7)

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y
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



