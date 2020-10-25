import numpy as np
import math
import copy
import time
from queue import PriorityQueue

def LoadFromFile(file):
	n = 0
	initial = []
	with open(file, 'r') as f:
		n = int(next(f))
		trusted = [str(i) for i in range(1, n*n )] #expected characters
		trusted.append("*")
		for i in f:
			to_append = i[:-1].split('\t') #split line on tabs until the last character with new line char dropped
			if '' in to_append or len(to_append) != n: #if '' in to_append then there were 2 consecutive tabs 
				print("Error, invalid file")
				return None
			temp = []
			for x in to_append:
				if x in trusted:
					temp.append(x)
					trusted.remove(x)
				#each time we get an expected character we remove it from the valid list so as to evade duplicates 
				#or numbers not in the defined range
				else:
					print("Error, invalid file: unexpected character, not int from 1-n^2 or * or duplicate")
					return None
			initial.append(temp)

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
	options = [(blank[0]-1, blank[1]), (blank[0]+1, blank[1]), (blank[0], blank[1]-1), (blank[0], blank[1]+1)] 
	# list of options in up, down, left, right order
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

#this method was made primarily because Bidirection requires the goal and I wasn't gonna write the same code twice
def find_goal(state):
	values = list(state.values())
	keys = [str(x) for x in range(1, len(state))]
	keys.append('*')
	return dict(zip(keys, values))

def IsGoal(state):
	return state == find_goal(state)

#step back through the indices to reconstruct the tiles, path of indices and states traversed
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

#Of the following methods, all of the [blank]WIP methods are the methods used to test bugs and other changes so as not 
#to break the working code. Once the code in the WIP method functions, it is moved to the main method.

def BFS(state):
	index = 0 #index here is used as a way to enumerate the states in order to keep track of them and access them in dictionaries
	frontier = [(index, state)]
	discovered = set([tuple(state.items())]) #if you don't pass it with the brackets it treats each key, value pair as an individual entry and not the state as a whole
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]	
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index += 1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				frontier.append((index, neighbor))
				discovered.update([check]) #needed to keep the tuple of the state together and not be expanded
	return None

def BFS_WIP(state):
	index = 0
	frontier = [(index, state)]
	discovered = set([tuple(state.items())])
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		# index = parent_index
		# discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			print(parents)
			print(index_state_map)
			return reconstruct(current_state, parent_index, parents, index_state_map)
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index += 1
				# print("before index map")
				# DebugPrint(math.sqrt(len(neighbor)), neighbor)
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				# print("from index map")
				# DebugPrint(math.sqrt(len(index_state_map[index][1])), index_state_map[index][1])
				frontier.append((index, neighbor))
				discovered.update([check])
	return None

def DFS(state):
	index = 0
	frontier = [(index, state)]
	discovered = set([tuple(state.items())])
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index += 1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				frontier.insert(0, (index, neighbor))
				discovered.update([check])
	return None

def DFS_WIP(state):
	index = 0
	frontier = [(index, state)]
	discovered = set([tuple(state.items())])
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while frontier:
		(parent_index, current_state) = frontier.pop(0)
		# index = parent_index
		# discovered.add(tuple(current_state.items()))
		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]
		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index += 1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				frontier.insert(0, (index, neighbor))
				discovered.update([check])
	return None

