# making the new dir structure work for heroku

import sys
sys.path = ["app"] + sys.path

import server
start = server.start
