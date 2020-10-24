import numpy as np
import math
import copy
import heapq as hq

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

def reconstruct(current_state, parent_index, parents, index_state_map):
	index = parent_index+1
	parents[index] = parent_index
	index_state_map[index] = ('*', current_state)
	path = [index]
	states = []
	tiles = []
	while parents[index]:
		path.append(parents[index])
		states.append(index_state_map[index])
		tiles.append(index_state_map[index][0])
		index = parents[index]
	path.append(parents[index])
	states.append(index_state_map[index])
	tiles.append(index_state_map[index][0])
	return list(reversed(tiles)), list(reversed(path)), list(reversed(states))

def BFS(state):
	index = 0
	frontier = [(index, state)]
	discovered = set(tuple(state.items()))
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]	
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index = parent_index+1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				frontier.append((index, neighbor))
				discovered.add(check)
	return None

def BFS_WIP(state):
	index = 0
	frontier = [(index, state)]
	discovered = set(tuple(state.items()))
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index = parent_index+1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				frontier.append((index, neighbor))
				discovered.add(check)
	return None

def DFS(state):
	index = 0
	frontier = [(index, state)]
	discovered = set(tuple(state.items()))
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index = parent_index+1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				frontier.insert(0, (index, neighbor))
				discovered.add(check)
	return None

def DFS_WIP(state):
	index = 0
	frontier = [(index, state)]
	discovered = set(tuple(state.items()))
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index = parent_index+1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				frontier.insert(0, (index, neighbor))
				discovered.add(check)	
	return None

def BidirectionalSearch(state):
	goal = find_goal(state)
	index_f = 0
	index_b = 0
	frontier_forward = [(index_f,state)]
	frontier_backward = [(index_b, goal)]

	discovered_forward = set(tuple(state.items()))
	discovered_backward = set(tuple(goal.items()))

	parents_forward = {index_f: None}
	parents_backward = {index_b: None}

	index_state_map_f = {index_f: (0, state)}
	index_state_map_b = {index_b: (0, goal)}

	while frontier_forward and frontier_backward:
		
		(parent_index_f, current_state_forward) = frontier_forward.pop(0)
		(parent_index_b, current_state_backward) = frontier_backward.pop(0)

		discovered_forward.add(tuple(current_state_forward.items()))
		discovered_backward.add(tuple(current_state_backward.items()))

		if len(discovered_forward.intersection(discovered_backward)) >= 1:
			index_f = parent_index_f + 1
			parents_forward[index_f] = parent_index_f
			index_state_map_f[index_f] = ('0', current_state_forward)

			index_b = parent_index_b + 1
			parents_backward[index_b] = parent_index_b
			# index_state_map_b[index_b] = ('0', current_state_backward)

			tiles_f, tiles_b = [], []
			while parents_forward[index_f] and parents_backward[index_b]:
				tiles_f.append(index_state_map_f[index_f][0])
				index_f = parents_forward[index_f]

				tiles_b.append(index_state_map_b[index_b][0])
				index_b = parents_backward[index_b]
			to_ret = list(reversed(tiles_f)) + tiles_b
			to_ret.remove('0')
			return to_ret

		for moved_f, neighbor_f in ComputeNeighbors(current_state_forward):
			check_f = tuple(neighbor_f.items())
			if  check_f not in discovered_forward:
				index_f = parent_index_f + 1
				parents_forward[index_f] = parent_index_f
				index_state_map_f[index_f] = (moved_f, neighbor_f)
				frontier_forward.append((index_f, neighbor_f))
				discovered_forward.add(check_f)

		for moved_b, neighbor_b in ComputeNeighbors(current_state_backward):
			check_b = tuple(neighbor_b.items())
			if check_b not in discovered_backward:
				index_b = parent_index_b + 1
				parents_backward[index_b] = parent_index_b
				index_state_map_b[index_b] = (moved_b, neighbor_b)
				frontier_backward.append((index_b, neighbor_b))
				discovered_backward.add(check_b)
	return None

