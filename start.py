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

import urllib
import os.path
import Queue
import sys
import threading
import traceback
#import urllib2
from scraper import *
from data_storer import *
from parser import *

## Local configs
## Set these as needed locally
THUMB_IMG_DIR = 'data/thumbs'
LORES_IMG_DIR = 'data/lores'
HIRES_IMG_DIR = 'data/hires'
RAW_HTML_DIR = 'data/cdc-phil-raw-html'
MAX_DAEMONS = 50

def mkdir(dirname):
    if not os.path.isdir("./" + dirname + "/"):
        os.mkdir("./" + dirname + "/")

def bootstrap_filestructure():
    mkdir(THUMB_IMG_DIR)    
    mkdir(LORES_IMG_DIR)    
    mkdir(HIRES_IMG_DIR)    
    mkdir(RAW_HTML_DIR)    

def floorify(id):
    ## mod 100 the image id numbers to make smarter folders
    floor = id - id % 100
    floored = str(floor).zfill(5)[0:3]+"XX"
    return floored

def make_directories(ids, root_dir):
    ## directories for image downloads
    floors = map(floorify, ids)
    floor_dirs = set(floors)
    # convert the floors into strings of format like 015XX
    map((lambda dirname: mkdir(root_dir + '/' + dirname)), floor_dirs)

# hug thanks to http://www.ibm.com/developerworks/aix/library/au-threadingpython/
# this threading code is mostly from there
db_lock = threading.RLock()
class ImgDownloader(threading.Thread):
    def __init__(self, queue, root_dir, flag_table_object):
        threading.Thread.__init__(self)
        self.queue = queue
        self.root_dir = root_dir
        self.flag_table_object = flag_table_object
    def run(self):
        while True:
            ## grab url/id tuple from queue
            id_url_tuple = self.queue.get()
            try:
                print id_url_tuple
                id = id_url_tuple[0]
                url = id_url_tuple[1]
                path = './' + self.root_dir + '/' + floorify(id) + '/' + str(id).zfill(5) + url[-4:]
                urllib.urlretrieve(url, path)
                print "finished downloading " + url
                id_status_dict = {'id': id, 'status': 1}
                # signal to db that we're done downloading
                with db_lock:
                    self.flag_table_object.insert().execute(id_status_dict)
                    print "finished marking as downloaded" + url

                # signals to queue job is done
                self.queue.task_done()
            except KeyboardInterrupt:
                sys.exit(0)
                self.queue.task_done()
            except:
                print "ERROR: trouble dling image apparently... " + str(id)
                print path
                traceback.print_exc()
                self.queue.task_done()
                return None

def get_images(root_dir, db_column_name, flag_table, flag_table_object):
    ## takes: a directory global, url_to? from phil table, an image status table
    ## returns: images to folder structure and stores downloaded status table
    queue = Queue.Queue()
    # MAKE OUR THREADZZZ
    for i in range(MAX_DAEMONS):
        t = ImgDownloader(queue, root_dir, flag_table_object)
        t.setDaemon(True)
        t.start()

    # TODO: this solution is saddening. it's roundabout and icky. we did it because we suck at databases
    # get urls for all the images
    query = text("select id," + db_column_name + " from phil where " + db_column_name + "  != '';")
    ids_and_urls = db.execute(query).fetchall()
    id_dict = dict(ids_and_urls)

    # get the ids for all the images that we've already downloaded
    query = text("select id from " + flag_table + " where status = '1';")
    ids_to_remove = db.execute(query).fetchall()
    rm_dict = map((lambda tuple: tuple[0]), ids_to_remove)

    # remove them from our dict of urls to download images from
    for id_rm in rm_dict:
        del id_dict[id_rm]

    # generate list of ids from results dict
    ids = id_dict.keys()
    # bootstrap our file structure for our download
    make_directories(ids, root_dir)
    # enqueue all the results
    id_tuples = id_dict.items()
    map(queue.put, id_tuples)

    # wait on the queue until everything has been processed
    queue.join()
        

