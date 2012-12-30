# -*- coding: utf-8 -*-
from lucene import *
from lucene import SimpleFSDirectory, System, File,\
    Document, Field, StandardAnalyzer,ChineseAnalyzer,CJKAnalyzer, IndexWriter, Version,\
    IndexSearcher, QueryParser, MultiFieldQueryParser, IndexReader, Term, DateTools
import mq
from model import doc_model
from mq import mq_api
import re


def do_invite(keywords):
    initVM()
    indexDir  = "/home/william/woyaoo/luceneindex"
    version   = Version.LUCENE_CURRENT
    idxDir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(version)
    searcher = IndexSearcher(idxDir)
    query = QueryParser(version, "description", analyzer).parse(keywords)
    hits = searcher.search(query, 1000)
    indentCandidates = []

    print len(hits.scoreDocs)
    for hit in hits.scoreDocs:
        print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        intents = doc.get("intent")
        print doc.get("url")
        if intents == None:
            continue
        intents = eval(intents)

        for intent in intents:
            indentCandidates.append(intent)

    searcher.close()
    inviteEmails = []
    patterns = ["[^A-Za-z0-9_-]*(?P<buzz>([A-Za-z0-9_-]+(\.\w+)*@(\w+\.)+\w{2,3}))", '''qq[^\d]*(?P<buzz>[1-9][0-9]{4,})''']
    for indentCandidate in indentCandidates:


        emailPattern = patterns[0]
        qqPattern = patterns[1]
        qqMatches =re.finditer(qqPattern,indentCandidate, re.IGNORECASE| re.DOTALL)
        emailMatches = re.finditer(emailPattern,indentCandidate, re.IGNORECASE| re.DOTALL)

        for qqMatch in qqMatches:
            qq = qqMatch.group("buzz").strip()
        #print qq
            qqMail = qq+"@qq.com"
            inviteEmails.append(qqMail)

        for emailMatch in emailMatches:
            email = emailMatch.group("buzz").strip()
            #print email

            inviteEmails.append(email)



    #remove multipule emails
    toInviteEmails = set(inviteEmails)
    print len(toInviteEmails)
    for mail_address in toInviteEmails:
        print mail_address
    return toInviteEmails


if __name__=="__main__":
    do_invite("八")
    #WoyaoooMQAPI().SendMessage("user.sendInvite","email")