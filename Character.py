import pyxel
from ortools.sat.python import cp_model

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

        self.marks = [[0 for _ in range(cols)] for _ in range(rows)]  # ×マーク状態
        self.miss_count = 0  # ミス数
        self.mistakes = []  # ここで追加！mistakesの初期化
    
    def is_cleared(self):
        if all(cell == 0 for row in self.grid for cell in row):
            return False  # 盤面が空ならクリアじゃない
        return self.grid == self.solution
    
    def set_solution_from_grid(self):
        # gridの状態をsolutionにコピーする
        self.solution = [row[:] for row in self.grid]

    def toggle_cell(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            if self.marks[row][col] == 1:
                return  # ×がある場合は何もしない
            self.grid[row][col] = 1 - self.grid[row][col]
            
            if self.grid[row][col] == 1:
                self.marks[row][col] = 0  # 塗ったら×は自動で消す

            if hasattr(self, 'solution'):
                if self.grid[row][col] != self.solution[row][col]:
                    if (col, row) not in self.mistakes:
                        self.mistakes.append((col, row))
                else:
                    if (col, row) in self.mistakes:
                        self.mistakes.remove((col, row))

    def toggle_mark(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            if self.grid[row][col] == 1:
                return  # 黒く塗られてたら×をつけさせない
            self.marks[row][col] = 1 - self.marks[row][col]

    def evaluate_mistakes(self):
        self.miss_count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                mark = self.marks[row][col]
                sol = self.solution[row][col]

                if cell == 1 and sol == 0:
                    self.miss_count += 1  # 黒く塗っちゃダメなとこ塗った
                if mark == 1 and sol == 1:
                    self.miss_count += 1  # ×付けたとこが実は塗るべきだった

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

            for col, row in self.mistakes:
                x = col * self.cell_size + self.offset_x + 3
                y = row * self.cell_size + self.offset_y + 3
                pyxel.text(x, y, "x", 8)  # 赤色で×印を表示

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y
                color = 0 if self.grid[row][col] == 0 else 7
                pyxel.rect(x, y, self.cell_size, self.cell_size, color)
                pyxel.rectb(x, y, self.cell_size, self.cell_size, 13)
                if self.marks[row][col] == 1:
                    pyxel.text(x + 4, y + 4, "X", 8)
    
        
    def clear_all(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.marks = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.miss_count = 0

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

    def is_unique_solution(self, row_hints, col_hints):
        model = cp_model.CpModel()
        grid = [[model.NewBoolVar(f"cell_{r}_{c}") for c in range(self.cols)] for r in range(self.rows)]

        # 行ヒント制約
        for r, hint in enumerate(row_hints):
            self._add_line_hint_constraint(model, grid[r], hint)

        # 列ヒント制約
        for c, hint in enumerate(col_hints):
            col = [grid[r][c] for r in range(self.rows)]
            self._add_line_hint_constraint(model, col, hint)

        solver = cp_model.CpSolver()
        solution_count = 0

        class SolutionCounter(cp_model.CpSolverSolutionCallback):
            def __init__(self):
                cp_model.CpSolverSolutionCallback.__init__(self)
                self.count = 0

            def on_solution_callback(self):
                self.count += 1
                if self.count > 1:
                    self.StopSearch()

        counter = SolutionCounter()
        solver.SearchForAllSolutions(model, counter)

        return counter.count == 1


    def _add_line_hint_constraint(self, model, line_vars, hint):
        n = len(line_vars)
        if hint == [0]:
            for var in line_vars:
                model.Add(var == 0)
            return

        total_blocks = len(hint)
        starts = [model.NewIntVar(0, n - 1, f"start_{i}") for i in range(total_blocks)]

        for i in range(1, total_blocks):
            model.Add(starts[i] >= starts[i-1] + hint[i-1] + 1)

        for i in range(total_blocks):
            for j in range(hint[i]):
                model.Add(line_vars[starts[i] + j] == 1)

        # それ以外は0に
        for i in range(n):
            in_block_conditions = []
            for b in range(total_blocks):
                for j in range(hint[b]):
                    in_block_conditions.append(starts[b] + j == i)
            model.AddBoolOr([line_vars[i].Not()] + in_block_conditions)


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



