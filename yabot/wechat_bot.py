# coding: utf-8

import itchat

from itchat.content import TEXT
from yabot.monitors.ya import YaMonitor
from yabot.monitors.vote import VoteMonitor


class WechatBot(object):

    def __init__(self):
        self.chatroom_uin_monitors = {}
        self.member_uin_monitors = {}

    @classmethod
    def init(cls):
        itchat.auto_login(hotReload=True, enableCmdQR=True)
        return cls()

    def monitor_chatroom(self, chatroom_uin):
        self.chatroom_uin_monitors[chatroom_uin] = [
            YaMonitor(chatroom_uin),
            VoteMonitor(),
        ]

    def monitor_member(self, member_id):
        pass

    def reply_chatroom_msg(self, msg):
        chatroom_username = msg['FromUserName']
        chatroom_d = itchat.search_chatrooms(userName=chatroom_username)

        if not chatroom_d:
            return

        text = msg['Text'].strip()
        from_nickname = msg['ActualNickName']
        is_command = text.startswith(u'整 ')

        chatroom_uin = chatroom_d['Uin']

        if chatroom_uin not in self.chatroom_uin_monitors:
            return

        if is_command:
            text = text[2:]

        for monitor in self.chatroom_uin_monitors[chatroom_uin]:
            if is_command:
                ret = monitor.process_command(from_nickname, text)
            else:
                ret = monitor.process_text(from_nickname, text)
            if ret:
                itchat.send_msg(ret, chatroom_username)

    def reply_member_msg(self, msg):
        pass

    def run(self):
        itchat.msg_register([TEXT], isGroupChat=True)(self.reply_chatroom_msg)
        itchat.msg_register([TEXT])(self.reply_member_msg)
        itchat.run()
