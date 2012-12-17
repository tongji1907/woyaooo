# -*- coding: utf-8 -*-
import data
from lucene import *
from lucene import SimpleFSDirectory, System, File,\
    Document, Field, StandardAnalyzer,ChineseAnalyzer,CJKAnalyzer, IndexWriter, Version,\
    IndexSearcher, QueryParser, MultiFieldQueryParser, IndexReader, Term, DateTools

from data import dbfactory
from model import doc
from model import conversation


if __name__=="__main__":
    initVM()
    indexDir  = "/home/william/woyaoo/luceneindex"
    version   = Version.LUCENE_CURRENT
    standardAnalyzer  = StandardAnalyzer(version)
    #chineseAnalyzer = CJKAnalyzer(version)
    #engine =data.engine_from_config('indexdb.config')
    engine = data.engine_from_config()
    db = data.init_datafactory(engine)
    docs = dbfactory.Session().query(doc.Doc).all()
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

