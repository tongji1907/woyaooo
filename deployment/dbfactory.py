__author__ = 'william'
"""SQLAlchemy Metadata and Session object"""
import doc_model
import conversation
import talk
import sqlalchemy as sa
from sqlalchemy import create_engine
import ConfigParser
from sqlalchemy import orm
from sqlalchemy import MetaData

from sqlalchemy import MetaData

#__all__ = ['engine', 'metadata', 'Session']
'''
def init_datafactory(engine):
    """Call me before using any of the tables or classes in the model."""
    sm = orm.sessionmaker(autoflush=True, bind=engine)
    #sm = orm.sessionmaker()
    #sm.configure(bind=engine)
    engine = engine
    #dbfactory.Session = orm.scoped_session(sm)
    Session = sm
    metadata = MetaData(bind =engine)
    config_mapping()

def config_mapping():
    t_doc = sa.Table('doc',metadata, autoload=True)
    t_conversation = sa.Table('conversation',metadata,autoload = True)
    t_talk = sa.Table("talk",metadata,autoload =True)
    #t_bayes = sa.Table("bayes_lib",dbfactory.metadata,autoload = True)
    orm.mapper(doc_model.Doc, t_doc)
    orm.mapper(conversation.Conversation,t_conversation)
    orm.mapper(talk.Talk,t_talk)
    #orm.mapper(bayeslib.BayeseLib,t_bayes)

def engine_from_config(configfile='dbconfig/db.config'):
    #config_file = open('db.config')
    config_file = open((configfile))
    configs = ConfigParser.ConfigParser()
    configs.readfp(config_file)
    config_file.close()
    db_name = configs.get('mysql','database')
    user_name = configs.get('mysql',"user")
    host_name = configs.get('mysql','host')
    password = configs.get('mysql',"password")
    engine_url = 'mysql://%s:%s@%s:3306/%s?charset=utf8' % (user_name,password,host_name,db_name)
    print (engine_url)
    engine =create_engine(engine_url,encoding = "utf-8",echo =False)
    return engine
'''
class DBFactory():

    session = None
    def __init__(self):
        pass
    def init_dbfactory(self,configfile='dbconfig/db.config'):
        config_file = open((configfile))
        configs = ConfigParser.ConfigParser()
        configs.readfp(config_file)
        config_file.close()
        db_name = configs.get('mysql','database')
        user_name = configs.get('mysql',"user")
        host_name = configs.get('mysql','host')
        password = configs.get('mysql',"password")
        engine_url = 'mysql://%s:%s@%s:3306/%s?charset=utf8' % (user_name,password,host_name,db_name)
        print (engine_url)
        engine =create_engine(engine_url,encoding = "utf-8",echo =False)
        sm = orm.sessionmaker(autoflush=True, bind=engine)
        self.session = sm
        metadata = MetaData(bind =engine)
        t_doc = sa.Table('doc',metadata, autoload=True)
        t_conversation = sa.Table('conversation',metadata,autoload = True)
        t_talk = sa.Table("talk",metadata,autoload =True)
        #t_bayes = sa.Table("bayes_lib",dbfactory.metadata,autoload = True)
        orm.mapper(doc_model.Doc, t_doc)
        orm.mapper(conversation.Conversation,t_conversation)
        orm.mapper(talk.Talk,t_talk)

    def getSession(self):
        return self.session()

