from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from voyage.application import application

http_server = WSGIServer(('', 9999), application, handler_class=WebSocketHandler)
http_server.serve_forever()
