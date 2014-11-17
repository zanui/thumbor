#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import os
import shutil

from thumbor.optimizers import BaseOptimizer

class Optimizer(BaseOptimizer):

    def should_run(self, image_extension, buffer):
        return 'jpg' in image_extension or 'jpeg' in image_extension

    def optimize(self, buffer, input_file, output_file):
        jpegoptim_path = self.context.config.JPEGOPTIM_PATH
        shutil.copy2(input_file, output_file)
        command = '%s --strip-all %s' % (
            jpegoptim_path,
            output_file
        )
        os.system(command)
