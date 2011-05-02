import re

from eventlet import wsgi
import eventlet

class Handler(object):
    def __init__(self):
        self.status_code = 200
        self.content_type = 'text/html'

    def get(self):
        return ''

    def process_request(self, environ, start_response):
        value = self.get()
        start_response(str(self.status_code), [('content-type', self.content_type)])

        return value

class HelloWorldHandler(Handler):
    def get(self):
        return "hello world"

class HelloMoreHandler(Handler):
    def get(self):
        return "Hello more"

URL = [
    [r'^/$', HelloWorldHandler],
    [r'^/more$', HelloMoreHandler]
]

def dispatch(environ, start_response):
    for url in URL:
        if url[0].match(environ['PATH_INFO']):
            return url[1]().process_request(environ, start_response)

    start_response('404', [('content-type', 'text/html')])
    return ''

listener = eventlet.listen(('0.0.0.0', 7000))
try:
    for url in URL:
        url[0] = re.compile(url[0])
    wsgi.server(listener, dispatch, log=None)
finally:
    listener.close()
