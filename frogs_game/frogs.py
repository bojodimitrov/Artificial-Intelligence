"""
Main
"""
import sys
import time
import operator

_GREEN = "<"
_BROWN = ">"
_EMPTY = "_"

class Game:
    """
    Controls the frogs positions, return all possible next moves, recreates game given a snapshot
    """
    def __init__(self, frog_count):
        self.frogs_count = frog_count

        self.frogs = []
        for i in range(0, int(self.frogs_count)):
            self.frogs.append(_BROWN)
        self.frogs.append(_EMPTY)
        for i in range(0, int(self.frogs_count)):
            self.frogs.append(_GREEN)

    def get_current_state(self):
        return list(self.frogs)

    def print(self):
        """
        Prints current game state
        """
        for frog in self.frogs:
            if frog == _EMPTY:
                print('_', end='')
            else:
                print(frog, end='')
        print('\n')

    def recreate(self, snapshot):
        """
        Recreates the game state using the given snapshot.
        snapshot: symbols '<', '>' or '_' represent green and brown frog or empty space
        """
        self.frogs.clear()
        for x in snapshot:
            self.frogs.append(x)

    def get_possible_moves(self):
        """
        Returns all possible moves
        """
        empty_space_position = self.frogs.index(_EMPTY)
        left, right = max(empty_space_position - 2, 0), min(empty_space_position + 2, len(self.frogs) - 1)
        possible_moves = []
        for frog in range(left, right+1):
            if self.frogs[frog] == _GREEN:
                self.__check_frog(possible_moves, empty_space_position, frog, operator.sub)
            if self.frogs[frog] == _BROWN:
                self.__check_frog(possible_moves, empty_space_position, frog, operator.add)
        return possible_moves

    def __check_frog(self, possible_moves, empty_space_position, frog, action):
        current_state = list(self.frogs)
        if action(frog, 1) == empty_space_position or action(frog, 2) == empty_space_position:
            current_state[empty_space_position] = current_state[frog]
            current_state[frog] = _EMPTY
            possible_moves.append(current_state)

    def is_finished(self, state):
        """
        Checks if game is in finished state
        """
        tmp_frogs = []
        for i in range(0, int(self.frogs_count)):
            tmp_frogs.append(_GREEN)
        tmp_frogs.append(_EMPTY)
        for i in range(0, int(self.frogs_count)):
            tmp_frogs.append(_BROWN)
        if state == tmp_frogs:
            return True
        return False

start = time.time()

if len(sys.argv) <= 1:
    _NUMBER_OF_FROGS = 2
else:
    _NUMBER_OF_FROGS = sys.argv[1]

_GAME = Game(int(_NUMBER_OF_FROGS))
Q = []
_RESULT = []
visited = set()
pathFound = False

def traverse_moves(move):
    global _RESULT
    global pathFound
    if pathFound:
        return
    if not move:
        return
    Q.append(move)
    if _GAME.is_finished(move):
        
        _RESULT = list(Q)
        pathFound = True
    _GAME.recreate(move)
    visited.add(''.join(move))
    possible_moves = _GAME.get_possible_moves()
    for a_move in possible_moves:
        if(not ''.join(a_move) in visited):
            traverse_moves(a_move)
    Q.pop()

traverse_moves(_GAME.get_current_state())

end = time.time()
for elem in _RESULT:
    for x in elem:
        print(x, end='')
    print()

#print(end - start)
