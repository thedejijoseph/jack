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
	filename = "assets/worker.log",
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
			break
		
		else:
			item = work_queue.get()
			
			logging.info(f"work: {item}")
			entry = process(item)
			package = item + ": " + json.dumps(entry)
			save_queue.put(package)
			logging.info(f"done: {item}")
			
			work_queue.task_done()

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
			
			save_file = open("assets/saved.txt", "a")
			save_file.write(package + "\n")
			save_file.close()
		
		elif save_queue.empty() is True:
			# check if all the work is done
			if work_queue.empty():
				# check again if all the work's been saved
				time.sleep(3)
				if save_queue.empty():
					# if this checks out, workers
					# would have stopped
					# close the threads!
					for wrkr in workers:
						wrkr.join()
					
					break

def start():
	global done, undone, all_words
	global work_queue, save_queue
	global no_of_workers, workers
	
	words_file = open("assets/words.txt", "r")
	all_words = set(words_file.read().splitlines())
	words_file.close()
	
	source_file = open("assets/1.txt", "r")
	save_file = open("assets/saved.txt", "r")
	
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