# -*- coding: utf-8 -*-
import data
from lucene import *
from lucene import SimpleFSDirectory, System, File,\
    Document, Field, StandardAnalyzer,ChineseAnalyzer,CJKAnalyzer, IndexWriter, Version,\
    IndexSearcher, QueryParser, MultiFieldQueryParser, IndexReader, Term, DateTools

from data import dbfactory
from model import doc
from model import conversation
from mq_api import WoyaoooMQAPI
import re

if __name__=="__main__":
    initVM()
    indexDir  = "/home/william/woyaoo/luceneindex"
    version   = Version.LUCENE_CURRENT
    idxDir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(version)
    #analyzer = CJKAnalyzer(version)
    searcher = IndexSearcher(idxDir)
    query = QueryParser(version, "description", analyzer).parse('猪八戒')
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
    patterns = [ur"""[\u2E80-\uFFFD]*qq\s*[:|：]*\s*(?P<buzz>[1-9]*[1-9][0-9]*)""", ur"""[\u2E80-\uFFFD]*\s*(?P<buzz>([A-Za-z0-9_-]+(\.\w+)*@(\w+\.)+\w{2,3}))\s*"""]
    for indentCandidate in indentCandidates:
        #ismatch = False
        for onepattern in patterns:
            emailmatch = re.finditer(onepattern,indentCandidate, re.IGNORECASE| re.DOTALL)
            #self.mat += 1
            for oneemail in emailmatch:
                #if(oneemail)
                themail = oneemail.group("buzz").strip()
                inviteEmails.append(themail)
                print themail


    #WoyaoooMQAPI().SendMessage("user.sendInvite","email")