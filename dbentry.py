from sqlalchemy import DateTime, Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    msgid = Column(String)
    timestamp = Column(DateTime)
    entry = Column(String)

    def __repr__(self):
        return "(%d) %s: %d" % (self.msgid, self.timestamp, self.entry)
