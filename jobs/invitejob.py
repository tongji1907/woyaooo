# -*- coding: utf-8 -*-
from lucene import *
from lucene import SimpleFSDirectory, System, File,\
    Document, Field, StandardAnalyzer,ChineseAnalyzer,CJKAnalyzer, IndexWriter, Version,\
    IndexSearcher, QueryParser, MultiFieldQueryParser, IndexReader, Term, DateTools

from model import doc_model
from mq import mq_api
from algorithm import bayes

import re


def do_invite(keywords):
    print "invite started!>>>>>>"
    initVM()
    indexDir  = "/home/william/woyaoo/luceneindex"
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
    toInviteEmails.append("csonnet@hotmail.com")
    toInviteEmails.append("haiming.chen@gmail.com")
    toInviteEmails.append("wangxue9871@163.com")
    #remove multipule emails

    toInviteEmails = set(inviteEmails)
    print "invite total" +str(len(toInviteEmails))+" emails >>>>>>>>>>>"
    #for mail_address in toInviteEmails:
       # print mail_address
    return toInviteEmails


if __name__=="__main__":
    do_invite("我想买一辆车，10万以内的，请报价或建议。谢谢")
    #WoyaoooMQAPI().SendMessage("user.sendInvite","email")