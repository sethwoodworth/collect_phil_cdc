from BeautifulSoup import BeautifulStoneSoup
import urllib
import urllib2
import re
from datetime import datetime,date
import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

#database config
engine = create_engine('sqlite:///phil.cdc.sql')

# Instantiate the db #

metadata = MetaData()
phil_table = Table('phil', metadata,
    Column('id', Integer, primary_key=True),
    Column('', String),
    Column('', String),
    Column('creation_date', DateTime),
    Column('access_time', DateTime)
)
metadata.create_all(engine) 
 
# DB Class interactions 
Base = declarative_base()

class Talert(Base):
    __tablename__ = 'talerts'

    id = Column(Integer, primary_key=True)
    guid = Column(Integer, unique=True)
    title = Column(String)
    content = Column(String)
    mbta_date = Column(Integer)
    timestamp = Column(Integer)

    def __init__(self, guid, title, content, mbta_date, timestamp):
        self.guid = guid
        self.title = title
        self.content = content
        self.mbta_date = mbta_date
        self.timestamp = timestamp

    def __repr__(self):
        return "<Talert('%s','%s','%s','%s','%s')>" % (self.guid, self.title, self.content, self.mbta_date, self.timestamp)

    def guid(self):
        return self.guid

Session = sessionmaker(bind=engine)
session = Session()

# Setting up the MBTA XML feed, and cleaning it
print 'Pulling the MBTA feed and making Soup'
url = 'http://talerts.com/rssfeed/alertsrss.aspx'
response = urllib.urlopen(url)
raw_xml = response.read()
xmlSoup = BeautifulStoneSoup(raw_xml)

def parse_item(item):
    # Return the elements of the items
    # guid comes in as talerts##########, remove and convert to int

    guid = int(re.sub('talerts','',item.find("guid").find(text=True)))
    date_raw = item.find("pubdate").find(text=True)
    title = item.find("title").find(text=True)
    content = item.find("description").find(text=True)
    
    # MBTA's date format is odd, convert to Unix time then to ISO standard
    date_str = time.strptime(date_raw, '%a, %d %b %Y %H:%M:%S GMT')
    date = time.strftime("%Y-%m-%d %H:%M:%S", date_str)
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	#cur_time = datetime.now()

    return Talert(guid, title, content, date, cur_time)

def item_block(soup):
    # Take xml and generate items to be inserted
    for channel in soup.findAll('item'):
        to_add = parse_item(channel)
        session.add(to_add)
    print 'Good, got it, storing now'
    session.commit()

item_block(xmlSoup)
