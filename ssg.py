from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
import json

sentences = []
class InputHandler(RequestHandler):
    def set_default_headers(self):
        super(InputHandler, self).set_default_headers()
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def post(self):
        sentences.append(self.request.body)
        self.write({'sentence': json.loads(self.request.body)})

if __name__ == "__main__":
    handler_mapping = [
                       (r'/sentence', InputHandler),
                       (r'/sentence/', InputHandler),
                      ]
    application = Application(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()