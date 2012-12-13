__author__ = 'william'

import sqlalchemy as sa
from sqlalchemy import orm

import dbfactory

t_doc = sa.Table('doc', dbfactory.metadata, autoload=True)

class Doc(object):
    pass

orm.mapper(Doc, t_doc)