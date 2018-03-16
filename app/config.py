import logging
import itertools

import requests

logging.basicConfig(
	level = logging.DEBUG,
	format = "%(asctime)s | %(levelname)s | %(message)s"
)


# setup
# -----

scramble = itertools.permutations

file_host = "https://cdn.rawgit.com/wrecodde/jack/master/"

try:
	# check locally
	word_file_path = "assets/words.txt"
	with open(word_file_path) as words_file:
		words = words_file.read().splitlines()
		word_bank = set(words)
except FileNotFoundError:
	word_file_url = file_host + "assets/words.txt"
	r = requests.get(word_file_url)
	words = r.text.splitlines()
	word_bank = set(words)
except:
	import sys
	sys.exit()

