# coding:utf-8
'''
Created on 2012-12-3

@author: JD
'''
import sys
import mq_api
import receiver_base



class MQReceiver_Conversation(receiver_base.MQReceiverBase):
    def __init__(self):
        routing_key_list = []
        routing_key_list.append("conversation.create")#创建对话
        routing_key_list.append("crawlfinish")           #添加对话
        #routing_key_list.append("conversation.sendRequireManage") #请求需求管理
        #routing_key_list.append("talk.indexed")       #对话已被收录
        receiver_base.MQReceiverBase.__init__(self, routing_key_list)
        
    def callBack(self, ch, method, properties, body):
        try:
            routing_key = method.routing_key
            if routing_key == 'conversation.create':
                self.__createConversation(body)

            elif routing_key == "crawlfinish":
                self.__crawlFinished(body)
            '''
            elif routing_key == "conversation.sendRequireManage":
                self.__sendRequirementTakeEmail(body)
            elif routing_key == "talk.indexed":
                self.__sendTalkIndexed(body)
            '''
        except Exception, e:
            print >> sys.stdout, 'Error @MQReceiver_Conversateion.Create: %r' % e
   
#========================================具体实现 ========================================    
    #新建对话

    def __createConversation(self, str_talk):
        """前台发送过来新建对话的实现
                    参数格式：talk的dict进行str化
        """
        dict_talk = eval(str_talk)         
        #id = dict_talk['id']
        conversation_id = dict_talk['conversationId']
        #creator = int(dict_talk['creator'])
        #created = dict_talk['created']
        description = dict_talk['description']

        print "talk created>>>>"+description
        #emails = invitejob.do_invite(description)

        #mq_api.WoyaoooMQAPI().sendInviteEmail(list(emails),conversation_id)


    def __crawlFinished(self,str_talk):
        print "crawl finished>>>>>"
        docindexjob.do_index()
        dict_talk = eval(str_talk)
        conversation_id = dict_talk['conversationId']
        description = dict_talk['description']
        print description
        emails = invitejob.do_invite(description)
        mq_api.WoyaoooMQAPI().sendInviteEmail(list(emails),conversation_id)

    
if __name__ == "__main__":
    MQReceiver_Conversation().startListen()