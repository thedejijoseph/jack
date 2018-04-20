# resource.py: hold app resource

import itertools
import types
import shutil
import os

import requests


__all__ = [
	"cache", "cache_this", 
	"prepare", "serve", 
	"fine_print"]

# config
# ------

scramble = itertools.permutations
file_host = "https://cdn.rawgit.com/wrecodde/jack/master/"

try:
	# check locally
	word_file_path = os.path.join(os.path.dirname(__file__), "assets/words.txt")
	with open(word_file_path) as words_file:
		words = words_file.read().splitlines()
		word_bank = set(words)
except:
	# removed external hosting option
	# external resources and lists would move with the app
	raise


# caching
# -------

# todo:
	# build and load a cache (a database or a text file)

cache = {}
def cache_this(order, serving):
	"""write the package to cache file and memory"""
	
	# this might include extra processes too
	cache[order] = serving

# app functions
# ------------

def prepare(order):
	"""Permutates given argument (string)
	returns a generator object of valid permutations.
	"""
	size = len(order)
	# removed size checks
	# even though 10+ sizes take really long
	
	for i in range(2, size + 1):
		yield [''.join(dish) for dish in scramble(order, i) if ''.join(dish) in word_bank]
		
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
	# cut list into lists of words the same size
	# [['ae', 'ea'], ['eat', 'tea'], [4], [5], ...]
	
	stretch = 0
	for i in bowls:
		if len(i) > stretch:
			stretch = len(i)
	
	for i in range(2, stretch + 1):
		grp = [x for x in filter(lambda k: True if i == len(k) else False, bowls)]
		grp.sort()
		queue.extend(grp)
	
	return queue


# supplementary methods
# ---------------------

def quick_look(order):
	"""See if the word is just scrambled"""
	
	options = [''.join(i) for i in scramble(order)]
	for e in options:
		if e in menu:
			return e
	
	return None


# for terminal access
# -------------------

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
	t_width = shutil.get_terminal_size().columns
	t_height = shutil.get_terminal_size().lines
	
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