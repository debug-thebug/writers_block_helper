import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options
import hashlib
import pickle

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler)
        ]
        tornado.web.Application.__init__(self, handlers)
        
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Welcome!")
		self.render("frontend_form.html")

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        input_text = self.get_argument("text")
        self.write("Your text: " + input_text)
        self.render("frontend_form.html")
    get = post
        
def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
