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

# move this to the root of the collect-cdc-phil directory to populate the thumb field of the phil table
import re
from data_storer import *

def fix_thumb_field():
    query = text("select id,url_to_lores_img from phil;")
    id_urls = db.execute(query).fetchall()
    for id_url in id_urls:
        id = id_url[0]
        lores_url = id_url[1]
        thumb_url = re.sub('_lores.jpg', '_thumb.jpg', lores_url)
        update_statement = "update phil set url_to_thumb_img = '" + thumb_url + "' where id = " + str(id) + ";"
        db.execute(update_statement)


if __name__ == '__main__':
    fix_thumb_field()
