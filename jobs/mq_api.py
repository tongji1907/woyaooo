# -*- coding: utf-8 -*-

import pika
import sys

MQKey_TaskStatus = "task.status"

MQKey_TalkCreate = "talk.create"
MQKey_TalkUpdate = "talk.update"
MQKey_TalkDelete = "talk.delete"
MQKey_ConversationCreate = "conversation.create"
MQKey_ConversationAudit = "conversation.audit"
MQKey_EmailSendWelcome = "email.sendWelcome"
MQKey_EmailSendTakeRequire = "email.sendTakeRequire"
MQKey_EmailSend = "user.sendInvite"
MQKey_UserReg = "user.registry"

class WoyaoooMQAPI(object):
    def __init__(self):
        self.exchange = "woyaoooMQExc"
        self.type = "topic"
        self.supported_bindingKeys = [MQKey_TaskStatus,
                                      MQKey_TalkCreate,
                                      MQKey_TalkUpdate,
                                      MQKey_TalkDelete,
                                      MQKey_ConversationCreate,
                                      MQKey_ConversationAudit,
                                      MQKey_EmailSendWelcome,
                                      MQKey_EmailSendTakeRequire,
                                      MQKey_EmailSend,   
                                      MQKey_UserReg                                   
                                      ]
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = "42.121.31.175"))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange = self.exchange, type = self.type)
        
    def SendMessage(self, actionType, actionData):
        try:
            if not actionType in self.supported_bindingKeys:
                raise Exception("Unsupported Action: %r!" % actionType)
            
            self.channel.basic_publish(exchange = self.exchange, routing_key = actionType, body = str(actionData))
            print >> sys.stdout, "Message Sent: %r" % actionType
            return True
        except Exception, e:
            print >> sys.stdout, "Error: %r" % e
            return False
        
    #def __del__(self):
    #    self.connection.close()