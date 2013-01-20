# -*- coding: utf-8 -*-
from lucene import *
from lucene import SimpleFSDirectory, System, File,\
    Document, Field, StandardAnalyzer,ChineseAnalyzer,CJKAnalyzer, IndexWriter, Version,\
    IndexSearcher, QueryParser, MultiFieldQueryParser, IndexReader, Term, DateTools
from mq import mqreceiver_conversation

#from algorithm import bayes
import re,sys
from mq import receiver_base,mq_api
import docindexjob


class MQReceiver_Conversation(receiver_base.MQReceiverBase):
    def __init__(self):
        routing_key_list = []
        routing_key_list.append("conversation.create")#创建对话
        routing_key_list.append("crawlfinish")           #添加对话
        receiver_base.MQReceiverBase.__init__(self, routing_key_list)

    def callBack(self, ch, method, properties, body):
        try:
            routing_key = method.routing_key
            if routing_key == 'conversation.create':
                self.__createConversation(body)

            elif routing_key == "crawlfinish":
                self.__crawlFinished(body)

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
        emails = do_invite(description)
        mq_api.WoyaoooMQAPI().sendInviteEmail(list(emails),conversation_id)

def do_invite(keywords):
    print "invite started!>>>>>>"
    initVM()
    indexDir  = "/tmp/luceneindex/doc"
    version   = Version.LUCENE_CURRENT
    idxDir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(version)
    searcher = IndexSearcher(idxDir)
    query = QueryParser(version, "description", analyzer).parse(keywords)
    hits = searcher.search(query, 1000)
    indentCandidates = []

    #print len(hits.scoreDocs)
    for hit in hits.scoreDocs:
        print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        #print doc.get("description")

        intents = doc.get("intent")
        #print doc.get("url")
        if intents == None:
            continue
        intents = eval(intents)

        for intent in intents:
            indentCandidates.append(intent)

    searcher.close()
    inviteEmails = []
    #patterns = ["[^A-Za-z0-9_-]*(?P<buzz>([A-Za-z0-9_-]+(\.\w+)*@(\w+\.)+\w{2,3}))", '''qq[^\d]*(?P<buzz>[1-9][0-9]{4,})''']
    for indentCandidate in indentCandidates:
        #print repr(indentCandidate[0])

        emailCandidate = indentCandidate[0]
        if emailCandidate.find("@") == -1:
            qqMail = emailCandidate+"@qq.com"
            inviteEmails.append(qqMail)
        else:
            inviteEmails.append(emailCandidate)
        # remove useless intent
        #indentCandidate = indentCandidate.strip()

        #probability = bayes.checkneedprobability((indentCandidate).decode("ascii","ignore").encode("utf8"))
        #print probability
        #if (probability>0.5):
        #    continue
        #emailPattern = patterns[0]
        #qqPattern = patterns[1]
        #qqMatches =re.finditer(qqPattern,indentCandidate, re.IGNORECASE| re.DOTALL)
        #emailMatches = re.finditer(emailPattern,indentCandidate, re.IGNORECASE| re.DOTALL)

        #for qqMatch in qqMatches:
        #    qq = qqMatch.group("buzz").strip()
        #print qq
        #    qqMail = qq+"@qq.com"
        #    inviteEmails.append(qqMail)

        #for emailMatch in emailMatches:
        #    email = emailMatch.group("buzz").strip()
            #print email

        #    inviteEmails.append(email)


    #add haiming and rex mail

    #remove multipule emails

    toInviteEmails = set(inviteEmails)
    toInviteEmails.add("csonnet@hotmail.com")
    toInviteEmails.add("haiming.chen@gmail.com")
    toInviteEmails.add("wangxue9871@163.com")
    print "invite total" +str(len(toInviteEmails))+" emails >>>>>>>>>>>"
    #for mail_address in toInviteEmails:
       # print mail_address
    return toInviteEmails


if __name__=="__main__":
    MQReceiver_Conversation().startListen()
    #do_invite("我想买一辆车，10万以内的，请报价或建议。谢谢")
    #WoyaoooMQAPI().SendMessage("user.sendInvite","email")