# coding: utf-8

import re
from yabot.models.vote import VotePool
from yabot.models.member import Member


class VoteMonitor(object):

    def process_text(self, send_from, text):
        pass

    def process_command(self, send_from, text):
        match = re.match(ur'投票 (\d+)', text)
        if not match:
            return

        member = Member(send_from)
        vote_id = match.group(1)
        vote = VotePool.get_valid_vote(vote_id)
        if not vote:
            return u'没有这个投票啊，你瞎打的吧..'

        ret = vote.incr(member)
        if ret:
            l = [u'+1票\n']
        else:
            l = [u'并没有+1票\n']

        l.append(u'投票者:')
        for m in vote.members:
            l.append(m.nickname)

        if vote.is_success():
            l.append(u'票数达到啦!' + vote.success_msg)
        else:
            l.append(u'现在就剩%s票啦!' % (vote.threshold - vote.cnt))

        return '\n'.join(l)
