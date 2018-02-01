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
import os
import sys

from itertools import permutations as scramble

# configure logger

# run through setup

# first: word bank
try:
	word_bank_path = "assets/words.txt"
	word_bank_file = open(word_bank_path, "r")
	word_bank = set(word_bank_file.read().splitlines())
	
	word_bank_file.close()
except:
	print(f"error locating word bank: {word_bank_path}")
	raise

# the cache file
try:
	save_file_path = "assets/saved.txt"
	save_file = open(save_file_path, "r")
	saved = save_file.read().splitlines()
	
	save_file.close()
except FileNotFoundError:
	print(f"error locating cache file: {save_file_path}")
	print("creating one")
	
	try:
		# try to create an 'assets' dir
		os.mkdir("assets")
	except:
		pass
	# create empty file
	save_file = open(save_file_path, "w")
	save_file.close()

# source file
if __name__ == "__main__":
	print("which source file (1, 2, 3, 4).txt")
	source_file_path = "assets/" + input("assets/")
	
	try:
		source_file = open(source_file_path, "r")
		source = source_file.read().splitlines()
		
		source_file.close()
	except:
		print(f"error locating source file: {source_file_path}")
		raise
else:
	# build a stack of the sources
	try:
		f1 = open("assets/1.txt", "r")
		f2 = open("assets/2.txt", "r")
		f3 = open("assets/3.txt", "r")
		f4 = open("assets/4.txt", "r")
		
		stack = []
		stack.extend(f1.read().splitlines())
		stack.extend(f2.read().splitlines())
		stack.extend(f3.read().splitlines())
		stack.extend(f4.read().splitlines())
		
		f1.close()
		f2.close()
		f3.close()
		f4.close()
		
		source = stack
	except:
		print("error building stack")
		raise

def is_undone(item):
	return True if item not in done else False

# build a list of saved items (done)
done = []
for item in saved:
	key, value = item.split(": ")
	done.append(key)

done = set(done)
undone = [i for i in filter(is_undone, source)]
	
if undone == []:
	print("source is all clear")
	sys.exit()

	
# open up queue objects
work_queue = queue.Queue()
save_queue = queue.Queue()

# workers
no_of_workers = 16
workers = []
worker_checkout = []

proceed = input("proceed (y/n): ")
if proceed == "n":
	sys.exit()

def stop_workers():
	for wrkr in workers:
		wrkr.join()

def process(word):
	# get all possible words from this word
	word = word.lower()
	scrambles = [scramble(word, i) for i in range(len(word)+1)]
	
	found = []
	for group in scrambles:
		for option in group:
			word = ''.join(option)
			if word in word_bank:
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
	# all the work has been queued and started
	# results are being queued

	while True:
		if save_queue.empty() is False:
			package = save_queue.get()
			item = package.split(": ")[0]
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
				# check if all the workers are done with
				# their work
				if len(worker_checkout) == no_of_workers:
					stop_workers()
					logging.info("all done!")
					break

def start():
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