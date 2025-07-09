import pyxel

class Table:
    def __init__(self, cols, rows, cell_size):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        # 0 = 白、1 = 黒 の2次元リストを初期化
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def toggle_cell(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row][col] = 1 - self.grid[row][col]

    def draw(self):
        offset = 5
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + offset
                y = row * self.cell_size + offset
                color = 0 if self.grid[row][col] == 0 else 7
                pyxel.rect(x, y, self.cell_size, self.cell_size, color)
                pyxel.rectb(x, y, self.cell_size, self.cell_size, 13)



