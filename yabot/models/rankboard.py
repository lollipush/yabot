# coding: utf-8

import datetime

from yabot.models.storge import StorgeMixin
from yabot.models.member import Member


class RankItem(object):
    def __init__(self, member, score):
        self.member = member
        self.score = score

    def __hash__(self):
        return hash(self.member)

    def add_score(self, score_delta):
        self.score += score_delta

    def set_score(self, score):
        self.score = score


class RankBoard(StorgeMixin):

    def __init__(self, path, create_time=None):
        self.members = []
        self.file_path = path
        self.rank_items = {}
        self.create_time = create_time or datetime.datetime.now()

    def add_score(self, nickname, score):
        member = Member(nickname)
        if member not in self.members:
            self.members.append(member)
            self.rank_items[member] = RankItem(member, score)
        else:
            self.rank_items[member].add_score(score)

    def show_rank(self):
        l = [(member, item.score) for member, item in self.rank_items.items()]
        return sorted(l, key=lambda x: x[1], reverse=True)
