import re

from eventlet.greenthread import spawn

class Handler(object):
    def __init__(self):
        self.status_code = 200
        self.content_type = 'text/html'

    def get(self):
        return ''

    def process_request(self, environ, start_response):
        func = spawn(self.get)
        result = func.wait()

        start_response(str(self.status_code), [('content-type', self.content_type)])
        return result

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

for url in URL:
    url[0] = re.compile(url[0])
 
def dispatch(environ, start_response):
    def perform_dispatch(environ, start_response):
        for url in URL:
            if url[0].match(environ['PATH_INFO']):
                return url[1]().process_request(environ, start_response)

        start_response('404', [('content-type', 'text/html')])
        return ''

    func = spawn(perform_dispatch, environ, start_response)

    result = func.wait()

    return result
