# coding: utf-8


class Member(object):
    def __init__(self, nickname):
        self.nickname = nickname

    def __hash__(self):
        return hash(self.nickname)

    def __eq__(self, other):
        if not isinstance(other, Member):
            return False
        return self.nickname == other.nickname
