# coding: utf-8

import datetime
import random
import string


class VotePool(object):
    _pool = {}

    @classmethod
    def _gen_unique_id(cls):
        id = ''.join([random.choice(string.digits) for i in range(4)])
        if id in cls._pool:
            return cls._gen_unique_id()
        return id

    @classmethod
    def create_vote(cls, threshold, callback, success_msg, timeout=300):
        id = cls._gen_unique_id()
        cls._pool[id] = Vote(id, threshold, callback, success_msg, timeout)
        return cls._pool[id]

    @classmethod
    def get_valid_vote(cls, id):
        if id not in cls._pool:
            return None

        vote = cls._pool[id]
        if not vote.is_valid():
            return None
        return vote

    @classmethod
    def has_valid_vote(cls, id):
        return bool(cls.get_valid_vote(id))

    @classmethod
    def incr_vote(cls, id, member):
        vote = cls.get_valid_vote(id)
        if not vote:
            return False

        return vote.incr(member)


class Vote(object):

    def __init__(self, id, threshold, callback, success_msg, timeout):
        self.id = id
        self.cnt = 0
        self.callback = callback
        self.members = set()
        self.timeout = 300
        self.threshold = threshold
        self.success_msg = success_msg
        self.created_at = datetime.datetime.now()

    def incr(self, member):
        if not self.is_valid():
            return False

        if member in self.members:
            return False

        self.members.add(member)
        self.cnt += 1
        if self.cnt >= self.threshold:
            self.callback()
        return True

    def is_valid(self):
        return True

    def is_success(self):
        return self.cnt >= self.threshold
