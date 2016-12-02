# coding: utf-8
#
# ya - > 雅

import re
import jieba

from functools import partial
from yabot.models.rankboard import RankBoard
from yabot.models.storge import StorgeMixin
from yabot.models.vote import VotePool


class YalessWordSet(StorgeMixin):
    def __init__(self, path):
        self.word_set = set()
        self.file_path = path

    def is_yaless_word(self, word):
        return word.strip() in self.word_set

    def add_yaless_word(self, word):
        self.word_set.add(word.strip())
        jieba.add_word(word.strip())

    def remove_yaless_word(self, word):
        try:
            self.word_set.remove(word.strip())
            jieba.del_word(word.strip())
        except KeyError:
            pass

    def words(self):
        return list(self.word_set)


class YaMonitor(object):

    def __init__(self, name):
        self.name = name
        rankboard_path = './%s/yaless_rankboard' % self.name
        yaless_word_set_path = './%s/yaless_dict' % self.name

        self.rankboard = RankBoard.load(rankboard_path) or RankBoard(rankboard_path)
        self.yaless_word_set = YalessWordSet.load(yaless_word_set_path) or YalessWordSet(yaless_word_set_path)
        self.yaless_word_set.add_yaless_word(u'三蛋')
        self.yaless_word_set.add_yaless_word(u'吃翔')

    def process_text(self, send_from, text):
        yaless_word = []

        tks = set(jieba.cut(text))
        yaless_word = tks & set(self.yaless_word_set.words())
        self.rankboard.add_score(send_from, len(yaless_word))
        if not yaless_word:
            return

        return u'低俗!!! \n%s 说了低俗词语"%s"' % (send_from, u'、'.join(yaless_word))

    def process_command(self, send_from, text):
        return self._process_command_add_yaless_word(send_from, text) or \
            self._process_command_remove_yaless_word(send_from, text) or \
            self._process_command_show_rankboard(send_from, text) or \
            self._process_command_show_yaless_word(send_from, text) or \
            self._process_command_help(send_from, text)

    def _process_command_add_yaless_word(self, send_from, text):
        match = re.match(ur'个新低俗词 (.+)', text)
        if not match:
            return

        word = match.group(1)
        if self.yaless_word_set.is_yaless_word(word):
            return u'你傻啊，已经有这个低俗词了啊'

        vote = VotePool.create_vote(3, partial(self._add_yaless_word_callback, word), u'已新增不雅词“%s”' % word, 300)
        return u'下面开始为新增低俗词“%s”投票\n同意的人请回复: \n整 投票 %s' % (word, vote.id)

    def _process_command_remove_yaless_word(self, send_from, text):
        match = re.match(ur'删低俗词 (.+)', text)
        if not match:
            return

        word = match.group(1)
        if not self.yaless_word_set.is_yaless_word(word):
            return u'你傻啊，没有这个低俗词啊'

        vote = VotePool.create_vote(3, partial(self._remove_yaless_word_callback, word), u'已删不雅词“%s”' % word, 300)
        return u'下面开始为删除低俗词“%s”投票\n同意的人请回复: \n整 投票 %s' % (word, vote.id)

    def _add_yaless_word_callback(self, word):
        self.yaless_word_set.add_yaless_word(word)

    def _remove_yaless_word_callback(self, word):
        self.yaless_word_set.remove_yaless_word(word)

    def _process_command_show_rankboard(self, send_from, text):
        if text != u'看低俗榜':
            return

        l = [u'低俗榜']
        for index, (member, score) in enumerate(self.rankboard.show_rank()):
            l.append(u'第%s名: %s %s次' % (index+1, member.nickname, score))
        return u'\n'.join(l)

    def _process_command_show_yaless_word(self, send_from, text):
        if text != u'看低俗词':
            return
        l = [u'低俗词']
        for word in self.yaless_word_set.words():
            l.append(word)
        return u'\n'.join(l)

    def _process_command_help(self, send_from, text):
        if text != u'帮助':
            return
        l = [u'教你咋整', u'整 个新低俗词 xxx', u'整 看低俗榜', u'整 看低俗词', u'整 删低俗词 xxx']
        return u'\n'.join(l)
