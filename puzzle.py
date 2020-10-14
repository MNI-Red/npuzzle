class Node:
	neighbors = []
	value = ""

	def __innit__ (value_in, neighbors_in):
		value = value_in
		neighbors = neighbors_in

def LoadFromFile(file):
	n = 0
	initial = []
	with open(file, 'r') as f:
		n = int(next(f))
		for i in f:
			# print(i)
			to_append = i[:-1].split('\t')
			# print(to_append)
			if '' in to_append or len(to_append) != n:
				print("Error, invalid file")
				return None
			initial.append([x for x in to_append if x == '*' or x.isdecimal()]) #take the chars if they are numbers or *
	if len(initial) != n:
		print("Error, invalid file")
		return None
	return n, initial

def print_game(state):
	for i in state:
		print(i)

LoadFromFile("input.txt")
# print_game(initial)