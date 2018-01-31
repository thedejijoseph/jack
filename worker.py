# worker.py
# started with a call to jack.py

# continuously make an external cache of
# deliveries (derived words) from each
# order (valid english words, in this case)


import threading
import logging
import queue
import json
import time

from itertools import permutations as scramble

logging.basicConfig(
	#filename = "assets/worker.log",
	level = logging.DEBUG,
	format = "%(asctime)s | %(levelname)s | %(message)s"
)

def is_undone(item):
	return True if item not in done else False

def load_cache(cache_file):
	# where cache_file is a txt file
	# return a dict of its content
	cache = {}
	content = cache_file.splitlines()
	
	for line in content:
		item, entry = line.split(": ")
		cache[item] = json.loads(entry)
	
	return cache

def process(word):
	# get all possible words from this word
	word = word.lower()
	perms = [scramble(word, i) for i in range(len(word)+1)]
	
	found = []
	for collct in perms:
		for possble in collct:
			word = ''.join(possble)
			if word in all_words:
				found.append(word)
	
	found = set(found)
	found = list(found)
	return found

def worker():
	while True:
		if work_queue.empty() is True:
			worker_checkout.append(1)
			break
		
		else:
			item = work_queue.get()
			
			logging.info(f"work: {item}")
			entry = process(item)
			package = item + ": " + json.dumps(entry)
			save_queue.put(package)
			logging.info(f"done: {item}")
			
			work_queue.task_done()

progress = []
def progress_report():
	# give feedback on workers progress
	so_far = len(progress)
	all = len(undone)
	left = all - so_far
	
	report = so_far / all * 100
	report = "%.2f" %report
	
	print(f"{so_far} out of {all}: {report}%")

def save():
	# all the work left to do has been queued
	# work has started and results are being queued
	# start saving!

	while True:
		if save_queue.empty() is False:
			package = save_queue.get()
			item = package.split(': ')[0]
			logging.info(f"save: {item}")
			
			# handled this way for assurance that
			# items saved (written to file) are saved
			
			save_file = open(save_file_path, "a")
			save_file.write(package + "\n")
			save_file.close()
			
			progress.append(1)
			progress_report()
		
		elif save_queue.empty() is True:
			# check if all work's been assigned
			if work_queue.empty():
				# check to see if all the workers are done
				if len(worker_checkout) == no_of_workers:
					# check to see if all the work's been saved
					if save_queue.empty:
						for wrkr in workers:
							wrkr.join()
						logging.info("all done!")
						break
							

def start():
	global done, undone, all_words
	global work_queue, save_queue
	global no_of_workers, workers
	global worker_checkout
	
	# settings
	print("where's what we need to work on")
	source_file_path = input("source file (rel path): ./")
	
	print("where do we save our work to")
	save_file_path = input("save file (rel path): ./")
	
	words_file = open("assets/words.txt", "r")
	all_words = set(words_file.read().splitlines())
	words_file.close()
	
	source_file = open(source_file_path, "r")
	save_file = open(save_file_path, "r")
	
	logging.info("setting up")
	source = source_file.read().splitlines()
	saved = load_cache(save_file.read())
	
	done = saved.keys()
	undone = [i for i in filter(is_undone, source)]
	
	if undone == []:
		logging.info("all clear!")
		return

	# now we have a list of items left to work on
	source_file.close()
	save_file.close() # to be opened again for writing
	
	# open up queue objects
	work_queue = queue.Queue()
	save_queue = queue.Queue()
	
	# start workers
	no_of_workers = 16
	workers = []
	worker_checkout = []

	logging.info("queuing work")
	for item in undone:
		work_queue.put(item)

	for i in range(no_of_workers):
		wrkr = threading.Thread(target=worker)
		wrkr.start()
		
		workers.append(wrkr)
	
	save()

if __name__ == "__main__":
	start()