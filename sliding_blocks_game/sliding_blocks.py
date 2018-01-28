"""
Sliding blocks
"""
import operator
import numpy
import heapq as hq
import math


_EMPTY_BLOCK = 0

n = int(input())
_MAX = int(math.sqrt(n+1)-1)

board = []
starting_state = []
for i in range(_MAX+1):
    board.append(input())
for item in board:
    starting_state.append(list(map(lambda x: int(x) , item.split(' '))))

def matrixfy_string(string):
    """
    Returns 2D array from given string of digits
    """
    list_str = list(map(lambda x: int(x), string.split('.')))
    return [list_str[i:i + _MAX+1] for i in range(0, len(list_str), _MAX+1)]


str_finished_state = ''
for i in range(n):
    str_finished_state += str(i+1) + '.'
str_finished_state += '0'
_FINISHED_STATE = matrixfy_string(str_finished_state)

class PriorityQueue:
    """
    Implementation of priority queue using heap
    """
    def __init__(self):
        self.container = []
        self.data = set()
    
    def pop(self):
        chunk = hq.heappop(self.container)[1]
        self.data.remove(chunk)
        return chunk

    def put(self, item, priority):
        hq.heappush(self.container, (priority, item))
        self.data.add(item)

    def empty(self):
        return len(self.container) == 0

    def __contains__(self, chunk):
        return chunk in self.data


def generate_next_moves(state):
    """
    Generates all possible next moves
    """
    position = [(index, row.index(_EMPTY_BLOCK)) for index, row in enumerate(state) if _EMPTY_BLOCK in row][0]
    moves = []
    #move_up
    append_move_vertical(state, position, moves, operator.sub, operator.le, 0)
    #move_down
    append_move_vertical(state, position, moves, operator.add, operator.ge, _MAX)
    #move_left
    append_move_horizontal(state, position, moves, operator.sub, operator.le, 0)
    #move_up
    append_move_horizontal(state, position, moves, operator.add, operator.ge, _MAX)
    return moves

def append_move_vertical(state, position, moves, act, comp, edge):
    """
    Swaps empty space and a block if possible in a vertical manner
    """
    if comp(position[0], edge):
        return
    swapped = [row[:] for row in state]
    swapped[position[0]][position[1]] = swapped[act(position[0], 1)][position[1]]
    swapped[act(position[0], 1)][position[1]] = _EMPTY_BLOCK
    moves.append(swapped)

def append_move_horizontal(state, position, moves, act, comp, edge):
    """
    Swaps empty space and a block if possible in a horizontal manner
    """
    if comp(position[1], edge):
        return
    swapped = [row[:] for row in state]
    swapped[position[0]][position[1]] = swapped[position[0]][act(position[1], 1)]
    swapped[position[0]][act(position[1], 1)] = _EMPTY_BLOCK
    moves.append(swapped)

def heuristic_manhattan(state):
    """
    Returns weight of how far state is from finished state using manhattan distance
    """
    weight = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if(not _FINISHED_STATE[i][j] == 0):
                position = [(index, row.index(_FINISHED_STATE[i][j])) for index, row in enumerate(state) if _FINISHED_STATE[i][j] in row][0]
                weight += calc_distance(position, (i, j))
    return weight


def calc_distance(first, second):
    """
    Returns manhattan distance between two points
    """
    x_dist = abs(first[0] - second[0])
    y_dist = abs(first[1] - second[1])
    return x_dist + y_dist

def stringify_list(l):
    return '.'.join([str(item) for sublist in l for item in sublist])


def reconstruct_path(came_from, current):
    """
    Reconstructs path
    """
    total_path = []
    while current is not None:
        total_path.append(current)
        current = came_from[current]
    return total_path[::-1]


def a_star_search(start):
    """
    Implementation of A* algorith
    """
    str_start = stringify_list(start)
    frontier = PriorityQueue()
    frontier.put(str_start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[str_start] = None
    cost_so_far[str_start] = 0
    
    while not frontier.empty():
        
        current = frontier.pop()
        mat_current = matrixfy_string(current)
        if current == stringify_list(_FINISHED_STATE):
            return reconstruct_path(came_from, stringify_list(_FINISHED_STATE))
        
        for next in generate_next_moves(mat_current):
            str_next = stringify_list(next)

            new_cost = cost_so_far[current] + 1

            if str_next not in cost_so_far or new_cost < cost_so_far[str_next]:
                cost_so_far[str_next] = new_cost
                priority = new_cost + heuristic_manhattan(next)

                if str_next not in frontier:
                    frontier.put(str_next, priority)
                
                came_from[str_next] = current
    return []
    
def generate_winning_moves(path):
    previous = path[0]
    path.remove(previous)
    directions = []
    for current in path:
        directions.append(get_direction(matrixfy_string(previous), matrixfy_string(current)))
        previous = current
    return directions


def get_direction(first, second):
    first_empty_block_pos = [(index, row.index(_EMPTY_BLOCK)) for index, row in enumerate(first) if _EMPTY_BLOCK in row][0]
    second_empty_block_pos = [(index, row.index(_EMPTY_BLOCK)) for index, row in enumerate(second) if _EMPTY_BLOCK in row][0]
    if(first_empty_block_pos[0] - second_empty_block_pos[0] == 0 and first_empty_block_pos[1] - second_empty_block_pos[1] == -1):
        return "left"
    if(first_empty_block_pos[0] - second_empty_block_pos[0] == 0 and first_empty_block_pos[1] - second_empty_block_pos[1] == 1):
        return "right"
    if(first_empty_block_pos[0] - second_empty_block_pos[0] == -1 and first_empty_block_pos[1] - second_empty_block_pos[1] == 0):
        return "up"
    if(first_empty_block_pos[0] - second_empty_block_pos[0] == 1 and first_empty_block_pos[1] - second_empty_block_pos[1] == 0):
        return "down"

winning_moves = generate_winning_moves(a_star_search(starting_state))
for move in winning_moves:
    print(move)