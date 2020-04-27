from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


class WebApplication:
    def __init__(self):
        self.app = Flask(__name__)
        self.appmiddleware = DispatcherMiddleware(self.app, {
            '/metrics': make_wsgi_app()
        })
