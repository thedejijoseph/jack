
import resource
from resource import *

# changes:
	# established order length threshold
	# fixed large order printing (real time)
	# switched to resource timer


def process(order):
	"""jack's process logic"""
	
	timer = resource.Timer()
	timer.start()
	order = order.lower()
	
	# establish a threshold of length 9..
	if len(order) >= 9:
		if order in cache:
			serving = cache.get(order)
			timer.finish()
			tt = timer.time_taken()
			return tt, serving
	
	# <9 orders
	# and never processed >9 orders
	dish = prepare(order)
	serving = serve(dish)
	
	timer.finish()
	tt = timer.time_taken()
	
	cache_this(order, serving)
	return tt, serving

def drive_in(order):
	timer = resource.Timer()
	timer.start()
	total_size = 0
	
	large = resource.prepare(order)
	for batch in large:
		if batch:
			length = len(batch[0])
			rough = resource.serve(batch)
			size = len(rough)
			total_size += size
			
			print(length, "lettered", size, "large")
			print("=" * 7)
			fine_print(rough)
	timer.finish()
	report(order, total_size, timer.time_taken())
	print("")


if __name__ == "__main__":
	import sys
	app, *orders = sys.argv
	
	for order in orders:
		try:
			drive_in(order)
		except KeyboardInterrupt:
			print(f"\nCANCELLING {order}..")
			print("")
			pass
