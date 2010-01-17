from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper


db = create_engine('sqlite:///phil.cdc.sql')

#db.echo = True     #uncomment for db debug
metadata = MetaData(db)

phil_table = Table('phil', metadata,
    Column('id', Integer, primary_key=True),
    Column('desc', Text),         # Description - Extensive and authoritative explanation of the visual image or video file
    Column('categories', Text),   # Categories - used to describe the image
    Column('credit', Text),       # Photo Credit - Photographer or Videographer who took the photo or shot the video
    Column('links', Text),       # seth: url to other cdc content
    Column('provider', Text),      # Content Provider - The contributor of the asset
                                    # Source is possibly ficional, we haven't proven either way
    Column('source', Text),       # Source Library - Where the image originated
    Column('url_to_hires_img', Text),  # seth: static url to hi-res images
    Column('url_to_lores_img', Text),  # seth: static url to lo-res images
    Column('copyright', Text),  # Copyright Status - either "Public Domain" (free use) or Copyright Protected
#   Column('is_color', Boolean),    # Color Scheme - Color or Black & White # provide, but not printed, null for now
    Column('creation', Text),   # Creation Date - When the object was created (photo taken, video shot, etc.)

    #TODO: upload exists only here, but we have the data, add it back if exists in fields
    Column('access_time', DateTime) # seth: time/day we accessed the content
)

hires_status_table = Table('hires_status', metadata,
    Column('id', Integer, primary_key=True),
    Column('status', Boolean)
)

lores_status_table = Table('lores_status', metadata,
    Column('id', Integer, primary_key=True),
    Column('status', Boolean),
)

thumbs_status_table = Table('thumbs_status', metadata,
    Column('id', Integer, primary_key=True),
    Column('status', Boolean),
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
    links = Column(String)
    provider = Column(String)
    source = Column(String)
    url_to_hires_img = Column(String)
    url_to_lores_img = Column(String)
    copyright = Column(String)
#   is_color = Column(Boolean)
    creation = Column(String)
    access_time = Column(Integer)


    def __init__(self, id, desc, categories, credit, links, provider, source, url_to_hires_img, url_to_lores_img, copyright, creation, access_time):
        self.id = id
        self.desc = desc
        self.categories = categories
        self.credit = credit
        self.links = links
        self.provider = provider
        self.source = source
        self.url_to_hires_img = url_to_hires_img
        self.url_to_lores_img = url_to_lores_img
        self.copyright = copyright
        self.creation = creation
        self.access_time = access_time


    def __repr__(self):
        return "<Phil('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',)>" % (self.id, self.desc, self.categories, self.credit, self.links, self.provider, self.source, self.url_to_hires_img, self.url_to_lores_img, self.copyright, self.creation, self.upload, self.access_time)

Session = sessionmaker(bind=db)
session = Session()

table = phil_table.insert()

#table.execute(metadata)
#table.commit()


#if __name__ == '__main__':
#    test_db()
