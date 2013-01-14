__author__ = 'william'
# -*- coding: utf-8 -*-


from lucene import *
#from lucene import SimpleFSDirectory, System, File,\
#    Document, Field, StandardAnalyzer,ChineseAnalyzer,CJKAnalyzer, IndexWriter, Version,\
#    IndexSearcher, QueryParser, MultiFieldQueryParser, IndexReader, Term, DateTools

import dbfactory
import conversation


def do_index():
    initVM()
    indexDir  = "/tmp/luceneindex/conversation"
    version   = Version.LUCENE_CURRENT
    standardAnalyzer  = StandardAnalyzer(version)

    df = dbfactory.DBFactory()
    df.init_dbfactory()
    conversations = df.getSession().query(conversation.Conversation).all()
    print len(conversations)
    idxDir = SimpleFSDirectory(File(indexDir))
    perIndexCount = 5000
    writer = IndexWriter(idxDir, standardAnalyzer, True, IndexWriter.MaxFieldLength(512))

    #add field
    for doc in conversations:
        #print repr(doc.description)
        lucenedoc = Document()
        if  doc.description == None:
            descriptionValue = ''
        else:

            descriptionValue = doc.description.strip('\r\n').encode("UTF-8")
        if doc.title == None:
            titleVaue = ''
        else:
            titleValue = doc.title.strip('\r\n').encode("UTF-8")
        if doc.abstract == None:
            abstractValue = ''
        else:
            abstractValue = doc.abstract.strip('\r\n').encode("UTF-8")
        print repr(descriptionValue)
        lucenedoc.add(Field('id', doc.id, Field.Store.YES, Field.Index.NOT_ANALYZED))
        lucenedoc.add(Field('intention', doc.intention, Field.Store.YES, Field.Index.NOT_ANALYZED))
        lucenedoc.add(Field('dateSubmitted', str(doc.dateSubmitted), Field.Store.YES, Field.Index.NOT_ANALYZED))
        lucenedoc.add(Field('abstract', abstractValue, Field.Store.YES, Field.Index.NOT_ANALYZED))
        lucenedoc.add(Field('description', descriptionValue, Field.Store.YES, Field.Index.ANALYZED))
        lucenedoc.add(Field('title',titleValue,Field.Store.YES,Field.Index.ANALYZED))
        writer.addDocument(lucenedoc)
        writer.optimize()
    writer.close()
    print "index finished"

def do_lucene_search(keywords):
    print "search conversation started!>>>>>>"
    initVM()
    indexDir  = "/tmp/luceneindex/conversation"
    version   = Version.LUCENE_CURRENT
    idxDir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(version)
    searcher = IndexSearcher(idxDir)
    query = QueryParser(version, "description", analyzer).parse(keywords)
    hits = searcher.search(query, 1000)


    for hit in hits.scoreDocs:
        print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print "description: "+doc.get("description")
        print "id: "+doc.get("id")
        print "intention: " +doc.get("intention")
        print "dateSubmitted: "+doc.get("dateSubmitted")
        print "abstract: "+doc.get("abstract")
        print "title: "+doc.get("title")
if __name__=="__main__":
    do_index()
    do_lucene_search("我")
