#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from thumbor.handlers.eventlet.base import Handler
from thumbor.cli import Cli

class HealthCheckHandler(Handler):

    def get(self):
        cli = Cli()
        return cli.health_check()

class UnsafeHandler(Handler):

    def get(self, *args, **kw):
        cli = Cli()

        int_or_0 = lambda value: 0 if value is None else int(value)

        opt = {
            'meta': kw['meta'] == 'meta',
            'crop': {
                'left': int_or_0(kw['crop_left']),
                'top': int_or_0(kw['crop_top']),
                'right': int_or_0(kw['crop_right']),
                'bottom': int_or_0(kw['crop_bottom'])
            },
            'fit_in': kw['fit_in'],
            'width': int_or_0(kw['width']),
            'height': int_or_0(kw['height']),
            'horizontal_flip': kw['horizontal_flip'] == '-',
            'vertical_flip': kw['vertical_flip'] == '-',
            'halign': kw['halign'] or 'center',
            'valign': kw['valign'] or 'middle',
            'smart': kw['smart'] == 'smart',
            'image': kw['image']
        }

        content_type, result = cli.unsafe(opt)

        self.content_type = content_type

        return result
