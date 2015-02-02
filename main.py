__author__ = 'mario'

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
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


    app.add_handlers("localhost", [(r"/search.*", searchHandler)])
    app.listen(8888)
    IOLoop.current().start()
