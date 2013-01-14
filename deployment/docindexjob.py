# -*- coding: utf-8 -*-
import dbfactory
import doc_model

from lucene import *
from lucene import SimpleFSDirectory, System, File,\
    Document, Field, StandardAnalyzer,ChineseAnalyzer,CJKAnalyzer, IndexWriter, Version,\
    IndexSearcher, QueryParser, MultiFieldQueryParser, IndexReader, Term, DateTools

def do_index():
    initVM()
    indexDir  = "/home/william/woyaoo/luceneindex"
    version   = Version.LUCENE_CURRENT
    standardAnalyzer  = StandardAnalyzer(version)
    #chineseAnalyzer = CJKAnalyzer(version)
    df = dbfactory.DBFactory()
    df.init_dbfactory('dbconfig/indexdb.config')

    docs = df.getSession().query(doc_model.Doc).filter(doc_model.Doc.dateCreated>'20121220').all()
    print len(docs)
    idxDir = SimpleFSDirectory(File(indexDir))
    perIndexCount = 5000
    writer = IndexWriter(idxDir, standardAnalyzer, True, IndexWriter.MaxFieldLength(512))

    #add field
    for doc in docs:
        #print repr(doc.description)
        lucenedoc = Document()
        descriptionValue = doc.description.strip('\r\n').encode("UTF-8")
        #descriptionValue ='中国 abc'
        print repr(descriptionValue)
        lucenedoc.add(Field('url', doc.url, Field.Store.YES, Field.Index.NOT_ANALYZED))
        lucenedoc.add(Field('intent', doc.intent, Field.Store.YES, Field.Index.NOT_ANALYZED))
        #lucenedoc.add(Field('description', doc.description, Field.Store.YES, Field.Index.ANALYZED))
        lucenedoc.add(Field('description', descriptionValue, Field.Store.YES, Field.Index.ANALYZED))
        lucenedoc.add(Field('title',doc.title,Field.Store.YES,Field.Index.ANALYZED))
        writer.addDocument(lucenedoc)
        writer.optimize()
    writer.close()
    print "index finished"

if __name__=="__main__":
    do_index()

