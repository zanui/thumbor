#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

import re

from thumbor.url import Url
from thumbor.handlers.eventlet.handlers import HealthCheckHandler, UnsafeHandler

URLS = (
    [r'/healthcheck', HealthCheckHandler],
    [Url.regex(with_unsafe=True, include_image=True), UnsafeHandler]
)

for url in URLS:
    url[0] = re.compile(url[0])

