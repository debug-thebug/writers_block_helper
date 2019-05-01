from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
import json
from mongodb_connector import dbHandler
from validity_checker import ValidityChecker
from synonym_generator import SynonymGenerator
from wordcloud_gen import WordCloudGenerator
import logging

sentences = []
class InputApplication(Application):
    def __init__(self, handler_mapping):
        self.db = dbHandler()
        self.checker = ValidityChecker()
        self.sentencegenerator = SynonymGenerator()
        self.wcgenerator = WordCloudGenerator()
        super(InputApplication, self).__init__(handler_mapping)

class InputHandler(RequestHandler):
    def set_default_headers(self):
        super(InputHandler, self).set_default_headers()
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:7777')
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def get(self):
        self.render("frontend_form.html", message=None, corrections=None, sentences=None, wordcloud=False)

    def post(self):
        input_text = self.get_argument("text")

        # Generate corrections first
        corrections = self.application.checker.corrections(text=input_text)
        if self.application.checker.len_corrections(corrections) == 0:
            corrections = None

        # Generate synonymous sentences
        sentences = self.application.sentencegenerator.get_sentence(3, text=input_text)

        # Generate word cloud
        self.application.wcgenerator.generate_wc(text=input_text, fname="Dynamic_Word_Cloud")

        # Render page after generating required info
        self.render("frontend_form.html", message=input_text, corrections=corrections, sentences=sentences, wordcloud=True)

        # sentences.append(self.request.body)
        # give input in dict/json format
        # self.application.db.insertSentenceToDb(json.loads(self.request.body))

if __name__ == "__main__":
    logging_level = logging.getLevelName('INFO')
    logging.getLogger().setLevel(logging_level)
    logging.info('starting event logger on %s:%d', '127.0.0.1', 7777)
	
    handler_mapping = [
					   (r'/', InputHandler),
                       (r'/sentence', InputHandler),
                       (r'/sentence/', InputHandler),
                       (r"/static/(.*)", StaticFileHandler, {"path": "./"})
                      ]
    application = InputApplication(handler_mapping)
    application.listen(7777)
    IOLoop.current().start()