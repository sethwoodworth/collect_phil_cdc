import urllib
import os.path
import sys
import traceback
#import urllib2
from scraper import *
from data_storer import *
from parser import *

################################################################################
#####################                                  #########################
#####################         Release Our Data         #########################
#####################                                  #########################
################################################################################

#####
#####  A HelloSilo Project
#####  ROD@HelloSilo.com
#####

#####
##### Authors:
##### Parker Phinney @gameguy43   (parker@madebyparker.com)
##### Seth Woodworth @sethish     (seth@sethish.com)
#####

## Local configs
## Set these as needed locally
HIRES_IMG_DIR = 'hires'
LORES_IMG_DIR = 'thumbs'
RAW_HTML_DIR = 'cdc-phil-raw-html'

def mkdir(dirname):
    if not os.path.isdir("./" + dirname + "/"):
        os.mkdir("./" + dirname + "/")

def bootstrap_filestructure():
    mkdir(HIRES_IMG_DIR)
    mkdir(LORES_IMG_DIR)
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

class ImgDownloader(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            #grabs url/id tuple from queue
            id_url_tuple = self.queue.get()
            id = id_url_tuple[0]
            url = id_url_tuple[1]
            path = './' + root_dir + '/' + floorify(id) + '/' + str(id).zfill(5) + url[-4:]
            urllib.urlretrieve(url, path)
            s = text('REPLACE INTO ' + flag_table + ' (id,status) values (' + id + ',1);')
            db.execute(s)
            #signals to queue job is done
            self.queue.task_done()

MAX_DAEMONS = 5

def get_images(root_dir, db_column_name, flag_table):
    ## takes: a directory global, url_to? from phil table, an image status table
    ## returns: images to folder structure and stores downloaded status table
    queue = Queue.Queue()
    #MAKE OUR THREADZZZ
    for i in range(max_daemons):
        t = ImgDownloader(queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    query = text("select phil.id," + db_column_name + " from phil join " + flag_table + " ON ( phil.id = " + flag_table + ".id ) where " + flag_table + ".status != '1';")
    results = db.execute(query).fetchall()
    # generate list of ids from results dict
    ids = map((lambda tuple: tuple[0]), results)
    print ids
    #bootstrap our file structure for our download
    make_directories(ids, root_dir)
    #enqueue all the results
    map((lambda id_url_tuple:queue.put(id_url_tuple)), results)

    #wait on the queue until everything has been processed     
    queue.join()
        

def test():
    get_images(LORES_IMG_DIR, 'url_to_lores_img', 'lores_status')
    #get_images(HIRES_IMG_DIR, 'url_to_hires_img')


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
    current = start
    try:
        cookiejar = get_me_a_cookie()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print "ERROR: WE COULDN'T EVEN GET A COOKIE"
        traceback.print_exc()
        return None
    failed_indices = []
    while current <= end:
        print "STARTING: " + str(current)
        try:
            # 1: fetching html of id, for store and parse
            html = cdc_phil_scrape(current, cookiejar)
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print "ERROR: couldn't scrape out html for id " + str(current)
            failed_indices.append(current)
            traceback.print_exc()
            current+=1
            continue
        # if we didn't get a session error page:
        if not is_session_expired_page(html):
            try:
                # 2: write html to disk
                store_raw_html(current, html)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't store raw html for id " + str(current)
                failed_indices.append(current)
                current+=1
                continue
            try:
                # 3: parse the metadata out of their html
                metadata = parse_img(html)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't parse raw html for id " + str(current)
                failed_indices.append(current)
                traceback.print_exc()
                current+=1
                continue
            try:
                store_datum(metadata)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't store metadata for id " + str(current)
                failed_indices.append(current)
                traceback.print_exc()
                current+=1
                continue
            # These lines will only run if everthing went according to plan
            print "SUCCESS: everything went according to plan for id " + str(current)
            current+=1
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


def check_start(start, end):
    if start < end:
        print "choosing a higher end than start, range fail"
    else:
        break

def check_latest(start):
    check_start(start)
    query = text("select id from phil order by id desc limit 1;")
    results = int(table.execute(query).fetchall())
    if results > start:
        return results
    else:
        return start


if __name__ == '__main__':
    bootstrap_filestructure()
    #cdc_phil_scrape_range(1, 11850)
    test()
