import heapq
from collections import deque

class PuzNode:
    def __init__(self, board, mom=None, move=None, steps=0, deep=0):
        self.board = board
        self.mom = mom
        self.move = move
        self.steps = steps
        self.deep = deep
    
    def __lt__(self, other):
        return self.steps < other.steps

class TileGame:
    def __init__(self, start, target=((1,2,3),(4,5,6),(7,8,0))):
        self.start = start
        self.target = target
        self.n = 3
    
    def find_hole(self, board):
        for r in range(self.n):
            for c in range(self.n):
                if board[r][c] == 0:
                    return r, c
        return None
    
    def get_kids(self, node):
        board = node.board
        r, c = self.find_hole(board)
        kids = []
        
        for move, (dr, dc) in [('↑', (-1,0)), ('↓', (1,0)), 
                              ('←', (0,-1)), ('→', (0,1))]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                new_board = [list(row) for row in board]
                new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
                new_board_tup = tuple(tuple(row) for row in new_board)
                kids.append(PuzNode(new_board_tup, node, move, node.steps + 1, node.deep + 1))
        return kids
    
    def taxi_dist(self, board):
        dist = 0
        target_spots = {}
        for r in range(self.n):
            for c in range(self.n):
                target_spots[self.target[r][c]] = (r, c)
        
        for r in range(self.n):
            for c in range(self.n):
                val = board[r][c]
                if val != 0:
                    tr, tc = target_spots[val]
                    dist += abs(r - tr) + abs(c - tc)
        return dist
    
    def is_done(self, board):
        return board == self.target

def wide_search(game):
    first_node = PuzNode(game.start)
    if game.is_done(first_node.board):
        return first_node
        
    queue = deque([first_node])
    seen = set([game.start])
    count = 0
    
    while queue:
        node = queue.popleft()
        count += 1
        
        for kid in game.get_kids(node):
            if game.is_done(kid.board):
                print(f"Wide Search: Looked at {count} boards")
                return kid
                
            if kid.board not in seen:
                seen.add(kid.board)
                queue.append(kid)
    
    return None

def deep_search(game, max_deep=25):
    first_node = PuzNode(game.start)
    if game.is_done(first_node.board):
        return first_node
        
    stack = [first_node]
    seen = set([game.start])
    count = 0
    
    while stack:
        node = stack.pop()
        count += 1
        
        if game.is_done(node.board):
            print(f"Deep Search: Looked at {count} boards")
            return node
        
        if node.deep < max_deep:
            for kid in game.get_kids(node):
                if kid.board not in seen:
                    seen.add(kid.board)
                    stack.append(kid)
    
    return None

def cheap_search(game):
    first_node = PuzNode(game.start)
    if game.is_done(first_node.board):
        return first_node
        
    heap = []
    heapq.heappush(heap, (first_node.steps, first_node))
    seen = set([game.start])
    count = 0
    
    while heap:
        _, node = heapq.heappop(heap)
        count += 1
        
        if game.is_done(node.board):
            print(f"Cheap Search: Looked at {count} boards")
            return node
        
        for kid in game.get_kids(node):
            if kid.board not in seen:
                seen.add(kid.board)
                heapq.heappush(heap, (kid.steps, kid))
    
    return None

def star_search(game):
    def star_cost(node):
        return node.steps + game.taxi_dist(node.board)
    
    first_node = PuzNode(game.start)
    if game.is_done(first_node.board):
        return first_node
        
    heap = []
    heapq.heappush(heap, (star_cost(first_node), first_node))
    seen = set([game.start])
    count = 0
    
    while heap:
        _, node = heapq.heappop(heap)
        count += 1
        
        if game.is_done(node.board):
            print(f"Star Search: Looked at {count} boards")
            return node
        
        for kid in game.get_kids(node):
            if kid.board not in seen:
                seen.add(kid.board)
                heapq.heappush(heap, (star_cost(kid), kid))
    
    return None

def get_journey(node):
    path = []
    current = node
    while current:
        path.append(current)
        current = current.mom
    return path[::-1]

def show_solution(node, algo_name):
    if node is None:
        print(f"{algo_name}: No path found")
        return
    
    journey = get_journey(node)
    print(f"\n{algo_name} Path:")
    print(f"Moves needed: {len(journey) - 1}")
    print("Board journey:")
    
    for i, step in enumerate(journey):
        if i == 0:
            print("Start board:")
        elif i == len(journey) - 1:
            print("Target board:")
        else:
            print(f"Move {i} ({step.move}):")
        
        for row in step.board:
            print("  ", row)
        print()

if __name__ == "__main__":
    # Test puzzle from the exercise
    start_board = ((3, 2, 1),
                   (8, 0, 5), 
                   (6, 7, 4))
    
    target_board = ((1, 2, 3),
                    (4, 5, 6),
                    (7, 8, 0))
    
    game = TileGame(start_board, target_board)
    
    print("🧩 Tile Slider Game")
    print("Starting board:")
    for row in start_board:
        print("  ", row)
    print("\nGoal board:")
    for row in target_board:
        print("  ", row)
    
    print("\n" + "🔍" * 25)
    
    # Test all search methods
    wide_node = wide_search(game)
    show_solution(wide_node, "Wide Search")
    
    deep_node = deep_search(game)
    show_solution(deep_node, "Deep Search")
    
    cheap_node = cheap_search(game)
    show_solution(cheap_node, "Cheap Search")
    
    star_node = star_search(game)
    show_solution(star_node, "Star Search")