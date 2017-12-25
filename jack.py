from pprint import pprint as waiter
from itertools import permutations as scramble

file = open("words.txt").read()
menu = set(file.splitlines())

order = input("whats your order: ")

def boil(order):
	board = []
	
	for i in range(3, len(order) + 1):
		options = scramble(order, i)
		for entry in options:
			dish = ''.join(entry)
			if dish in menu:
				board.append(dish)
	
	return board

def serve(board):
	bowl = list(set(board))
	max_length = 0
	
	tray = []
	
	for word in bowl:
		if len(word) >= max_length:
			max_length = len(word)
	
	for l in range(3, max_length + 1):
		select = [word for word in bowl if len(word) == l]
		select.sort()
		tray.extend(select)
	
	return tray

board = boil(order)
tray = serve(board)

waiter(tray)