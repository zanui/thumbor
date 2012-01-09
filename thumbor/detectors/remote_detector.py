#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado import httpclient
from tornado.options import options
from pyremotecv import PyRemoteCV

from thumbor.detectors import BaseDetector

import bson

class RemoteDetector(BaseDetector):
    http_client = None

    @classmethod
    def get_async_http_client(cls):
        if cls.http_client is None:
            cls.http_client = httpclient.AsyncHTTPClient()
        return cls.http_client

    def detect(self, context, callback):
        def on_result(response):
            result = []
            if response.error:
                callback(result)
            features = bson.loads(response.body)['points']

            for point in features:
                result.append(self.format_point(point))

            callback(result)

        client = self.get_async_http_client()

        engine = context['engine']        
        msg = { 
            'type': self.detection_type,
            'size': engine.size,
            'mode': engine.get_image_mode(),
            'image': engine.get_image_data()
        }

        req = httpclient.HTTPRequest("http://%s:%s/handle_image" % (options.REMOTECV_HOST, options.REMOTECV_PORT),
            request_timeout=options.REMOTECV_TIMEOUT,
            body=bson.dumps(msg),
            method='POST')
        
        client.fetch(req, on_result)

    # def detect(self, context, callback):
    #     engine = context['engine']
    #     host = 'tcp://%s:%s' % (options.REMOTECV_HOST, options.REMOTECV_PORT)
    #     image = engine.get_image_data()

    #     def on_result(points):
    #         result = []
    #         if not points: callback(result)

    #         for point in points:
    #             result.append(self.format_point(point))

    #         callback(result)

    #     PyRemoteCV.async_detect(
    #         action=self.detection_type,
    #         server=host,
    #         image_size=engine.size,
    #         image_bytes=image,
    #         image_mode=engine.get_image_mode(),
    #         callback=on_result,
    #         timeout=options.REMOTECV_TIMEOUT
    #     )

