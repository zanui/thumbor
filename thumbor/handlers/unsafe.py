#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from os.path import splitext

import tornado.web
from tornado.options import options

from thumbor.handlers import ContextHandler

int_or_0 = lambda value: 0 if value is None else int(value)

class Context(dict):
    @classmethod
    def from_dict(cls, kw):
        opt = cls()

        opt['meta'] = kw['meta'] == 'meta'

        opt['crop'] = {
            'left': int_or_0(kw['crop_left']),
            'top': int_or_0(kw['crop_top']),
            'right': int_or_0(kw['crop_right']),
            'bottom': int_or_0(kw['crop_bottom'])
        }

        opt['crop']['enabled'] = opt['crop']['left'] > 0 or \
                                 opt['crop']['top'] > 0 or \
                                 opt['crop']['right'] > 0 or \
                                 opt['crop']['bottom'] > 0

        opt['fit_in'] = kw['fit_in'] == 'fit-in'

        opt['width'] = int_or_0(kw['width'])
        opt['height'] = int_or_0(kw['height'])

        if options.MAX_WIDTH and opt['width'] > options.MAX_WIDTH:
            opt['width'] = options.MAX_WIDTH
        if options.MAX_HEIGHT and opt['height'] > options.MAX_HEIGHT:
            opt['height'] = options.MAX_HEIGHT

        opt['horizontal_flip'] = kw['horizontal_flip'] == '-'
        opt['vertical_flip'] = kw['vertical_flip'] == '-'

        opt['halign'] = kw['halign'] or 'center'
        opt['valign'] = kw['valign'] or 'middle'

        opt['smart'] = kw['smart'] == 'smart'

        opt['imageUrl'] = kw['image']
        opt['extension'] = splitext(opt['imageUrl'])[-1].lower().lstrip('.')

        return opt

class ImagingHandler(ContextHandler):

    @tornado.web.asynchronous
    def get(self, **kw):
        context = Context.from_dict(kw)

        self.process_image(context)

    def process_image(self, context):
        def callback(buffer):
            self.set_header('Content-Type', 'image/%s' % context['extension'])

            self.engine.load(buffer, context['extension'])

            #self.engine.resize(context['width'], context['height'])

            #contents = self.engine.read()
            self.write(self.engine.read())
            #self.write(buffer)
            #self.write('ok')
            self.finish()

        self.fetch_image(context, callback)

    def fetch_image(self, context, callback):
        storage = self.storage()
        buffer = storage.get(context['imageUrl'])

        if buffer is not None:
            callback(buffer)
        else:
            def handle_loader_loaded(buffer):
                if buffer is None:
                    callback(None)
                    return

                #self.engine.load(buffer, context['extension'])
                #self.engine.normalize()
                #buffer = self.engine.read()

                storage.put(context['imageUrl'], buffer)
                storage.put_crypto(context['imageUrl'])

                callback(buffer)

            self.loader.load(context['imageUrl'], handle_loader_loaded)

class MainHandler(ContextHandler):

    @tornado.web.asynchronous
    def get(self,
            meta,
            crop_left,
            crop_top,
            crop_right,
            crop_bottom,
            fit_in,
            horizontal_flip,
            width,
            vertical_flip,
            height,
            halign,
            valign,
            smart,
            image,
            **kw):

        if not self.validate(image):
            self._error(404)
            return

        int_or_0 = lambda value: 0 if value is None else int(value)

        opt = {
            'meta': meta == 'meta',
            'crop': {
                'left': int_or_0(crop_left),
                'top': int_or_0(crop_top),
                'right': int_or_0(crop_right),
                'bottom': int_or_0(crop_bottom)
            },
            'fit_in': fit_in,
            'width': int_or_0(width),
            'height': int_or_0(height),
            'horizontal_flip': horizontal_flip == '-',
            'vertical_flip': vertical_flip == '-',
            'halign': halign or 'center',
            'valign': valign or 'middle',
            'smart': smart == 'smart'
        }

        return self.execute_image_operations(opt, image)

