#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from eventlet.greenthread import spawn

class Handler(object):
    def __init__(self):
        self.status_code = 200
        self.content_type = 'text/html'

    def get(self):
        return ''

    def process_request(self, environ, start_response, *args, **kw):
        func = spawn(self.get, *args, **kw)
        result = func.wait()

        start_response(str(self.status_code), [('content-type', self.content_type)])
        return result