def get_all_images():
    get_images(THUMB_IMG_DIR, 'url_to_thumb_img', 'thumb_status', thumb_status_table)
    get_images(LORES_IMG_DIR, 'url_to_lores_img', 'lores_status', lores_status_table)
    get_images(HIRES_IMG_DIR, 'url_to_hires_img', 'hires_status', hires_status_table)

def store_raw_html(id, html):
    ## stores an html dump from the scraping process, just in case
    idstr = str(id).zfill(5)
    floor = id - (id%100)
    ceiling = str(floor + 100).zfill(5)
    floor = str(floor).zfill(5)
    mkdir(RAW_HTML_DIR + '/' + floor + '-' + ceiling)
    fp = open(RAW_HTML_DIR + '/' + floor + '-' + ceiling + '/' + idstr + '.html', 'w')
    fp.write(html)
    fp.close()


def store_datum(dict):
    ## stores scraped metadata into phil table
    # TODO: incorporate this into main function
    # TODO: 'table' is a db storage object so isn't descriptive
    table.execute(dict)

def cdc_phil_scrape_range(start, end):
    ## main glue function
    current_id = start
    try:
        cookiejar = get_me_a_cookie()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print "ERROR: WE COULDN'T EVEN GET A COOKIE"
        traceback.print_exc()
        return None
    failed_indices = []
    while current_id <= end:
        print "STARTING: " + str(current_id)
        try:
            # 1: fetching html of id, for store and parse
            html = cdc_phil_scrape(current_id, cookiejar)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print "ERROR: couldn't scrape out html for id " + str(current_id)
            failed_indices.append(current_id)
            traceback.print_exc()
            current_id+=1
            continue
        # if we didn't get a session error page:
        if not is_session_expired_page(html):
            try:
                # 2: write html to disk
                store_raw_html(current_id, html)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't store raw html for id " + str(current_id)
                failed_indices.append(current_id)
                current_id+=1
                continue
            try:
                # 3: parse the metadata out of their html
                metadata = parse_img(html)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't parse raw html for id " + str(current_id)
                metadata = {
                        'id': current_id,
                        'we_couldnt_parse_it': True,
                        }
                store_datum(metadata)
                print "we just recorded in the DB the fact that we couldn't parse this one"
                failed_indices.append(current_id)
                traceback.print_exc()
                current_id+=1
                continue
            try:
                store_datum(metadata)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't store metadata for id " + str(current_id)
                failed_indices.append(current_id)
                traceback.print_exc()
                current_id+=1
                continue
            # These lines will only run if everthing went according to plan
            print "SUCCESS: everything went according to plan for id " + str(current_id)
            current_id+=1
        # but if we got a session error page
        else:
            times_to_try_getting_cookie = 3
            print "SESSION error. Getting a new cookie...we'll give this " + str(times_to_try_getting_cookie) + " tries..."
            try_num = 1
            while try_num <= times_to_try_getting_cookie:
                try:
                    cookiejar = get_me_a_cookie()
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print "eep, no luck. giving it another shot..."
                    try_num+=1
                    continue
                # refreshed cookie, returning to loop
                print "SESSION success. got a new cookie."
                break

    print "HOLY CRAP WE ARE DONE"
    if not len(failed_indices) == 0:
        print "Failed at " + str(len(failed_indices)) + " indices :"
        print failed_indices

def get_highest_index_in_our_db():
    query = text("select id from phil order by id desc limit 1;")
    result = int(db.execute(query).fetchall()[0][0])
    return result

def database_is_empty():
    query = text("select id from phil order by id desc limit 1;")
    result = db.execute(query).fetchall()
    return not result

if __name__ == '__main__':
    bootstrap_filestructure()
    # note that we re-do our most recent thing.  just in case we died halfway through it or something
    # note also that we don't download any images until we run get_all_images()
    if database_is_empty():
        print "looks like the database is empty"
        start_from = 0
    else:
        start_from = get_highest_index_in_our_db()
    end_with = get_highest_index_at_phil()
    end_with = 500
    print "looks like the highest index in their db is %s, so i'll end with that" % end_with
    print "i'm about to scrape out raw dumps and grab metadata for %s - %s" % (start_from, end_with)
    cdc_phil_scrape_range(start_from, end_with)
    # don't worry--this only downloads images that we don't already have marked as downloaded in our database
    # get_all_images()
