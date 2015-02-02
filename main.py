__author__ = 'mario'

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, StaticFileHandler
from searchHandler import searchHandler

class RootHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return Application([
        url(r"/", RootHandler)
        ])


if __name__ == "__main__":

    app = make_app()
    app.settings.setdefault("template_path", "templates")

    handlers = [(r'/static/(.*)', StaticFileHandler, {'path': "./static"}),
                (r"/search.*", searchHandler)]


    app.add_handlers("localhost", handlers)
    app.listen(8889)
    IOLoop.current().start()