def BidirectionalWIP(state):
	goal = find_goal(state)
	index_f = 0
	index_b = 0
	frontier_forward = [(index_f,state)]
	frontier_backward = [(index_b, goal)]

	discovered_forward = set(tuple(state.items()))
	discovered_backward = set(tuple(goal.items()))

	parents_forward = {index_f: None}
	parents_backward = {index_b: None}

	index_state_map_f = {index_f: (0, state)}
	index_state_map_b = {index_b: (0, goal)}

	while frontier_forward and frontier_backward:
		
		(parent_index_f, current_state_forward) = frontier_forward.pop(0)
		(parent_index_b, current_state_backward) = frontier_backward.pop(0)

		discovered_forward.add(tuple(current_state_forward.items()))
		discovered_backward.add(tuple(current_state_backward.items()))

		if len(discovered_forward.intersection(discovered_backward)) >= 1:
			index_f = parent_index_f + 1
			parents_forward[index_f] = parent_index_f
			index_state_map_f[index_f] = ('0', current_state_backward)

			index_b = parent_index_b + 1
			parents_backward[index_b] = parent_index_b
			# index_state_map_b[index_b] = ('0', current_state_backward)

			tiles_f, tiles_b, states_f, states_b = [], [], [], []
			while parents_forward[index_f] and parents_backward[index_b]:
				tiles_f.append(index_state_map_f[index_f][0])
				states_f.append(index_state_map_f[index_f])
				index_f = parents_forward[index_f]

				tiles_b.append(index_state_map_b[index_b][0])
				states_b.append(index_state_map_b[index_b])
				index_b = parents_backward[index_b]
			to_ret = list(reversed(tiles_f)) + tiles_b
			to_ret.remove('0')
			return to_ret, list(reversed(states_f)) + states_b

		# (moved_f, neighbor_f), (moved_b, neighbor_b) = (ComputeNeighbors(current_state_forward), ComputeNeighbors(current_state_backward))
		# # moved_f, neighbor_f = forward[0], for
		# # print(both_neighbors)
		# print(moved_f, neighbor_f, moved_b, neighbor_b)

		for moved_f, neighbor_f in ComputeNeighbors(current_state_forward):
			check_f = tuple(neighbor_f.items())
			if  check_f not in discovered_forward:
				index_f = parent_index_f + 1
				parents_forward[index_f] = parent_index_f
				index_state_map_f[index_f] = (moved_f, neighbor_f)
				frontier_forward.append((index_f, neighbor_f))
				discovered_forward.add(check_f)

		for moved_b, neighbor_b in ComputeNeighbors(current_state_backward):
			check_b = tuple(neighbor_b.items())
			if check_b not in discovered_backward:
				index_b = parent_index_b + 1
				parents_backward[index_b] = parent_index_b
				index_state_map_b[index_b] = (moved_b, neighbor_b)
				frontier_backward.append((index_b, neighbor_b))
				discovered_backward.add(check_b)
	return None

def h(current, goal):
	man_dist = 0
	for i in current:
		if i != "*":
			(x_i, y_i) = current[i]
			(x_g, y_g) = goal[i]
			man_dist += abs(x_i - x_g) + abs(y_i-y_g)
	return man_dist

def AStar(state):
	index = 0
	g_score = 0
	goal = find_goal(state)
	f_score = g_score + h(state, goal)
	frontier = hq.heapify([(f_score, g_score, index)])
	discovered = set(tuple(state.items()))
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_f, parent_g, parent_index) = hq.heappop(frontier)
		discovered.add(tuple(current_state.items()))

		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]

		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index = parent_index+1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)

				g_score = parent_g + 1
				f_score = h(neighbor, goal) + g_score
				hq.heappush(frontier, (f_score, g_score, index))
				print(frontier)
				discovered.add(check)

	print(index_state_map)
	return None

def AStarWIP(state):
	index = 0
	g_score = 0
	goal = find_goal(state)
	# print(goal)
	f_score = h(state, goal)+g_score
	
	g, f = {}, {}
	g[index] = g_score
	f[index] = h(state, goal)+g_score

	close_vertices = set()
	# print(tuple(state.items()))
	open_vertices = set()
	open_vertices.add(tuple(state.items()))


	frontier = [(f_score, g_score, index)]
	# discovered = set(tuple(state.items()))
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		current_state = None
		current_F_score = None
		for (f_score, g_score, index) in frontier:
			if current_state is None or f[index] < current_F_score:
				current_F_score = f[index]
				current_state = index_state_map[index][1]
				parent_f_score, parent_g_score, parent_index = f_score, g_score, index

		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)

		frontier.remove((parent_f_score, parent_g_score, parent_index))
		tuple_state = tuple(current_state.items())		
		# print(open_vertices)
		# print(tuple_state)
		# open_vertices.remove(tuple_state)
		close_vertices.add(tuple_state)

		# (parent_f_score, parent_g_score, parent_index) = frontier.pop(0)
		# current_state = index_state_map[parent_index][1]
		# # print(current_state)
		# print(frontier)
		# discovered.add(tuple(current_state.items()))
		# g_score = parent_g_score+1

		for moved, neighbor in ComputeNeighbors(current_state):
			tuple_neighbor = tuple(neighbor.items())
			if tuple_neighbor in close_vertices:
				continue
			temp_g = g[parent_index] + 1
			if tuple_neighbor not in open_vertices:
				open_vertices.add(tuple_neighbor)
			elif temp_g >= g[index]:
				continue
			
			index = parent_index+1
			index_state_map[index] = (moved, neighbor)
			parents[index] = parent_index
			# print(neighbor)
			g[index] = temp_g
			H = h(neighbor, goal)
			f[index] = g[index] + H
			frontier.append((f[index], g[index], index))
			# check = tuple(neighbor.items())
			# if check not in discovered:
			# 	
			# 	parents[index] = parent_index
			# 	index_state_map[index] = (moved, neighbor)
			# 	f_score = h(neighbor, goal) + g_score
			# 	heapq.heappush(frontier, (f_score, g_score, index))
			# 	discovered.add(check)
	print(index_state_map)
	return None

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

# tiles, path, states = BFS_WIP(state)
# tiles, path, states = DFS_WIP(state)
print(AStar(state))
# tiles, states = BidirectionalWIP(state)
print(states)
# for i in states:
# 	DebugPrint(size, i[1])
print(tiles)
print(path)
# print(len(tiles), len(path), len(states))

# tiles = BFS(state)
# print(tiles)

# tiles = DFS(state)
# print(tiles)

# tiles = BidirectionalSearch(state)
# print(tiles)

