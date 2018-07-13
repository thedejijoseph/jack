import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.websocket
from tornado import gen

import os
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor()

import jack

# configure logging module
log_format = "%(levelname)s: %(asctime)s | %(message)s"
logging.basicConfig(filename="./app/app.log", level=logging.INFO, format=log_format)
logger = logging.getLogger()


from tornado.options import define
define("port", default=3303, type=int)


class BaseHandler(tornado.web.RequestHandler):
	pass

class IndexHandler(BaseHandler):
	@gen.coroutine
	def get(self):
		self.render("index.html", port_no=tornado.options.options.port)
		# do you see where the fix ended up going..
		return

class ServiceHandler(BaseHandler):
	@gen.coroutine
	def get(self):
		order = self.get_argument('order')
		# delivery = yield pool.submit(jack.process, order)
		
		# adding logging (debug purposes)
		logger.info(f"processing order: {order}")
		
		delivery = yield pool.submit(jack.real_time, order)
		for batch in delivery:
			self.write(json.dumps({"serving": batch}))

class RealTimeServiceHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		# log connecting client
		logger.info("socket client-server connection established")
		pass
	
	def on_message(self, message):
		order_packet = json.loads(message)
		order = order_packet.get("order")
		if not order:
			delivery_packet = {"error": True, "msg": "invalid order"}
			self.write_message(delivery_packet)
		
		logger.info(f"processing order: {order}")
		order = order.lower()
		prime = jack.real_time(order)
		
		for pack in prime:
			self.write_message(json.dumps(pack))
		
		self.close()
	
	def on_close(self):
		pass

class HandshakeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
	    logger.info("opening handshake socket")
	    return

    def on_message(self, message):
        logger.info("receiving handshake")
        self.write_message("hi")
        self.close()
        return

    def on_close(self):
	    logger.info("handshake complete")
	    return

class DashboardHandler(BaseHandler):
	def get(self):
		self.render("dashboard.html")

class AboutPage(BaseHandler):
	def get(self):
		self.render("about.html")


handlers = [
	(r"/", IndexHandler),
	(r"/serve-old", ServiceHandler),
	(r"/serve", RealTimeServiceHandler),
	(r"/handshake", HandshakeHandler),
	(r"/dashboard", DashboardHandler),
	(r"/about", AboutPage),
]

settings = dict(
	debug = True,
	static_path = os.path.join(os.path.dirname(__file__), "assets"),
	template_path = os.path.join(os.path.dirname(__file__), "pages"),
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
		print("KeyboardInterrupt: destroying server")
