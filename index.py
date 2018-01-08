import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado import gen

import os
import json
import logging

import jack

logging.basicConfig(
	level = logging.DEBUG,
	format = '%(asctime)s | %(levelname)s | %(message)s'
)

logging.disable(logging.DEBUG)

from tornado.options import define
define("port", default=5000, help="open at given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
	pass

class IndexHandler(BaseHandler):
	def get(self):
		self.render("word_scrambler.html")
		return

class ServiceHandler(BaseHandler):
	@gen.coroutine
	def get(self):
		# GET request received at /serve
		order = self.get_query_argument('order')
		logging.debug(f"receiving order for {order}")
		
		# processing order
		delivery = jack.process(order, chain="web")
		
		# serving response
		logging.debug(f"sending order for {order}")
		self.write(json.dumps(delivery))

handlers = [
	(r"/", IndexHandler),
	(r"/serve", ServiceHandler),
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