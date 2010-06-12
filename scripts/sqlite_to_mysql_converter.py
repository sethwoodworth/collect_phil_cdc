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


#db = create_engine('mysql://root@localhost/phil')
#db = create_engine('mysql://phil:toast@localhost/cdc_phil_data_test')
db = create_engine('mysql://phil:toast@localhost/cdc_phil_data')

metadata = MetaData(bind=db)

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
    Column('access_time', DateTime), # seth: time/day we accessed the content
    mysql_charset='utf8'
)
#
#hires_status_table = Table('hires_status', metadata,
#    Column('id', Integer, primary_key=True),
#    Column('status', Boolean),
#    mysql_charset='utf8'
#)
#
#lores_status_table = Table('lores_status', metadata,
#    Column('id', Integer, primary_key=True),
#    Column('status', Boolean),
#    mysql_charset='utf8'
#)
#
#thumb_status_table = Table('thumb_status', metadata,
#    Column('id', Integer, primary_key=True),
#    Column('status', Boolean),
#    mysql_charset='utf8'
#)

metadata.create_all(db)

table = phil_table.insert()

def from_sqlite_to_mysql():
    db2 = create_engine('sqlite:///full.sql')
    connection2 = db2.connect()
    
    #for table in metadata.table_iterator(reverse=False):
    table = phil_table
    result = connection2.execute("select * from %s" % table.name)
    for row in result:
        table.insert().execute(row)
    result.close()
    connection2.close()

    
if __name__ == '__main__':
    from_sqlite_to_mysql()
