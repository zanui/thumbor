#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import os

from thumbor.optimizers import BaseOptimizer

class Optimizer(BaseOptimizer):

    def should_run(self, image_extension, buffer):
        return 'jpg' in image_extension or 'jpeg' in image_extension

    def optimize(self, buffer, input_file, output_file):
        jpegtran_path = self.context.config.JPEGTRAN_PATH
        command = '%s -copy none -optimize -progressive -outfile %s %s ' % (
            jpegtran_path,
            output_file,
            input_file,
        )
        os.system(command)
