#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from os.path import splitext
import tempfile

from thumbor.transformer import Transformer
from thumbor.engines.json_engine import JSONEngine
from thumbor.utils import logger, real_import
from thumbor.config import conf

CONTENT_TYPE = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.png': 'image/png'
}

class Cli(object):
    def health_check(self):
        return 'working'

    def unsafe(self, options):
        loader = real_import(conf.LOADER)
        storage = real_import(conf.STORAGE).Storage
        engine = real_import(conf.ENGINE).Engine

        options['loader'] = loader
        options['storage'] = storage()
        options['engine'] = engine()

        if not self.validate(options):
            self._error(404)
            return

        return self.execute_image_operations(options)

    def _error(self, status, msg=None):
        self.set_status(status)
        if msg is not None:
            logger.error(msg)
        self.finish()

    def execute_image_operations(self, opt):

        should_crop = opt['crop']['left'] > 0 or \
                      opt['crop']['top'] > 0 or \
                      opt['crop']['right'] > 0 or \
                      opt['crop']['bottom'] > 0

        crop_left = crop_top = crop_right = crop_bottom = None
        if should_crop:
            crop_left = opt['crop']['left']
            crop_top = opt['crop']['top']
            crop_right = opt['crop']['right']
            crop_bottom = opt['crop']['bottom']

        width = opt['width']
        height = opt['height']

        if conf.MAX_WIDTH and width > conf.MAX_WIDTH:
            width = conf.MAX_WIDTH
        if conf.MAX_HEIGHT and height > conf.MAX_HEIGHT:
            height = conf.MAX_HEIGHT

        halign = opt['halign']
        valign = opt['valign']

        extension = splitext(opt['image'])[-1].lower()

        return self.get_image(opt, opt['meta'], should_crop, crop_left,
                       crop_top, crop_right, crop_bottom,
                       opt['fit_in'],
                       opt['horizontal_flip'], width, opt['vertical_flip'],
                       height, halign, valign, extension,
                       opt['smart'], opt['image'])

    def get_image(self,
                  options,
                  meta,
                  should_crop,
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
                  extension,
                  should_be_smart,
                  image
                  ):

        buffer = self._fetch(options, image, extension)

        if buffer is None:
            self._error(404)
            return

        context = dict(
            loader=options['loader'],
            engine=options['engine'],
            storage=options['storage'],
            buffer=buffer,
            should_crop=should_crop,
            crop_left=crop_left,
            crop_top=crop_top,
            crop_right=crop_right,
            crop_bottom=crop_bottom,
            fit_in=fit_in,
            should_flip_horizontal=horizontal_flip,
            width=width,
            should_flip_vertical=vertical_flip,
            height=height,
            halign=halign,
            valign=valign,
            extension=extension,
            focal_points=[]
        )

        context['engine'].load(buffer, extension)

        if meta:
            context['engine'] = JSONEngine(self.engine, image)

        if 'detectors' in options and should_be_smart:
            #work this out to be async
            #with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_file:
                #jpg_buffer = buffer if extension in ('.jpg', '.jpeg') else self.engine.read('.jpg')
                #temp_file.write(jpg_buffer)
                #temp_file.seek(0)
                #context['file'] = temp_file.name

                #self.detectors[0](index=0, detectors=self.detectors).detect(context)
            pass

        Transformer(context).transform()

        content_type = "application/json" if meta else CONTENT_TYPE[context['extension']]

        results = context['engine'].read(context['extension'])

        return (content_type, results)

    def validate(self, options):
        if not hasattr(options['loader'], 'validate'):
            return True

        is_valid = options['loader'].validate(options['image'])

        if not is_valid:
            logger.error('Request denied because the specified path "%s" was not identified by the loader as a valid path' % path)

        return is_valid

    def _fetch(self, options, url, extension):
        buffer = options['storage'].get(url)

        if buffer is not None:
            return buffer
        else:
            buffer = options['loader'].load(url)
            options['engine'].load(buffer, extension)
            options['engine'].normalize()
            buffer = options['engine'].read()
            options['storage'].put(url, buffer)

            return buffer

