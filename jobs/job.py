import data

from data import dbfactory
from data import doc

engine =data.engine_from_config()
db = data.init_datafactory(engine)

query = dbfactory.Session.session.query(doc.Doc).all()
dbfactory.Session.flush()

for item in query:
    print item['url']