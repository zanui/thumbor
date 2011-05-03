#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import sys
import os

from eventlet.greenthread import spawn
from spawning.spawning_controller import start_controller

from thumbor.handlers.eventlet.urls import URLS

def dispatcher(environ, start_response):
    def perform_dispatch(environ, start_response):
        for url in URLS:
            if url[0].match(environ['PATH_INFO']):
                return url[1]().process_request(environ, start_response)

        start_response('404', [('content-type', 'text/html')])
        return ''

    func = spawn(perform_dispatch, environ, start_response)

    result = func.wait()

    return result

def run(options):
    sock = None

    os.setpgrp()

    factory = 'spawning.wsgi_factory.config_factory'

    factory_args = {
        'verbose': options['verbose'],
        'host': options['host'],
        'port': options['port'],
        'num_processes': options['processes'],
        'threadpool_workers': options['threads'],
        'watch': None,
        'reload': options['reload'],
        'deadman_timeout': 10,
        'access_log_file': None,
        'pidfile': None,
        'coverage': False,
        'sysinfo': False,
        'no_keepalive' : False,
        'max_age' : None,
        'argv_str': " ".join(sys.argv[1:]),
        'args': ['thumbor.handlers.eventlet.app.dispatcher'],
        'status_port': None,
        'status_host': options['host']
    }

    start_controller(sock, factory, factory_args)
