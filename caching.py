from config import *

cache = {}

# importing this module should build a cache from
# available external sources: a database or txt file

def cache_this(order, serving):
	"""write the package to cache file and memory"""
	
	# this might include extra processes too
	cache[order] = serving