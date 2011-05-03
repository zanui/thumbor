#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from thumbor.config import conf

class BaseEngine(object):

    def __init__(self):
        self.image = None
        self.extension = None

    def load(self, buffer, extension):
        #loads image buffer in byte format.
        self.extension = extension
        self.image = self.create_image(buffer)

    @property
    def size(self):
        return self.image.size

    def normalize(self):
        width, height = self.size
        if width > conf.MAX_WIDTH or height > conf.MAX_HEIGHT:
            width_diff = width - conf.MAX_WIDTH
            height_diff = height - conf.MAX_HEIGHT
            if conf.MAX_WIDTH and width_diff > height_diff:
                height = self.get_proportional_height(conf.MAX_WIDTH)
                self.resize(conf.MAX_WIDTH, height)
            elif conf.MAX_HEIGHT and height_diff > width_diff:
                width = self.get_proportional_width(conf.MAX_HEIGHT)
                self.resize(width, conf.MAX_HEIGHT)

    def get_proportional_width(self, new_height):
        width, height = self.size
        return round(float(new_height) * width / height, 0)

    def get_proportional_height(self, new_width):
        width, height = self.size
        return round(float(new_width) * height / width, 0)

    def create_image(self):
        raise NotImplementedError()

    def crop(self):
        raise NotImplementedError()

    def resize(self):
        raise NotImplementedError()

    def flip_horizontally(self):
        raise NotImplementedError()
    
    def flip_vertically(self):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()
