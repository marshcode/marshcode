from davesite.app import factory
app = factory.create_app(__name__)

class URLPrefixMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = app.config.get('SCRIPT_NAME', '/')
        return self.app(environ, start_response)

app.wsgi_app = URLPrefixMiddleware(app.wsgi_app)