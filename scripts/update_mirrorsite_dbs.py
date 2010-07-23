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

# NOTE: this must be run form the root of this repo
from collect_phil_cdc.data_storer import *

from collect_phil_cdc.config import *
data_mysql_db = create_engine('mysql://%s:%s@%s/%s' % (data_mysql_db_user, data_mysql_db_pass, data_mysql_db_host, data_mysql_db_db))

metadata = MetaData(bind=data_mysql_db)

mysql_phil_table = Table('phil', metadata,
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

metadata.create_all(data_mysql_db)

mysql_phil_table.insert()

data_mysql_db_connection = data_mysql_db.connect()

# convert only the unconverted (meaning "new") lines int he sqlite into mysql (just grab and store)
def from_sqlite_to_mysql(sqlite_connection, mysql_table_obj):
    # get highest index in the mysql data table
    try:
        query = text("SELECT id FROM `phil` ORDER BY `id` DESC limit 1;")
        data_mysql_db_max_id = int(data_mysql_db_connection.execute(query).fetchall()[0][0])
    except IndexError:
        # in this edge case, we have ZERO posts in the mysql data database
        data_mysql_db_max_id = (-1)

    # grab all the new stuff from the sqlite
    result = sqlite_connection.execute("select * from %s where id > %d" % (mysql_table_obj.name, data_mysql_db_max_id))
    # and put it in
    for row in result:
	try:
		mysql_table_obj.insert().execute(row)
	except:
		print "hm. error inserting converting this row from sqlite to mysql"
    result.close()

def hack_wp_db():
    db = create_engine('mysql://%s:%s@%s/%s' % (wp_db_user, wp_db_pass, wp_db_host, wp_db_db))
    connection = db.connect()
    # get highest index in the table of posts
    query = text("SELECT id FROM `wp_posts` ORDER BY `id` DESC limit 1;")
    try:
        highest_post_index = int(db.execute(query).fetchall()[0][0])
    except IndexError:
        # in this case, we have ZERO posts in the wp database
        highest_post_index = (-1)
    highest_data_index = get_highest_index_in_our_db()
    num_posts_to_add = highest_data_index - highest_post_index
    for i in range(num_posts_to_add):
        connection.execute('INSERT INTO wp_posts (post_type) VALUES ("page");');

    
if __name__ == '__main__':
    # we already have a database and a session defined in data_storer.py
    from_sqlite_to_mysql(data_sqlite_session, mysql_phil_table)
    hack_wp_db()
