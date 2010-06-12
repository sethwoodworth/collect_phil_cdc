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

# this file adds all the necessary empty "page"s to the wordpress mysql database so that it hooks up to our mysql database of data properly (the wp install thinks the image pages are just normal static "page"s)


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper
import sys

if len(sys.argv) <= 1:
    sys.exit("requires one arg: number of pages to add")

from wp_credentials import *
db = create_engine('mysql://%s:%s@%s/%s' % (db_user, db_pass, db_host, db_db))
connection = db.connect()

for i in range(int(sys.argv[1])):
    connection.execute('INSERT INTO wp_posts (post_type) VALUES ("page");');
