import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado import gen

import os
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor()

import jack

logging.basicConfig(
	level = logging.DEBUG,
	format = "%(asctime)s | %(levelname)s | %(message)s",
)

from tornado.options import define
define("port", default=3303, help="open at given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
	pass

class IndexHandler(BaseHandler):
	def get(self):
		self.render("word_scrambler.html")
		return

class ServiceHandler(BaseHandler):
	@gen.coroutine
	def get(self):
		order = self.get_argument('order')
		package = yield pool.submit(jack.process, order)
		
		delivery = {
			"time_taken": package[0],
			"serving": package[1]}
		
		self.write(json.dumps(delivery))

class BlobHandler(BaseHandler):
	@tornado.web.asynchronous
	def get(self):
		print("starting")
		time.sleep(4)
		print("the love")

handlers = [
	(r"/", IndexHandler),
	(r"/serve", ServiceHandler),
	(r"/blob", BlobHandler),
]

settings = dict(
	debug = True,
	static_path = os.path.join(os.getcwd(), "assets"),
	template_path = os.path.join(os.getcwd(), "pages"),
)

app = tornado.web.Application(
	handlers,
	**settings
)

def start():
	tornado.options.parse_command_line()
	app_server = tornado.httpserver.HTTPServer(app)
	app_server.listen(tornado.options.options.port)
	
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	try:
		start()
	except KeyboardInterrupt:
		logging.warning("Error: Keyboard Interrupt")
		logging.critical("Shutting down")
