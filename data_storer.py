from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper


db = create_engine('sqlite:///phil.cdc.sql')

#db.echo = True     #uncomment for db debug
metadata = MetaData(db)

phil_table = Table('phil', metadata,
    Column('id', Integer, primary_key=True),
    Column('desc', String),         # Description - Extensive and authoritative explanation of the visual image or video file
    Column('categories', String),   # Categories - used to describe the image
    Column('credit', String),       # Photo Credit - Photographer or Videographer who took the photo or shot the video
    Column('provider', String),      # Content Provider - The contributor of the asset
    Column('source', String),       # Source Library - Where the image originated
    Column('path_to_img', String),  # seth: static url to hi-res images
    Column('is_color', Boolean),    # Color Scheme - Color or Black & White
    Column('creation', DateTime),   # Creation Date - When the object was created (photo taken, video shot, etc.)
    Column('upload', DateTime),     # Upload Date - When the image entered the PHIL database
    Column('access_time', DateTime) # seth: time/day we accessed the content
)
metadata.create_all(db)


# DB Class interactions 
Base = declarative_base()

class Phil(Base):
    __tablename__ = 'phil'

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    categories = Column(String)
    credit = Column(String)
    provider = Column(String)
    source = Column(String)
    path_to_img = Column(String)
    is_color = Column(Boolean)
    creation = Column(Integer)
    access_time = Column(Integer)

    def __init__(self, id, desc, categories, credit, provider, source, path_to_img, is_color, creation, access_time):
        self.id = id
        self.desc = desc
        self.categories = categories
        self.credit = credit
        self.provider = provider
        self.source = source
        self.path_to_img = path_to_img
        self.is_color = is_color
        self.creation = creation
        self.access_time = access_time


    def __repr__(self):
        return "<Phil('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.id, self.desc, self.categories, self.credit, self.provider, self.source, self.path_to_img, self.is_color, self.creation, self.access_time)

Session = sessionmaker(bind=db)
session = Session()


def test_db():
    barv = Phil(0, 'desc', 'categories', 'credit', 'provider', 'source', 'path_to_img', 'True', 0000, 0000)
    session.add(barv)
    session.commit()


if __name__ == '__main__':
    test_db()
