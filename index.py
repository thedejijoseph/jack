import tornado.web
import tornado.ioloop

import os
import json
import logging

import jack

logging.basicConfig(
	level = logging.DEBUG,
	format = '%(asctime)s | %(levelname)s | %(message)s'
)

class BaseHandler(tornado.web.RequestHandler):
	pass

class IndexHandler(BaseHandler):
	def get(self):
		logging.info("GET request received at /")
		self.render("word_scrambler.html")
		return

class ServiceHandler(BaseHandler):
	def get(self):
		logging.info("GET request received at /serve")
		order = self.get_query_argument('order')
		
		logging.info(f"processing order '{order}'")
		dishes = jack.process(order)
		
		logging.info("sending response")
		self.write(json.dumps(dishes))
	
	def post(self):
		logging.info("POST request received at /serve")
		return

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

logging.info("server is starting up")
app.listen(8085)
tornado.ioloop.IOLoop.current().start()