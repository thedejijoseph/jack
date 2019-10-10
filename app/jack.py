
import core
from core import *


def process(order):
	""""""

	timer = core.Timer()
	timer.start()
	total_size = 0
	
	order = order.lower()
	
	if True:
		if order in cache:
			serving = cache.get(order)
			timer.finish()
			total_time = timer.time_taken()
			total_size = len(serving)
			delivery = {"serving": serving, "size": total_size, "time": total_time}
			
			return delivery
		
		# order is not cached
		# and if order is not in cache its not larger than 9
		tray = core.prepare(order)
		serving = core.serve(tray)
		timer.finish()
		total_time = timer.time_taken()
		total_size = len(serving)
		delivery = {"serving": serving, "size": total_size, "time": total_time}
		
		cache_this(order, serving)
		return delivery
	
def real_time(order):
	timer = core.Timer()
	timer.start()
	total_count = 0
	
	order = order.lower()
	if True:
		# real time processing
		tray = core.prepare(order)
		for dish in tray:
			serving = core.serve(dish)
			
			# because i cant get anything meaningful out of javascript
			# with my phone, ill do the cutting here.
			# cut into blocks of 3 for blk_size < 9
			# and 2 for blk_size < 12. we're working with 12 as max limit
			
			if serving:
				# if the serving is not empty
				count = len(serving); total_count += count
				blk_size = len(serving[0])
				serving = cut_into_blocks(serving)
				delivery = {"serving": serving, "blk_size": blk_size, "blk_count": count}
				yield delivery
		
		# finishing up
		timer.finish()
		total_time = timer.time_taken()
		
		package = {"time": total_time, "order": order, "count": total_count}
		yield package

def drive_in(order):
	"""for access from the terminal"""
	
	timer = core.Timer()
	timer.start()
	total_size = 0
	
	order = order.lower()
	tray = core.prepare(order)
	for dish in tray:
		if dish:
			serving = core.serve(dish)
			
			length = len(dish[0])
			size = len(serving)
			total_size += size
			
			print(length, "lettered", size, "large")
			print("-" * 7)
			fine_print(serving)
	
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
