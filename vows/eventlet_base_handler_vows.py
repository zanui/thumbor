#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from pyvows import Vows, expect

from thumbor.handlers.eventlet.base import Handler

@Vows.batch
class BaseHandlerVows(Vows.Context):
    def topic(self):
        return Handler()

    class WhenProcessingRequest(Vows.Context):
        def topic(self, handler):
            def start_response(status_code, arguments):
                pass

            return handler.process_request({}, start_response)

        def should_be_empty(self, topic):
            expect(topic).to_be_empty()
