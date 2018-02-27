from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from werkzeug.debug import DebuggedApplication
from werkzeug.serving import run_with_reloader

from voyage.application import application


@run_with_reloader
def run_server():
    http_server = WSGIServer(('', 9999), DebuggedApplication(application), handler_class=WebSocketHandler)
    http_server.serve_forever()


if __name__ == "__main__":
    run_server()
