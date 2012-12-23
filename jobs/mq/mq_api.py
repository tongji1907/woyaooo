# -*- coding: utf-8 -*-

import pika
import sys

class WoyaoooMQAPI(object):
    def __init__(self):
        #self.host = "localhost"
        self.host = "42.121.31.175"
        self.exchange = "woyaoooMQExc"
        self.type = "topic"

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange = self.exchange, type = self.type)

    def sendWelcomeEmail(self, user_id):
        """
        发送欢迎信，新用户注册后触发
        user_id: 新注册用户ID号
        """
        self.channel.basic_publish(exchange = self.exchange, routing_key = "user.sendWelcome", body = str(user_id))
        print >> sys.stdout, "Message Sent: user.sendWelcome"

    def sendInviteEmail(self, email_list, conversation_id):
        """
                  发送邀请信，根据后台逻辑自动触发
        email_list: email 地址数组
        converation_id: 邀请信所关联的对话ID号
        """
        str_emails = str(email_list)
        lst = [str_emails, str(conversation_id)]
        self.channel.basic_publish(exchange = self.exchange, routing_key = "user.sendInvite", body = str(lst))
        print >> sys.stdout, "Message Sent: user.sendInvite"

    def sendTalkManageEmail(self, talk_id_list):
        """
        发送需求管理信，后台管理人员手动触发
        talk_id_list: Talk的ID数组
        """
        self.channel.basic_publish(exchange = self.exchange, routing_key = "talk.sendTalkManage", body = str(talk_id_list))
        print >> sys.stdout, "Message Sent: talk.sendTalkManage"

    def createTalk(self, talk):
        """
                  创建一个Talk，前台用户触发
        talk: dict格式的talk数据实体
        """
        self.channel.basic_publish(exchange = self.exchange, routing_key = "talk.create", body = str(talk))
        print >> sys.stdout, "Message Sent: talk.create"

    def createConversation(self, talk):
        """
        创建一个对话，即第一个Talk的创建。前台用户触发
        talk: dict格式的talk数据实体
        """
        self.channel.basic_publish(exchange = self.exchange, routing_key = "conversation.create", body = str(talk))
        print >> sys.stdout, "Message Sent: conversation.create"

    def talkIndexed(self, talk_id):
        pass
