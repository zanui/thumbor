#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import signal
import optparse
import logging

from thumbor import __version__
from thumbor.utils import real_import

ip = "0.0.0.0"
port = 8888
conf = None
server = None

#def __kill_server():
    #print 'stopping server...'
    #server.stop()
    #ioloop = tornado.ioloop.IOLoop.instance()
    #ioloop.stop()
    #ioloop._stopped = False

#def handle_sigterm(signum, frame):
    #__kill_server()
    #print "server stopped"

#def handle_sighup(signum, frame):
    #__kill_server()

    #print 'restarting server...'
    #run_app(ip, port, conf)

def main():
    '''Runs thumbor server with the specified arguments.'''
    global server
    global ip
    global port
    global conf

    parser = optparse.OptionParser(usage="thumbor or type thumbor -h (--help) for help", description=__doc__, version=__version__)
    parser.add_option("-p", "--port", type="int", dest="port", default=8888, help = "The port to run this thumbor instance at [default: %default]." )
    parser.add_option("-i", "--ip", dest="ip", default="0.0.0.0", help = "The host address to run this thumbor instance at [default: %default]." )
    parser.add_option("-c", "--conf", dest="conf", default="", help = "The path of the configuration file to use for this thumbor instance [default: %default]." )
    parser.add_option("-l", "--log-level", dest="log_level", default="warning", help = "The log level to be used. Possible values are: debug, info, warning, error, critical or notset. [default: %default]." )
    parser.add_option("-a", "--app", dest="app", default='thumbor.handlers.eventlet.app', help = "A custom app to use for this thumbor server in case you subclassed ThumborServiceApp [default: %default]." )

    (options, args) = parser.parse_args()

    #if not signal.getsignal(signal.SIGHUP):
        #signal.signal(signal.SIGHUP, handle_sighup)
    #if not signal.getsignal(signal.SIGTERM):
        #signal.signal(signal.SIGTERM, handle_sigterm)

    port = options.port
    ip = options.ip
    conf = options.conf or None
    log_level = options.log_level

    run_app(ip, port, conf, log_level, options.app)

def run_app(ip, port, conf, log_level, app):
    global server

    logging.basicConfig(level=getattr(logging, log_level.upper()))

    #if app:
        #try:
            #application = __import_class(app)(conf)
        #except Exception, err:
            #raise RuntimeError('Could not import your custom application "%s" because of error: %s' % (app, str(err)))
    #else:
        #application = ThumborServiceApp(conf)

    #server = HTTPServer(application)
    #server.bind(port, ip)
    #server.start()

    #try:
        #tornado.ioloop.IOLoop.instance().start()
    #except KeyboardInterrupt:
        #print
        #print "-- thumbor closed by user interruption --"

    try:
        application = real_import(app)
    except Exception, err:
        raise RuntimeError('Could not import your custom application "%s" because of error: %s' % (app, str(err)))

    options = {
        'verbose': False,
        'host': ip,
        'port': port,
        'processes': 1,
        'threads': 30,
        'reload': False
    }

    application.run(options)

if __name__ == "__main__":
    main()
