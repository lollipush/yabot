# coding: utf-8

import os
import cPickle


class StorgeMixin(object):

    @classmethod
    def dump(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        with open(path, 'wb') as f:
            cPickle.dump(self, f)

    @classmethod
    def load(self, path):
        try:
            with open(path, 'rb') as f:
                return cPickle.load(f)
        except IOError:
            return None
