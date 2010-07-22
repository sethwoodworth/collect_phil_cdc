################################################################################
################################################################################
#####################                                  #########################
#####################         Release Our Data         #########################
#####################                                  #########################
#####################       a HelloSilo Project        #########################
#####################       <ROD@hellosilo.com>        #########################
################################################################################
##                                                                            ##  
##     Copyright 2010                                                         ##
##                                                                            ##  
##         Parker Phinney   @gameguy43   <parker@madebyparker.com>            ##
##         Seth Woodworth   @sethish     <seth@sethish.com>                   ##
##                                                                            ##
##                                                                            ##
##     Licensed under the GPLv3 or later,                                     ##
##     see PERMISSION for copying permission                                  ##
##     and COPYING for the GPL License                                        ##
##                                                                            ##
################################################################################
################################################################################

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper


from config import *

data_sqlite_db = create_engine('sqlite://%s:%s@%s/%s' % (data_sqlite_db_user, data_sqlite_db_pass, data_sqlite_db_host, data_sqlite_db_db))

#data_sqlite_db.echo = True     #uncomment for db debug
metadata = MetaData(data_sqlite_db)

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
    Column('url_to_thumb_img', Text),  # seth: static url to thumb images
    Column('copyright', Text),  # Copyright Status - either "Public Domain" (free use) or Copyright Protected
#   Column('is_color', Boolean),    # Color Scheme - Color or Black & White # provide, but not printed, null for now
    Column('creation', Text),   # Creation Date - When the object was created (photo taken, video shot, etc.)

    #TODO: upload exists only here, but we have the data, add it back if exists in fields
# I don't even know what the above means any more--i think it refers to a field called "upload" which we seem to not have any more
    Column('access_time', DateTime), # seth: time/day we accessed the content
    Column('doesnt_exist', Boolean), # parker: set to true if the image seems to not be in the database
    Column('we_couldnt_parse_it', Boolean), # parker: set to true if we encountered a parse error when trying to extract the metadata
)

hires_status_table = Table('hires_status', metadata,
    Column('id', Integer, primary_key=True),
    Column('status', Boolean)
)
hires_status_table.insert()

lores_status_table = Table('lores_status', metadata,
    Column('id', Integer, primary_key=True),
    Column('status', Boolean),
)
lores_status_table.insert()

thumb_status_table = Table('thumb_status', metadata,
    Column('id', Integer, primary_key=True),
    Column('status', Boolean),
)
thumb_status_table.insert()


metadata.create_all(data_sqlite_db)


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
    url_to_thumb_img = Column(String)
    copyright = Column(String)
#   is_color = Column(Boolean)
    creation = Column(String)
    access_time = Column(Integer)
    doesnt_exist = Column(Boolean)
    we_couldnt_parse_it = Column(Boolean)



    def __init__(self, id, desc, categories, credit, links, provider, source, url_to_hires_img, url_to_lores_img, url_to_thumb_img, copyright, creation, access_time, doesnt_exist, we_couldnt_parse_it):
        self.id = id
        self.desc = desc
        self.categories = categories
        self.credit = credit
        self.links = links
        self.provider = provider
        self.source = source
        self.url_to_hires_img = url_to_hires_img
        self.url_to_lores_img = url_to_lores_img
        self.url_to_thumb_img = url_to_thumb_img
        self.copyright = copyright
        self.creation = creation
        self.access_time = access_time
        self.doesnt_exist = Column(Boolean)
        self.we_couldnt_parse_it = Column(Boolean)


    def __repr__(self):
        return "<Phil('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s')>" % (self.id, self.desc, self.categories, self.credit, self.links, self.provider, self.source, self.url_to_hires_img, self.url_to_lores_img, self.url_to_thumb_img, self.copyright, self.creation, self.upload, self.access_time, self.doesnt_exist, self.we_couldnt_parse_it)

Session = sessionmaker(bind=data_sqlite_db)
data_sqlite_session = Session()

table = phil_table.insert()

#table.execute(metadata)
#table.commit()

def get_highest_index_in_table(session, table_obj):
    return int(session.query(table_obj.id).order_by(desc(table_obj.id)).first()[0])

def get_highest_index_in_our_db():
    return get_highest_index_in_table(data_sqlite_session, Phil)
    #query = text("select id from phil order by id desc limit 1;")
    #result = int(data_sqlite_db.execute(query).fetchall()[0][0])
    #return result

def database_is_empty():
    query = text("select id from phil order by id desc limit 1;")
    result = data_sqlite_db.execute(query).fetchall()
    return not result

def store_datum(dict):
    ## stores scraped metadata into phil table
    # TODO: incorporate this into main function
    # TODO: 'table' is a db storage object so isn't descriptive
    table.execute(dict)

def get_dict_of_images_to_dl(db_column_name, flag_table):
    # TODO: this solution is saddening. it's roundabout and icky. we did it because we suck at databases
    # get urls for all the images
    query = text("select id," + db_column_name + " from phil where " + db_column_name + "  != '';")
    ids_and_urls = data_sqlite_db.execute(query).fetchall()
    id_dict = dict(ids_and_urls)

    # get the ids for all the images that we've already downloaded
    query = text("select id from " + flag_table + " where status = 1;")
    ids_to_remove = data_sqlite_db.execute(query).fetchall()
    rm_dict = map((lambda tuple: tuple[0]), ids_to_remove)

    # remove them from our dict of urls to download images from
    for id_rm in rm_dict:
        if id_rm in id_dict:
            del id_dict[id_rm]

    return id_dict

#if __name__ == '__main__':
#    test_db()
