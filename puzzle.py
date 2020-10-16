import numpy as np
import math
import copy
import collections

def LoadFromFile(file):
	n = 0
	initial = []
	with open(file, 'r') as f:
		n = int(next(f))
		trusted = [str(i) for i in range(1, n*n )]
		trusted.append("*")
		# print(trusted)
		for i in f:
			# print(i)
			to_append = i[:-1].split('\t') #split line on tabs until the last character with new line char dropped
			# print(to_append)
			if '' in to_append or len(to_append) != n:
				print("Error, invalid file")
				return None
			temp = []
			for x in to_append:
				if x in trusted:
					temp.append(x)
					trusted.remove(x)
				else:
					print("Error, invalid file: unexpected character, not int from 1-n^2 or * or duplicate")
					return None
			initial.append(temp)
					
	# print(initial)

	if len(initial) != n:
		print("Error, invalid file: invalid length of inputed game state")
		return None
	elif "*" not in np.array(initial).flatten():
		print("Error, invalid file: no blank character")
		return None

	return n, dict((j,(x, y)) for x, i in enumerate(initial) for y, j in enumerate(i))

def DebugPrint(n, state):
	count = 0
	for i in state:
		print(i[0], end = '	')
		count += 1
		if count == n:
			print()
			count = 0
	print()

def swap_key_value(dict_in):
	return dict([(value, key) for key, value in dict_in.items()])

def ComputeNeighbors(state):
	to_ret = []
	n = math.sqrt(len(state))
	blank = state['*']
	# print("Blank at " + str(blank))
	options = [(blank[0]-1, blank[1]), (blank[0]+1, blank[1]), (blank[0], blank[1]-1), (blank[0], blank[1]+1)] #list of options in up, down, left, right order
	for pair in options:
		if  (pair[0] > n or pair[0] < 0) or (pair[1] > n or pair[1] < 0):
			options.remove(pair)
	# print("Alternate positions of blank: " + str(options))
	swapped_state = swap_key_value(state)
	
	for o in options:
		temp_dict = copy.deepcopy(swapped_state)
		temp = temp_dict[o]
		temp_dict[o] = "*"
		temp_dict[blank] = temp
		to_ret.append((temp, swap_key_value(temp_dict)))
	return to_ret

def IsGoal(state):
	values = list(state.values())
	keys = [str(x) for x in range(1, len(state))]
	keys.append("*")
	goal = dict(zip(keys, values))
	# print(goal)
	return state == goal

size, state = LoadFromFile("input.txt")
# print(state)
DebugPrint(size, state)
neighbors = ComputeNeighbors(state)
for i, j in neighbors:
	print("tile moved: " + str(i))
	DebugPrint(size, j)

IsGoal(state)