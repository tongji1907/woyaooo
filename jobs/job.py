import data

from data import dbfactory
from model import doc

engine =data.engine_from_config()
db = data.init_datafactory(engine)


items = dbfactory.Session().query(doc.Doc).all()

for item in items:
    print item.intent
    s = item.intent
    for t in s:
        print t
    #for inent in item.intent:
    #    print inent



