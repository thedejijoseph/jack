import os
import sys
import itertools

file = open("assets/words.txt").read()
menu = set(file.splitlines())

def boil(order):
	# fetch all possiblities
	# from length 3 to word length
	
	board = []
	
	for i in range(3, len(order) + 1):
		options = itertools.permutations(order, i)
		for entry in options:
			dish = ''.join(entry)
			if dish in menu:
				board.append(dish)
	
	return board

def serve(board):
	# re orders found possiblities
	
	# trim repeats
	bowl = list(set(board))
	max_length = 0
	
	tray = []
	
	# get the length of the longest word
	for word in bowl:
		if len(word) >= max_length:
			max_length = len(word)
	
	for l in range(3, max_length + 1):
		select = [word for word in bowl if len(word) == l]
		select.sort()
		tray.extend(select)
	
	return tray

def fine_print(dish):
	print(order, f"({len(dish)})")
	print("-" * len(order))
	
	if len(dish) <= 6:
		[print(">", i) for i in dish]
		print("")
		
	else:
		split = len(dish) // 2
		one, two = dish[:split], dish[split:]
		
		if len(two) > len(one):
			one.append(two.pop(0))
		
		# we assume a max arg len of 7
		width = 10
		
		# terminal_size = os.get_terminal_size().columns
		# width = terminal_size // 2
		
		for i in range(len(two)):
			print(one[i].ljust(width), two[i].ljust(width))
		
		if len(one) > len(two):
			print(one[-1].ljust(width))
		
		print("")

def process(order):
	board = boil(order)
	tray = serve(board)
	
	return tray

if __name__ == "__main__":
	app, *orders = sys.argv
	for order in orders:
		dish = process(order)
		fine_print(dish)