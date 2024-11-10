from datetime import datetime
from sqlalchemy import Integer
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative

@as_declarative()
class BaseEntity(object):
    created_at = Column(Integer, default=int(datetime.now().timestamp()))
    updated_at = Column(Integer, default=int(datetime.now().timestamp()))