def BidirectionalSearch(state):
	goal = find_goal(state)

	index_f = 0
	index_b = 0

	frontier_f = [(index_f, state)]
	frontier_b = [(index_b, goal)]

	discovered_f = set([tuple(state.items())])
	discovered_b = set(tuple(goal.items()))

	parents_f = {index_f: None}
	parents_b = {index_b: None}

	index_state_map_f = {index_f: (0, state)}
	index_state_map_b = {index_b: ('*', goal)}

	while frontier_f and frontier_b:
		(parent_index_f, current_state_f) = frontier_f.pop(0)
		(parent_index_b, current_state_b) = frontier_b.pop(0)

		discovered_f.update([tuple(current_state_f.items())])
		discovered_b.update([tuple(current_state_b.items())])

		if len(discovered_f.intersection(discovered_b)) > 0:

			del index_state_map_f[list(index_state_map_f.keys())[-1]]
			del index_state_map_b[list(index_state_map_b.keys())[-1]]
			
			tiles_f = []
			states_f = []
			for i in index_state_map_f:
				tiles_f.append(index_state_map_f[i][0])
				states_f.append(index_state_map_f[i][1])
			
			tiles_b = []
			states_b = []
			for i in index_state_map_b:
				tiles_b.append(index_state_map_b[i][0])
				states_b.append(index_state_map_b[i][1])

			tiles_to_ret = tiles_f + list(reversed(tiles_b))
			
			temp = tiles_to_ret[0]
			for i in tiles_to_ret[1:]:
				if i == temp:
					tiles_to_ret.remove(i)
				temp = i
			
			return tiles_to_ret[1:] #the first is labelled 0 so not rnt really a move

		for moved_f, neighbor_f in ComputeNeighbors(current_state_f):
			check_f = tuple(neighbor_f.items())
			if check_f not in discovered_f:
				index_f += 1
				parents_f[index_f] = parent_index_f
				index_state_map_f[index_f] = (moved_f, neighbor_f)
				frontier_f.append((index_f, neighbor_f))
				discovered_f.update([check_f])

		for moved_b, neighbor_b in ComputeNeighbors(current_state_b):
			check_b = tuple(neighbor_b.items())
			if check_b not in discovered_b:
				index_b += 1
				parents_b[index_b] = parent_index_b
				index_state_map_b[index_b] = (moved_b, neighbor_b)
				frontier_b.append((index_b, neighbor_b))
				discovered_b.update([check_b])
	return None

def BidirectionalWIP(state):
	goal = find_goal(state)

	index_f = 0
	index_b = 0

	frontier_f = [(index_f, state)]
	frontier_b = [(index_b, goal)]

	discovered_f = set([tuple(state.items())])
	discovered_b = set(tuple(goal.items()))

	parents_f = {index_f: None}
	parents_b = {index_b: None}

	index_state_map_f = {index_f: (0, state)}
	index_state_map_b = {index_b: ('*', goal)}

	while frontier_f and frontier_b:
		(parent_index_f, current_state_f) = frontier_f.pop(0)
		(parent_index_b, current_state_b) = frontier_b.pop(0)
		# print(ComputeNeighbors(current_state_f))
		# index_f = parent_index_f
		# index_b = parent_index_b

		# print(current_state_f.items())
		discovered_f.update([tuple(current_state_f.items())])
		# print(discovered_f)

		discovered_b.update([tuple(current_state_b.items())])
		# print(discovered_f, discovered_b)
		# print(discovered_f.intersection(discovered_b))

		if len(discovered_f.intersection(discovered_b)) > 0:
			# print([value for key, value in index_state_map_f])
			# index_f = parent_index_f + 1
			# parents_f[index_f] = parent_index_f
			# index_state_map_f[index_f] = (index_state_map_f[parent_index_f][0], current_state_f)

			# index_b = parent_index_b + 1
			# parents_b[index_b] = parent_index_b
			# index_state_map_b[index_b] = (index_state_map_b[parent_index_b][0], current_state_b)

			del index_state_map_f[list(index_state_map_f.keys())[-1]]
			del index_state_map_b[list(index_state_map_b.keys())[-1]]
			# print(parents_f, "\n")
			print(index_state_map_f,"\n")
			# print(parents_b, "\n")
			# print(index_state_map_b)
			# print(discovered_f.intersection(discovered_b))
			print("forward")
			tiles_f = []
			states_f = []
			for i in index_state_map_f:
				# print(index_state_map_f[i])
				tiles_f.append(index_state_map_f[i][0])
				states_f.append(index_state_map_f[i][1])
				# DebugPrint(4, index_state_map_f[i][1])
			
			print("back")
			tiles_b = []
			states_b = []
			for i in index_state_map_b:
				# print(index_state_map_b[i])
				tiles_b.append(index_state_map_b[i][0])
				states_b.append(index_state_map_b[i][1])
				# DebugPrint(4, index_state_map_b[i][1])

			tiles_to_ret = tiles_f + list(reversed(tiles_b))
			
			temp = tiles_to_ret[0]
			for i in tiles_to_ret[1:]:
				if i == temp:
					tiles_to_ret.remove(i)
				temp = i
			
			print(tiles_to_ret)
			return tiles_to_ret
			states_to_ret = states_f + states_b
			print(states_to_ret)
			for i in states_to_ret:
				DebugPrint(4, i)
			# print(discovered_f, "\n")
			# print(discovered_b)

			tiles_f, tiles_b, states_f, states_b = [], [], [], []
			while parents_f[index_f] and parents_b[index_b]:
				tiles_f.append(index_state_map_f[index_f][0])
				states_f.append(index_state_map_f[index_f])
				# DebugPrint(4, index_state_map_f[index_f][1])
				index_f = parents_f[index_f]

				tiles_b.append(index_state_map_b[index_b][0])
				states_b.append(index_state_map_b[index_b])
				# DebugPrint(4, index_state_map_b[index_b][1])
				index_b = parents_b[index_b]
			to_ret = list(reversed(tiles_f)) + tiles_b
			# print(parents_f, parents_b)
			return to_ret, list(reversed(states_f)) + states_b

		for moved_f, neighbor_f in ComputeNeighbors(current_state_f):
			check_f = tuple(neighbor_f.items())
			if check_f not in discovered_f:
				index_f += 1
				parents_f[index_f] = parent_index_f
				index_state_map_f[index_f] = (moved_f, neighbor_f)
				frontier_f.append((index_f, neighbor_f))
				discovered_f.update([check_f])

		for moved_b, neighbor_b in ComputeNeighbors(current_state_b):
			check_b = tuple(neighbor_b.items())
			if check_b not in discovered_b:
				index_b += 1
				parents_b[index_b] = parent_index_b
				index_state_map_b[index_b] = (moved_b, neighbor_b)
				frontier_b.append((index_b, neighbor_b))
				discovered_b.update([check_b])
	return None
	
