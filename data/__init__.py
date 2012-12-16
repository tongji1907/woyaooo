__author__ = 'william'
from model import doc
from model import conversation
import sqlalchemy as sa
from sqlalchemy import create_engine
import ConfigParser
from sqlalchemy import orm
from sqlalchemy import MetaData
import dbfactory


def init_datafactory(engine):
    """Call me before using any of the tables or classes in the model."""
    sm = orm.sessionmaker(autoflush=True, bind=engine)
    #sm = orm.sessionmaker()
    #sm.configure(bind=engine)
    dbfactory.engine = engine
    #dbfactory.Session = orm.scoped_session(sm)
    dbfactory.Session = sm
    dbfactory.metadata = MetaData(bind =engine)
    config_mapping()

def config_mapping():
    t_doc = sa.Table('doc', dbfactory.metadata, autoload=True)
    t_conversation = sa.Table('conversation',dbfactory.metadata,autoload = True)
    orm.mapper(doc.Doc, t_doc)
    orm.mapper(conversation.Conversation,t_conversation)

def engine_from_config(configfile='db.config'):
    #config_file = open('db.config')
    config_file = open((configfile))
    configs = ConfigParser.ConfigParser()
    configs.readfp(config_file)
    config_file.close()

    db_name = configs.get('mysql','database')
    user_name = configs.get('mysql',"user")
    host_name = configs.get('mysql','host')
    password = configs.get('mysql',"password")
    engine_url = 'mysql://%s:%s@%s:3306/%s?charset=utf8' % (password,user_name,host_name,db_name)

    print (engine_url)
    engine =create_engine(engine_url,encoding = "utf-8",echo =True)
    return engine