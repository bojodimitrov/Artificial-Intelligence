"""
Solves N-Queen problem using min-conflicts algorithm
"""
import random
import numpy
import time
import sys

if len(sys.argv) <= 1:
    _NUM = 8
else:
    _NUM = int(sys.argv[1])

_TRESHOLD = 10000
global start_calculating
global start_assignment

def create_board():
	board = []
	for i in range(_NUM):
		board.append([])
		for j in range(_NUM):
			board[i].append(0)
	return board

def create_greedy_initial_state():
	queens = []
	positions = list(range(_NUM))
	for i in range(_NUM):
		column = random.randint(0, len(positions)-1)
		queens.append(positions[column])
	return queens

def create_min_conflicts_initial_state(board):
	queens = []
	for i in range(_NUM):
		new_position = choose_new_position(board, i)
		queens.append(new_position)
		update_conflicts(board, new_position, i, 1)
	return queens


def calculate_conflicts(board, queens):
	num = 0
	for i in range(_NUM):
		update_conflicts(board, queens[i], i, 1)

			

def update_conflicts(board, x, y, change):
	for i in range(_NUM):
		if(i != y):
			board[x][i] += change
	#Update upper diagonal on left side
	for i,j in zip(range(x-1,-1,-1), range(y-1,-1,-1)):
		board[i][j] += change
	#Update upper diagonal on right side
	for i,j in zip(range(x-1,-1,-1), range(y+1,_NUM,1)):
		board[i][j] += change
    #Update lower diagonal on left side    
	for i,j in zip(range(x+1,_NUM,1), range(y-1,-1,-1)):
		board[i][j] += change
	#Update lower diagonal on right side    
	for i,j in zip(range(x+1,_NUM,1), range(y+1,_NUM,1)):
		board[i][j] += change

def no_conficts(board, queens):
	for i in range(_NUM):
		if board[queens[i]][i] > 0:
			return False
	return True

def reset_board(board):
	for i in range(_NUM):
		for j in range(_NUM):
			board[i][j] = 0

def choose_new_position(board, column):
	min = _NUM
	min_positions = []
	for i in range(_NUM):
		if(min > board[i][column]):
			min = board[i][column]
	for i in range(_NUM):
		if(min == board[i][column]):
			min_positions.append(i)
	return min_positions[random.randint(0, len(min_positions)-1)]
	

def most_conflicted_queen(board, queens):
	max = 0
	max_position = []
	for i in range(_NUM):
		if(max < board[queens[i]][i]):
			max = board[queens[i]][i]
	for i in range(_NUM):
		if(max == board[queens[i]][i]):
			max_position.append(i)
	return max_position[random.randint(0, len(max_position)-1)]
	
def n_queens():
	board = create_board()

	#assignment of queens using greedy methods
	global start_assignment
	start_assignment = time.time()

	queens = create_min_conflicts_initial_state(board)

	end_assignment = time.time()
	print("Assignment of queens done for ->", end=' ')
	print(end_assignment - start_assignment)

	global start_calculating
	start_calculating = time.time()

	#calculate_conflicts(board, queens)
	for i in range(_TRESHOLD):

		column =  most_conflicted_queen(board, queens)
		
		new_position = choose_new_position(board, column)
		update_conflicts(board, queens[column], column, -1)
		queens[column] = new_position
		update_conflicts(board, queens[column], column, 1)

		if(no_conficts(board, queens)):
			print("Swaps made -> " + str(i))
			return queens
	return False

def print_queens(queens):
	for i in range(_NUM):
		for j in range(_NUM):
			if queens[j] == i:
				print("*", end=' ')
			else:
				print("_", end=' ')
		print()

print("Start solving N-Queens problem for " + str(_NUM) + " queens.")

queens_composition = n_queens()
end = time.time()

if(queens_composition):
	#print_queens(queens_composition)
	print("Calculation done for ->", end=' ')
	print(end - start_calculating)
else:
	print("Solution not found.")
	
print("Total time taken ->", end=' ')
print(end - start_assignment)