def h(current, goal):
	man_dist = 0
	for i in current:
		(x_i, y_i) = current[i]
		(x_g, y_g) = goal[i]
		man_dist += abs(x_i - x_g) + abs(y_i-y_g)
	return man_dist

def AStar(state):
	index = 0
	g_score = 0
	goal = find_goal(state)
	f_score = g_score + 2*h(state, goal)
	q = PriorityQueue()
	q.put((f_score, g_score, index))
	discovered = set([tuple(state.items())])
	parents = {index: None}
	index_state_map = {index: (0, state)}
	while not q.empty():
		(parent_f, parent_g, parent_index) = q.get()
		# index = parent_index
		current_state = index_state_map[parent_index][1]
		discovered.add(tuple(current_state.items()))

		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]

		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index += 1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				discovered.update([check])

				g_score = parent_g + 1
				f_score = 2*h(neighbor, goal) + g_score
				q.put((f_score, g_score, index))		
	return None

def AStarWIP(state):
	index = 0
	g_score = 0
	goal = find_goal(state)
	f_score = g_score + 2*h(state, goal)
	q = PriorityQueue()
	q.put((f_score, g_score, index))
	# hq.heapify(frontier)
	discovered = set([tuple(state.items())])
	parents = {index: None}
	index_state_map = {index: (0, state)}
	# print(frontier)
	while not q.empty():
		# print(q)
		(parent_f, parent_g, parent_index) = q.get()
		index = parent_index
		current_state = index_state_map[parent_index][1]
		# DebugPrint(math.sqrt(len(current_state)), current_state)
		discovered.add(tuple(current_state.items()))

		if IsGoal(current_state):
			return reconstruct(current_state, parent_index, parents, index_state_map)[0]

		for moved, neighbor in ComputeNeighbors(current_state):
			check = tuple(neighbor.items())
			if check not in discovered:
				index += 1
				parents[index] = parent_index
				index_state_map[index] = (moved, neighbor)
				discovered.update([check])

				g_score = parent_g + 1
				f_score = 2*h(neighbor, goal) + g_score
				q.put((f_score, g_score, index))
				
	# print(index_state_map)
	return None

start = time.time()
size, state = LoadFromFile("input.txt")
# print(state)
print("Start State")
DebugPrint(size, state)
# neighbors = ComputeNeighbors(state)
# print(neighbors)
# for i, j in neighbors:
# 	print("tile moved: " + str(i))
# 	DebugPrint(size, j)
# IsGoal(state)

# print("Search")
print("Solution")
# print(state)

# tiles, path, states = BFS_WIP(state)
# tiles, path, states = DFS_WIP(state)
# print(AStarWIP(state))
# tiles, states = BidirectionalWIP(state)
# print(states)
# for i in states:
# 	DebugPrint(size, i[1])
# print(tiles)
# print(path)
# print(len(tiles), len(path), len(states))

# tiles = BFS(state)
# print(tiles)

# tiles = DFS(state)
# print(tiles)

# tiles = BidirectionalSearch(state)
# print(tiles)

tiles = AStar(state)
print(tiles)

print("Time taken: " + str(time.time() - start))