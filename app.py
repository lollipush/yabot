# coding: utf-8

from yabot.wechat_bot import WechatBot


bot = WechatBot.init()
bot.monitor_chatroom('7008087266@chatroom')

bot.run()
