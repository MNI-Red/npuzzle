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
				# if x == '*':
				# 	temp.append(0)
				# 	trusted.remove(x)
				# 	continue
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
	elif '*' not in np.array(initial).flatten():
		print("Error, invalid file: no blank character")
		return None


	return n, dict((j,(x, y)) for x, i in enumerate(initial) for y, j in enumerate(i))

def DebugPrint(n, state):
	count = 0
	for i in state:
		print(i, end = '	')
		count += 1
		if count == n:
			print()
			count = 0
	print()

def swap_key_value(dict_in):
	return dict([(value, key) for key, value in dict_in.items()])

def ComputeNeighbors(state):
	to_ret = []
	valid = list(state.values())
	# print(valid)
	n = int(math.sqrt(len(state)))
	# print(n)
	blank = state['*']
	# print("Blank at " + str(blank))
	options = [(blank[0]-1, blank[1]), (blank[0]+1, blank[1]), (blank[0], blank[1]-1), (blank[0], blank[1]+1)] #list of options in up, down, left, right order
	# print(options)
	options = [pair for pair in options if pair in valid]

	# print("Alternate positions of blank: " + str(options))
	swapped_state = swap_key_value(state)
	# print("swapped state: " +str(swapped_state))
	for o in options:
		temp_dict = copy.deepcopy(swapped_state)
		temp = temp_dict[o]
		temp_dict[o] = '*'
		temp_dict[blank] = temp
		to_ret.append((temp, swap_key_value(temp_dict)))
	# print("to_ret: " + str(to_ret))
	return to_ret

def find_goal(state):
	values = list(state.values())
	keys = [str(x) for x in range(1, len(state))]
	keys.append('*')
	return dict(zip(keys, values))

def IsGoal(state):
	return state == find_goal(state)

def BFS(state):
	frontier = [state]
	discovered = set(tuple(state.items()))
	parents = {0: None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			parents[-1] = current_state
			return parents
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				frontier.append(neighbor)
				discovered.add(check)
				parents[moved] = current_state

def BFS_WIP(state):
	frontier = [state]
	discovered = set(tuple(state.items()))
	parents = [(["*"], -1)]
	parent_key = parents[-1][0]
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			parents.append(current_state)
			return parents
		# print(current_state)
		# print(ComputeNeighbors(current_state))
		# swapped_parents = swap_key_value(parents)
		# print(swapped_parents)
		# print("Parents: " +str(parents))
		# print("Parents[-1][0]: " +str(parents[-1][0]))
		
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				# parent_key.append(moved)
				frontier.append(neighbor)
				discovered.add(check)
				parents.append((moved, current_state))
				

def DFS(state):
	frontier = [state]
	discovered = set(tuple(state.items()))
	parents = {0: None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			parents[-1] = current_state
			return parents
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				frontier.insert(0, neighbor)
				discovered.add(check)
				parents[moved] = current_state

def BFS_from_to(start, target):
	frontier = [start]
	discovered = set(tuple(state.items()))
	parents = {0: None}
	while frontier:
		current_state = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if current_state == target:
			parents[-1] = current_state
			return parents
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				frontier.append(neighbor)
				discovered.add(check)
				parents[moved] = current_state

def BidirectionalSearch(state):
	goal = find_goal(state)

	frontier_forward = [state]
	frontier_backward = [goal]

	discovered_forward = set(tuple(state.items()))
	discovered_backward = set(tuple(goal.items()))

	parents_forward = {0: None}
	parents_backward = collections.OrderedDict({-1: None})

	while frontier_forward and frontier_backward:
		
		current_state_forward = frontier_forward.pop(0)
		current_state_backward = frontier_backward.pop(0)

		discovered_forward.add(tuple(current_state_forward.items()))
		discovered_backward.add(tuple(current_state_backward.items()))

		if len(discovered_forward.intersection(discovered_backward)) >= 1:
			# print(parents_forward, "\n", parents_backward)
			parents_backward = {k: parents_backward[k] for k in reversed(list(parents_backward.keys()))}
			return {**parents_forward, **parents_backward}

		(moved_f, neighbor_f), (moved_b, neighbor_b) = (ComputeNeighbors(current_state_forward), ComputeNeighbors(current_state_backward))
		# # moved_f, neighbor_f = forward[0], for
		# # print(both_neighbors)
		# print(moved_f, neighbor_f, moved_b, neighbor_b)

		for moved_f, neighbor_f in ComputeNeighbors(current_state_forward):
			check_f = tuple(neighbor_f.items())
			if  check_f not in discovered_forward:
				frontier_forward.append(neighbor_f)
				discovered_forward.add(check_f)
				parents_forward[moved_f] = current_state_forward

		for moved_b, neighbor_b in ComputeNeighbors(current_state_backward):
			check_b = tuple(neighbor_b.items())
			if check_b not in discovered_backward:
				frontier_backward.append(neighbor_f)
				discovered_backward.add(check_b)
				parents_backward[moved_b] = current_state_backward

size, state = LoadFromFile("input.txt")
print(state)
DebugPrint(size, state)
neighbors = ComputeNeighbors(state)
# print(neighbors)
# for i, j in neighbors:
# 	print("tile moved: " + str(i))
# 	DebugPrint(size, j)
IsGoal(state)

# print(state)

path = BFS(state)
print(path)
del path[0]
print("BFS")
for key in path:
	# print(key[1])
	DebugPrint(size, path[key])

# path = DFS(state)
# del path[0]
# print("DFS")
# for key in path:
# 	DebugPrint(size, path[key])

# path = BidirectionalSearch(state)
# del path[0]
# del path[-1]
# # print(path)
# print("BidirectionalSearch")
# for key in path:
# 	DebugPrint(size, path[key])