#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from datetime import datetime, timedelta

from thumbor.storages import BaseStorage
from thumbor.config import conf

class Storage(BaseStorage):

    def __init__(self):
        self.items = {}
        self.crypto = {}
        self.expires = {}

    def __key_for(self, url):
        return 'crypto-%s' % url

    def put(self, path, bytes):
        self.items[path] = bytes
        self.expires[path] = datetime.now() + timedelta(seconds=conf.STORAGE_EXPIRATION_SECONDS)

    def put_crypto(self, path):
        if not conf.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return

        if not conf.SECURITY_KEY:
            raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

        self.crypto[self.__key_for(path)] = conf.SECURITY_KEY

    def get_crypto(self, path):
        if not conf.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return None

        crypto = self.crypto.get(self.__key_for(path), None)

        if not crypto:
            return None
        return crypto

    def get(self, path):
        item = self.items.get(path, None)
        return item

