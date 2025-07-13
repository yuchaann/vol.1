import pyxel

class Table:
    def __init__(self, cols, rows, cell_size):
        # 既存の初期化コード
        self.cols = cols
        self.rows = rows
        self.offset_x = 130
        self.offset_y = 130
        self.cell_size = cell_size
        self.show_answer = False
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
            
            for r in range(self.rows):
                for c in range(self.cols):
                    x = self.offset_x + c * self.cell_size
                    y = self.offset_y + r * self.cell_size

                    # 表示切替：答えを表示する or 通常モード
                    if self.show_answer:
                        color = 9 if self.solution[r][c] else 0
                    else:
                        color = 7 if self.grid[r][c] else 0

                    pyxel.rect(x, y, self.cell_size, self.cell_size, color)
                    pyxel.rectb(x, y, self.cell_size, self.cell_size, 13)

                    if self.marks[r][c] and not self.show_answer:
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

    def set_show_answer(self, flag):
        self.show_answer = flag
        self.show_answer = flag

    def has_unique_solution(self):
        """今のヒントに一意解があるか判定"""
        solutions = []
        def dfs(grid, row=0):
            if row == self.rows:
                # 解が完成したらヒント一致チェック
                if self.hints_match(grid):
                    solutions.append([r[:] for r in grid])
                return

            # この行でありえる塗り方の候補を生成
            for candidate in self.generate_row_candidates(self.row_hints[row], self.cols):
                grid[row] = candidate
                dfs(grid, row + 1)
                if len(solutions) > 1:
                    return  # 2個以上見つかったら中断

        grid = [[0] * self.cols for _ in range(self.rows)]
        dfs(grid)
        return len(solutions) == 1
    
    def generate_row_candidates(self, hint, length):
        """ヒントから可能な1行の候補を列挙"""
        def dfs(index, hint_index, current):
            if hint_index == len(hint):
                current += [0] * (length - len(current))
                results.append(current)
                return
            for i in range(index, length - sum(hint[hint_index:]) - (len(hint) - hint_index - 1) + 1):
                new_current = current + [0] * (i - len(current)) + [1] * hint[hint_index]
                if len(new_current) < length:
                    new_current += [0]
                dfs(i + 1, hint_index + 1, new_current[:])
        results = []
        dfs(0, 0, [])
        return results

    def hints_match(self, grid):
        """今のgridが行・列ヒントと一致してるか"""
        # 行チェック
        for r in range(self.rows):
            if self.extract_hint(grid[r]) != self.row_hints[r]:
                return False
        # 列チェック
        for c in range(self.cols):
            col = [grid[r][c] for r in range(self.rows)]
            if self.extract_hint(col) != self.col_hints[c]:
                return False
        return True

    def extract_hint(self, line):
        """ヒントを生成（1列や1行から）"""
        hints = []
        count = 0
        for cell in line:
            if cell == 1:
                count += 1
            elif count > 0:
                hints.append(count)
                count = 0
        if count > 0:
            hints.append(count)
        return hints or [0]




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