__author__ = 'william'

import dbfactory
import conversation
def do_extract():
    df = dbfactory.DBFactory()
    df.init_dbfactory()
    session = df.getSession()
    conversations = session.query(conversation.Conversation).all()
    for item in conversations:

        if item.description!=None and len(item.description)<10:
            print item.description
            item.subject = item.description
            item.title = '['+item.intention+']'+item.subject
        session.commit()
if __name__=="__main__":
    do_extract()