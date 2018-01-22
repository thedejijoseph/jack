#! ~/../usr/bin/python

import os
import sys
import itertools
import logging
import threading
import types
import json

logging.basicConfig(
	level = logging.DEBUG,
	format = "%(asctime)s | %(levelname)s | %(message)s"
)

source_file = open("assets/words.txt").read()
menu = set(source_file.splitlines())

scramble = itertools.permutations
cache = {}

def prepare(order):
	"""Permutates given argument (string)
	returns a generator object of valid permutations.
	"""
	size = len(order)
	# removed size checks
	# even though 10+ sizes take really long
	
	for i in range(2, size + 1):
		yield [''.join(dish) for dish in scramble(order, i) if ''.join(dish) in menu]
		
def serve(bowls):
	"""Re-orders argument alphabetically.
	serve(arg) >> sorted_list
	Where arg could be a generator or a list.
	"""
	queue = []
	
	if isinstance(bowls, types.GeneratorType):
		# arg is a generator
		# already cut into bowls of same size
		for bowl in bowls:
			if bowl is []:
				pass
			bl = list(set(bowl))
			bl.sort()
			queue.extend(bl)
		return queue
	
	# not a generator
	# cut list into lists of the same size
	
	stretch = 0
	for i in bowls:
		if len(i) > stretch:
			stretch = len(i)
	
	for i in range(2, stretch + 1):
		grp = [x for x in filter(lambda k: True if i == len(k) else False, bowls)]
		grp.sort()
		queue.extend(grp)
	
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

def repool():
	global pool
	pool = set(cache.keys())

def load_cache():
	logging.debug("loading cache")
	cache_file_id = "assets/saved.txt"
	cache_file = open(cache_file_id, "r")
	
	open_cache = cache_file.read().splitlines()
	for line in open_cache:
		item, entry = line.split(": ")
		cache[item] = serve(json.loads((entry)))
		repool()

def cache_this(item, entry):
	"""Add a just processed order to the cache"""
	
	cache[item] = entry
	# redo the pool (index)
	repool()

def engage(order):
	"""Perform the work flow from order to delivery."""
	
	bowl = prepare(order)
	serving = serve(bowl)
	
	cache_this(order, serving)
	return serving

def quick_look(order):
	"""See if the word is just scrambled"""
	
	options = [''.join(i) for i in scramble(order)]
	for e in options:
		if e in menu:
			return e
	
	return None

def process(order):
	"""Jack's public face."""
	# just for web access
	
	# is the order a valid word
	if order in pool:
		return cache[order]
	
	# never before processed
	# see if its a valid word just scrambled
	# is it: if its in the cache: good
	# if not: process it
	check = quick_look(order)
	if check:
		return cache.get(check[0], engage(order))
	
	return engage(order)
	
	# todo:
		# convergence

def quick_access(order):
	# just for terminal access
	# no need to complicate things
	
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

# interrupting terminal access
if __name__ != "__main__":
	threading.Thread(target=load_cache).start()

if __name__ == "__main__":
	app, *orders = sys.argv
	
	for order in orders:
		quick_access(order)
