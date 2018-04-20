import time
from resource import *

def process(order):
	"""jack's process logic"""
	
	t1 = time.time()
	order = order.lower()
	
	# establish a threshold of length 9..
	if len(order) >= 9:
		if order in cache:
			serving = cache.get(order)
			t2 = time.time()
			tt = "%.2f" %(t2 - t1)
			return tt, serving
	
	# <9 orders
	# and never processed >9 orders
	dish = prepare(order)
	serving = serve(dish)
	
	t2 = time.time()
	tt = "%.2f" %(t2 - t1)
	
	cache_this(order, serving)
	return tt, serving

def drive_in(order):
	time_taken, serving = process(order)
	
	unit = "seconds"
	if time_taken == "1.00":
		unit = "second"
	
	if serving == []:
		# how about a smarter feedback
		feedback = f"{order}: 0 servings ({time_taken} {unit})"
		
	elif len(serving) == 1:
		feedback = f"{order}: a special! ({time_taken} {unit})"
	
	else:
		feedback = f"{order}: {len(serving)} servings ({time_taken} {unit})"
	
	print(feedback)
	print("=" * 12)
	fine_print(serving)


if __name__ == "__main__":
	import sys
	app, *orders = sys.argv
	
	for order in orders:
		drive_in(order)
