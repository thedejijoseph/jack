#! ~/../usr/bin/python

import os
import sys
import itertools
import logging

logging.basicConfig(
	level = logging.DEBUG,
	format = "%(asctime)s | %(levelname)s | %(message)s"
)

file = open("assets/words.txt").read()
menu = set(file.splitlines())

scramble = itertools.permutations

def prepare(order):
	# permutates given argument "string"
	# returns a generator object of valid permutations
	order = list(order)
	
	size = len(order)
	if size < 3 or size >= 15:
		# unintelligible length
		yield []
	
	for i in range(3, size + 1):
		yield [''.join(dish) for dish in scramble(order, i) if ''.join(dish) in menu]
		
def serve(bowls):
	# re-orders argument alphabetically
	# serve(arg) >> sorted_list
	# where arg could be a generator or a list
	queue = []
	
	def spice(bowl):
		bowl = list(set(bowl))
		bowl.sort()
		queue.extend(bowl)
	
	if type(bowls) != list:
		# arg is a generator
		# (an assumption) tests for a generator?
		for bowl in bowls:
			if bowl is []:
				pass
			spice(bowl)
		return queue
	
	# not a generator
	bowl = bowls
	spice(bowl)
	return queue

def fine_print(delivery):
	# pretty prints arg to the terminal
	# where delivery could be from prepare()
	# or a complete list from serve()
	
	def compute(delivery):
		# delivery should always be a non-empty list
		if type(delivery) != list or delivery == []:
			pass
		
		# the trick is to get the optimal dimensions
		# to split the delivery into
		size = len(delivery)
		
		# get the longest item
		stretch = 0
		for i in delivery:
			if len(i) > stretch:
				stretch = len(i)
		
		# terminal width and height
		t_width = os.get_terminal_size().columns
		t_height = os.get_terminal_size().lines
		
		# comfortable width
		space = t_width // stretch + 2
		depth = size // space
		
		if size > t_height:
			rows = size
		else:
			rows = depth
		
		stack = []
		while delivery:
			cut = delivery[:rows]
			stack.append(cut)
			delivery = delivery[rows:]
			if delivery == []:
				break
		print("space, depth, size, len(stack)")
		print("len(stack[0]), len(stack[-1]), rows, stretch")
		print(space, depth, size, len(stack))
		print(len(stack[0]), len(stack[-1]), rows, stretch)
		
		print("t_width, t_height")
		print(t_width, t_height)
	
	if type(delivery) != list:
		# delivery is a generator object
		# (an assumption) how do i test for a generator?
		for batch in delivery:
			# sort generator delivery
			batch = serve(batch)
			compute(batch)
		return
	
	# filled up tray, carry on
	compute(delivery)
	return

def process(order, large=False):
	size = len(order)
	
	# might include preprocesses
	
	if large:
		# fine_print directly from prepare()
		fine_print(prepare(order))
		return
	
	dish = prepare(order)
	delivery = serve(dish)
	
	return delivery


if __name__ == "__main__":
	app, *orders = sys.argv
	
	for order in orders:
		if len(order) >= 10:
			# process(order, large=True)
			print(f"can't compute {order}: too large")
		else:
			tray = process(order)
			fine_print(tray)
