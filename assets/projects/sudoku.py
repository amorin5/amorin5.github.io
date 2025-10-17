"""
Run:
  python sudoku_color_notes.py [easy|medium|hard]
"""

import sys
import os
import random
from typing import List, Tuple, Optional, Set, Dict
from collections import defaultdict
try:
    from wcwidth import wcswidth
except Exception:
    def wcswidth(s):
        try:
            return len(re.sub(r'\x1b\[[0-9;]*m', '', s))
        except Exception:
            return len(s)
import re

# --- Color setup (works on Windows via colorama) ---
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
except Exception:  # fallback if colorama isn't installed
    class _Dummy:
        def __getattr__(self, k): return ""
    Fore = Style = _Dummy()

Board = List[List[int]]  # 9x9 values, 0 means empty


# ---------------------------- Solver / Generator ----------------------------

def find_empty(board: Board) -> Optional[Tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def valid(board: Board, r: int, c: int, val: int) -> bool:
    # row
    if any(board[r][x] == val for x in range(9)):
        return False
    # col
    if any(board[x][c] == val for x in range(9)):
        return False
    # box
    br, bc = (r // 3) * 3, (c // 3) * 3
    for rr in range(br, br + 3):
        for cc in range(bc, bc + 3):
            if board[rr][cc] == val:
                return False
    return True


def solve_backtrack(board: Board) -> bool:
    spot = find_empty(board)
    if not spot:
        return True
    r, c = spot
    for val in range(1, 10):
        if valid(board, r, c, val):
            board[r][c] = val
            if solve_backtrack(board):
                return True
            board[r][c] = 0
    return False


def solve_count(board: Board, limit: int = 2) -> int:
    """Return the number of solutions up to 'limit' (early-exit)."""
    cnt = 0

    def backtrack():
        nonlocal cnt
        if cnt >= limit:
            return
        spot = find_empty(board)
        if not spot:
            cnt += 1
            return
        r, c = spot
        for val in range(1, 10):
            if valid(board, r, c, val):
                board[r][c] = val
                backtrack()
                board[r][c] = 0

    backtrack()
    return cnt


def make_full_solution() -> Board:
    board = [[0] * 9 for _ in range(9)]

    def shuffled_1to9() -> List[int]:
        nums = list(range(1, 10))
        random.shuffle(nums)
        return nums

    def backtrack() -> bool:
        spot = find_empty(board)
        if not spot:
            return True
        r, c = spot
        for val in shuffled_1to9():
            if valid(board, r, c, val):
                board[r][c] = val
                if backtrack():
                    return True
                board[r][c] = 0
        return False

    backtrack()
    return board


def clone_board(b: Board) -> Board:
    return [row[:] for row in b]


def remove_clues_unique(board: Board, difficulty: str = "medium") -> Board:
    difficulty = difficulty.lower()
    attempts = {"easy": 40, "medium": 55, "hard": 64}.get(difficulty, 55)

    puzzle = clone_board(board)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for r, c in cells:
        if attempts <= 0:
            break
        if puzzle[r][c] == 0:
            continue
        backup = puzzle[r][c]
        puzzle[r][c] = 0

        test = clone_board(puzzle)
        solutions = solve_count(test, limit=2)
        if solutions != 1:
            puzzle[r][c] = backup  # revert
        attempts -= 1

    return puzzle


# ------------------------------ Notes / Helpers ------------------------------

def valid_local(board: Board, r: int, c: int, val: int) -> bool:
    # row
    for cc in range(9):
        if cc != c and board[r][cc] == val:
            return False
    # col
    for rr in range(9):
        if rr != r and board[rr][c] == val:
            return False
    # box
    br, bc = (r // 3) * 3, (c // 3) * 3
    for rr in range(br, br + 3):
        for cc in range(bc, bc + 3):
            if (rr != r or cc != c) and board[rr][cc] == val:
                return False
    return True


def compute_candidates(board: Board, r: int, c: int) -> Set[int]:
    if board[r][c] != 0:
        return set()
    cand = set(range(1, 10))
    # eliminate row
    cand -= {board[r][x] for x in range(9) if board[r][x] != 0}
    # eliminate col
    cand -= {board[x][c] for x in range(9) if board[x][c] != 0}
    # eliminate box
    br, bc = (r // 3) * 3, (c // 3) * 3
    for rr in range(br, br + 3):
        for cc in range(bc, bc + 3):
            v = board[rr][cc]
            if v != 0 and v in cand:
                cand.remove(v)
    return cand


# ------------------------------ Pretty Printing ------------------------------

CELL_W = int(os.getenv("SUDOKU_CELL_W", "4"))  # width per cell to allow short notes like [123] or [1+]

def style_given(s: str) -> str:
    return Style.BRIGHT + Fore.CYAN + s + Style.RESET_ALL

def style_user(s: str) -> str:
    return Style.BRIGHT + s + Style.RESET_ALL

def style_wrong(s: str) -> str:
    return Style.BRIGHT + Fore.RED + s + Style.RESET_ALL

def style_hint(s: str) -> str:
    return Style.BRIGHT + Fore.YELLOW + s + Style.RESET_ALL

ansi_re = re.compile(r'\x1b\[[0-9;]*m')

def visible_len(s: str) -> int:
    return wcswidth(ansi_re.sub('', s))

def pad_visible(s: str, width: int, align: str = 'center') -> str:
    vis = visible_len(s)
    if vis >= width:
        return s
    pad = width - vis
    if align == 'left':
        return s + ' ' * pad
    if align == 'right':
        return ' ' * pad + s
    left = pad // 2
    right = pad - left
    return ' ' * left + s + ' ' * right
    return Style.BRIGHT + Fore.YELLOW + s + Style.RESET_ALL


def cell_text(val: int, given: bool, wrong: bool, notes: Set[int] | None) -> str:
    if val == 0:
        if notes:
            s = "".join(str(d) for d in sorted(notes))
            if len(s) <= 4:
                disp = f"[{s}]"
            else:
                disp = f"[{s[:3]}+]"
        else:
            disp = " . "
        return f"{disp:^{CELL_W}}"
    else:
        s = f"{val}"
        text = f"{s:^{CELL_W}}"
        if wrong:
            return style_wrong(text)
        if given:
            return style_given(text)
        return style_user(text)


def print_board(board: Board, given_mask: List[List[bool]], wrong_set: Set[Tuple[int, int]] | None = None, notes_map: Dict[Tuple[int,int], Set[int]] = None) -> None:
    wrong_set = wrong_set or set()
    notes_map = notes_map or {}

    # header
    col_hdr = " ".join([f"{i:^{CELL_W}}" for i in range(1, 10)])
    print("\n     C " + col_hdr)
    print("   ┌" + ("─" * (CELL_W*3)) + "┬" + ("─" * (CELL_W*3)) + "┬" + ("─" * (CELL_W*3)) + "┐")
    for r in range(9):
        parts = []
        for c in range(9):
            given = given_mask[r][c]
            wrong = (r, c) in wrong_set
            notes = notes_map.get((r, c))
            parts.append(cell_text(board[r][c], given, wrong, notes))
        row_str = "│" + "".join(parts[0:3]) + "│" + "".join(parts[3:6]) + "│" + "".join(parts[6:9]) + "│"
        print(f" R{r+1:>2} {row_str}")
        if r in (2, 5):
            print("   ├" + ("─" * (CELL_W*3)) + "┼" + ("─" * (CELL_W*3)) + "┼" + ("─" * (CELL_W*3)) + "┤")
    print("   └" + ("─" * (CELL_W*3)) + "┴" + ("─" * (CELL_W*3)) + "┴" + ("─" * (CELL_W*3)) + "┘\n")
    print("Legend: '.' empty, cyan = given clue, red = wrong, yellow = last hint; notes shown as [digits] (truncated)\n")


# --------------------------------- Game Loop ---------------------------------

class Game:
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.solution: Board = make_full_solution()
        self.puzzle: Board = remove_clues_unique(self.solution, difficulty=self.difficulty)
        self.given = [[self.puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
        self.board: Board = clone_board(self.puzzle)
        self.notes: Dict[Tuple[int,int], Set[int]] = defaultdict(set)
        self._last_hint: Optional[Tuple[int,int]] = None

    def restart(self):
        self.__init__(self.difficulty)

    def is_complete(self) -> bool:
        return all(all(v != 0 for v in row) for row in self.board)

    def places_conflict(self) -> Set[Tuple[int, int]]:
        wrong = set()
        for r in range(9):
            for c in range(9):
                v = self.board[r][c]
                if v != 0 and v != self.solution[r][c]:
                    wrong.add((r, c))
        return wrong

    def set_value(self, r: int, c: int, v: int) -> str:
        if not (1 <= r <= 9 and 1 <= c <= 9 and 0 <= v <= 9):
            return "Row/Col must be 1..9 and value 0..9 (0 clears)."
        r -= 1; c -= 1
        if self.given[r][c]:
            return "That cell is a given clue; you can't change it."
        if v == 0:
            self.board[r][c] = 0
            self.notes.pop((r,c), None)
            return "Cleared."
        if not valid_local(self.board, r, c, v):
            return "That move conflicts with current row/column/box."
        self.board[r][c] = v
        self.notes.pop((r,c), None)
        return "Set."

    def hint(self, r: int, c: int) -> str:
        if not (1 <= r <= 9 and 1 <= c <= 9):
            return "Row/Col must be 1..9."
        r -= 1; c -= 1
        if self.given[r][c]:
            return "That's already a given."
        self.board[r][c] = self.solution[r][c]
        self.notes.pop((r,c), None)
        self._last_hint = (r, c)
        return f"Hint: set ({r+1},{c+1}) to {self.solution[r][c]}."

    def solve_all(self) -> None:
        self.board = clone_board(self.solution)
        self.notes.clear()

    # --- Notes management ---
    def notes_add(self, r: int, c: int, digits: List[int]) -> str:
        if not (1 <= r <= 9 and 1 <= c <= 9):
            return "Row/Col must be 1..9."
        r -= 1; c -= 1
        if self.board[r][c] != 0:
            return "Cell already has a value. Clear it before adding notes."
        for d in digits:
            if 1 <= d <= 9:
                self.notes[(r,c)].add(d)
        return "Notes updated."

    def notes_remove(self, r: int, c: int, digits: List[int]) -> str:
        if not (1 <= r <= 9 and 1 <= c <= 9):
            return "Row/Col must be 1..9."
        r -= 1; c -= 1
        s = self.notes.get((r,c), set())
        for d in digits:
            s.discard(d)
        if not s and (r,c) in self.notes:
            self.notes.pop((r,c), None)
        return "Notes updated."

    def notes_clear(self, r: int, c: int) -> str:
        if not (1 <= r <= 9 and 1 <= c <= 9):
            return "Row/Col must be 1..9."
        r -= 1; c -= 1
        self.notes.pop((r,c), None)
        return "Notes cleared."

    def notes_auto(self) -> int:
        count = 0
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    cand = compute_candidates(self.board, r, c)
                    if cand:
                        self.notes[(r,c)] = cand
                        count += 1
                    else:
                        self.notes.pop((r,c), None)
        return count


def print_help():
    print("""Commands:
  set r c v        -> place value v at row r, col c (1..9). Example: set 3 7 5
  r c v            -> shorthand for set (e.g., 3 7 5)
  clear r c        -> clear a cell (same as set r c 0)
  hint r c         -> fill the correct value for a single cell
  check            -> highlight any wrong entries vs. the solution
  solve            -> fill the entire board with the solution
  restart          -> new puzzle (same difficulty)
  pencil r c add d1 [d2 ...]     -> add notes (digits) to a cell
  pencil r c remove d1 [d2 ...]  -> remove specific notes from a cell
  pencil r c clear               -> clear all notes in a cell
  auto                           -> auto-fill candidate notes for all empty cells
  help             -> this help
  quit             -> exit
""")


def main():
    difficulty = "medium"
    if len(sys.argv) >= 2:
        difficulty = sys.argv[1].lower()
        if difficulty not in ("easy", "medium", "hard"):
            print("Difficulty must be one of: easy | medium | hard")
            return

    random.seed()
    game = Game(difficulty=difficulty)
    print(f"\nWelcome to Console Sudoku — difficulty: {difficulty} (now with colors + pencil marks)\n")
    print_help()
    print_board(game.board, game.given, notes_map=game.notes)

    last_hint_cell = None

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()

        if cmd in ("quit", "exit", "q"):
            print("Goodbye!")
            return

        elif cmd == "help":
            print_help()

        elif cmd == "restart":
            game.restart()
            print(f"New puzzle — difficulty: {game.difficulty}")
            print_board(game.board, game.given, notes_map=game.notes)

        elif cmd == "check":
            wrong = game.places_conflict()
            if not wrong and game.is_complete():
                print("Looks perfect — puzzle solved! 🎉")
            elif not wrong:
                print("No mistakes so far. Keep going!")
            else:
                print(f"{len(wrong)} incorrect cell(s) are marked in red below:")
            print_board(game.board, game.given, wrong_set=wrong, notes_map=game.notes)

        elif cmd == "solve":
            game.solve_all()
            print("Solution revealed.")
            print_board(game.board, game.given, notes_map=game.notes)

        elif cmd == "hint" and len(parts) == 3:
            try:
                r, c = int(parts[1]), int(parts[2])
            except ValueError:
                print("Usage: hint r c")
                continue
            msg = game.hint(r, c)
            print(style_hint(msg))
            print_board(game.board, game.given, notes_map=game.notes)

        elif cmd == "clear" and len(parts) == 3:
            try:
                r, c = int(parts[1]), int(parts[2])
            except ValueError:
                print("Usage: clear r c")
                continue
            print(game.set_value(r, c, 0))
            print_board(game.board, game.given, notes_map=game.notes)

        elif cmd == "set" and len(parts) == 4:
            try:
                r, c, v = int(parts[1]), int(parts[2]), int(parts[3])
            except ValueError:
                print("Usage: set r c v")
                continue
            print(game.set_value(r, c, v))
            print_board(game.board, game.given, notes_map=game.notes)

        elif cmd == "pencil" and len(parts) >= 4:
            # pencil r c add|remove|clear [digits...]
            try:
                r, c = int(parts[1]), int(parts[2])
            except ValueError:
                print("Usage: pencil r c add|remove|clear [digits...]")
                continue
            action = parts[3].lower()
            if action == "add" and len(parts) >= 5:
                try:
                    digits = [int(x) for x in parts[4:] if x.isdigit() and 1 <= int(x) <= 9]
                except ValueError:
                    print("Digits must be 1..9")
                    continue
                print(game.notes_add(r, c, digits))
            elif action == "remove" and len(parts) >= 5:
                try:
                    digits = [int(x) for x in parts[4:] if x.isdigit() and 1 <= int(x) <= 9]
                except ValueError:
                    print("Digits must be 1..9")
                    continue
                print(game.notes_remove(r, c, digits))
            elif action == "clear":
                print(game.notes_clear(r, c))
            else:
                print("Usage: pencil r c add|remove|clear [digits...]")
            print_board(game.board, game.given, notes_map=game.notes)

        elif cmd == "auto":
            n = game.notes_auto()
            print(f"Auto-filled notes for {n} cell(s).")
            print_board(game.board, game.given, notes_map=game.notes)

        else:
            # Shorthand set: "r c v"
            if len(parts) == 3 and all(p.isdigit() for p in parts):
                r, c, v = map(int, parts)
                print(game.set_value(r, c, v))
                print_board(game.board, game.given, notes_map=game.notes)
            else:
                print("Unknown command. Type 'help' for options.")

        if game.is_complete() and not game.places_conflict():
            print("🎉 Congratulations! You solved the puzzle! Type 'restart' for a new one or 'quit'.")


if __name__ == "__main__":
    main()
