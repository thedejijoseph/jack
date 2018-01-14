#! ~/../usr/bin/python

import os
import sys
import itertools
import logging
import threading

logging.basicConfig(
	level = logging.DEBUG,
	format = "%(asctime)s | %(levelname)s | %(message)s"
)

file = open("assets/words.txt").read()
menu = set(file.splitlines())

scramble = itertools.permutations
table = {}
cache = []

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
	"""Re-orders argument alphabetically.
	serve(arg) >> sorted_list
	Where arg could be a generator or a list.
	"""
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

def get_stack_size(delivery):
	"""Compute feasible stack_size to slice the delivery into.
	Returns a greater than zero integer, a comfortable stack_size.
	Zero (0, 0) if there was an error.
	"""
	
	# delivery should always be a non-empty list
	if type(delivery) != list or delivery == []:
		return 0, 0
	
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
	
	stack_size = t_width // (stretch + 2)
	
	return stack_size, stretch
	
def sort_by_x(delivery, stack_size):
	"""
	+ delivery sorted horizontally (not really).
	
	where x is the stack_size.
	this returns a list of stacks, stack_size long.
	"""
	stacks = []
	
	while True:
		cut = delivery[:stack_size]
		stacks.append(cut)
		delivery = delivery[stack_size:]
		if delivery == []:
			break
	
	return stacks

def sort_by_y(delivery, stack_size):
	"""
	+ delivery sorted vertically (not really too).
	
	lets say y is the stack_size here too
	this returns a list of stacks with variable length,
	but each stack is stack_size long.
	"""
	stacks = []
	
	while True:
		cut = delivery[:stack_size]
		if stacks != []:
			for item in cut:
				stacks[cut.index(item)].append(item)
		else:
			for item in cut:
				stacks.append([item])
		delivery = delivery[stack_size:]
		if delivery == []:
			break
	
	return stacks

def fine_print(delivery):
	"""Pretty-print content of the stack.
	stacks is a list of lists (stacks)
	"""
	
	stack_size, stretch = get_stack_size(delivery)
	stacks = sort_by_x(delivery, stack_size)
	
	# i think y looks better than x though
	
	for stack in stacks:
		for item in stack:
			print(item.ljust(stretch + 2), end="")
		print("")
	
	print("")

def process(order, chain="web", large=False):
	"""Jack's public face."""
	
	if chain == "web":
		# implement static caches
		
		if order in cache:
			return table.get(order)
		
		cache.append(order)
		
		dish = prepare(order)
		serving = serve(dish)
		
		table[order] = serving
		
		return serving
	
	elif chain == "terminal":
		# normalize
		order = order.lower()
		
		# to-do:
		# fine_print.ing larger
		# orders straight from the generator
		
		dish = prepare(order)
		serving = serve(dish)
		
		if serving == []:
			# how about a smarter feedback
			feedback = f"{order}: 0 servings"
			
		elif len(serving) == 1:
			feedback = f"{order}: a special!"
		
		else:
			feedback = f"{order}: {len(serving)} servings"
		
		print(feedback)
		print("=" * 12)
		fine_print(serving)


if __name__ == "__main__":
	app, *orders = sys.argv
	
	for order in orders:
		process(order, chain="terminal")
