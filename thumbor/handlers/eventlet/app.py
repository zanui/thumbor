#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import sys

import spawning.spawning_controller as controller
from eventlet.greenthread import spawn

from thumbor.handlers.eventlet.urls import URLS
from thumbor.config import conf
from thumbor.options import parse_config_file

def dispatcher(environ, start_response):
    def get_response(environ, start_response):
        for url in URLS:
            match = url[0].match(environ['PATH_INFO'])
            if match:
                return url[1]().process_request(environ, start_response, **match.groupdict())

        start_response('404', [('content-type', 'text/html')])
        return ''
    func = spawn(get_response, environ, start_response)
    result = func.wait()
    return result

def run(conf_path):
    parse_config_file(conf_path)
    factory = 'spawning.wsgi_factory.config_factory'

    factory_args = {
        'verbose': conf.VERBOSE,
        'host': conf.HOST,
        'port': conf.PORT,
        'num_processes': conf.PROCESSES,
        'threadpool_workers': conf.THREADS,
        'watch': None,
        'reload': conf.AUTO_RELOAD,
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
        'status_host': conf.HOST
    }

    controller.start_controller(None, factory, factory_args)
