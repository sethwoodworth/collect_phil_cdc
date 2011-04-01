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
from data_storer import *
import start

from config import *

import os


def update_db_based_on_img_files_on_disc(root_dir, flag_table_object, extension, cap):
    # clear out the current statuses
    # TODO: this doesn't work yet.
    flag_table_object.delete("*")
    for id in range(1, cap):
        path = root_dir + '/' + start.floorify(id) + '/' + str(id).zfill(5) + '.' + extension

        if os.path.isfile(path):
            # mark in the db that this file exists
            id_status_dict = {'id': id, 'status': 1}
            flag_table_object.insert().execute(id_status_dict)

def update_db_based_on_all_img_files_on_disc(cap):

    update_db_based_on_img_files_on_disc(HIRES_IMG_DIR, hires_status_table, 'tif', cap)
    update_db_based_on_img_files_on_disc(THUMB_IMG_DIR, thumb_status_table, 'jpg', cap)
    update_db_based_on_img_files_on_disc(LORES_IMG_DIR, lores_status_table, 'jpg', cap)


if __name__ == '__main__':
    # otherwise it would go forever
    # cap = 
    # cap = int(get_highest_index_in_our_db()) + 1
    cap = 11900
    update_db_based_on_all_img_files_on_disc(cap)
