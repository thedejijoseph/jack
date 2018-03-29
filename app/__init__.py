# making the new dir structure work for heroku

import sys
sys.path = ["app"] + sys.path

from .index import start
start = index.start
