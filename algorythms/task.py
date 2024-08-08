import random
from collections import deque

def is_valid(x, y, board, attacked_cells):
    return 0 <= x < 8 and 0 <= y < 8 and board[x][y] == 0 and (x, y) not in attacked_cells

def min_knight_moves(start, end, pawns):
    directions = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]

    board = [[0 for _ in range(8)] for _ in range(8)]
    attacked_cells = set()
    for px, py in pawns:
        board[px][py] = 1  # Mark pawns on the board and mark cells attacked by black pawns
        if px + 1 < 8:
            if py + 1 < 8:
                attacked_cells.add((px + 1, py + 1))
            if py - 1 >= 0:
                attacked_cells.add((px + 1, py - 1))

    queue = deque([(start[0], start[1], 0, [(start[0], start[1])])])  # (x, y, steps, path)
    visited = set((start[0], start[1]))

    while queue:
        x, y, steps, path = queue.popleft()

        if (x, y) == end:
            for i in board:
                print(i)
            print("Path:", '->'.join([f"({px},{py})" for px, py in path]))
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, board, attacked_cells) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1, path + [(nx, ny)]))

    for i in board:
        print(i)
    return -1  # Return -1 if there is no valid path

# Пример использования:
start = (random.randint(0, 7), random.randint(0, 7))
end = (random.randint(0, 7), random.randint(0, 7))
print("Start:", start)
print("End:", end)
pawns = []
for _ in range(8):
    pawns.append((random.randint(0, 7), random.randint(0, 7)))  # List of pawns
print("Pawns:", pawns)
print(min_knight_moves(start, end, pawns))
