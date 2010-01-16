import urllib
import os.path
import sys
import traceback
#import urllib2
from scraper import *
from data_storer import *
from parser import *


# store the hires images relative to the working directory
HIRES_IMG_DIR = 'cdc-phil-imgs-hires'
RAW_HTML_DIR = 'cdc-phil-raw-html'

def mkdir(dirname):
    if not os.path.isdir("./" + dirname + "/"):
        os.mkdir("./" + dirname + "/")

# run this before downloading hires images
def bootstrap_filestructure():
    mkdir(HIRES_IMG_DIR)
    mkdir(RAW_HTML_DIR)    

# FIXME: in these two functions, mkdir is run, which checks whether or not a dir exists.  this is inefficient.
# because we will run this function once for every single image.  easier to ie make all the directories, then assume they exist?
# or maybe we should just leave it.
# (note that running mkdir only creates the dir if it doesnt already exist)

def floorify(id):
    return id % 100

def make_directories(ids):
    floors = map(floorify, ids)
    floors_unique = set(floors)
    # convert the floors into strings of format like 015XX
    floor_dirs = map((lambda dir: str(dir).zfill(5)[0:3]+"XX"), floors_unique)
    map((lambda dirname: mkdir(HIRES_IMG_DIR + dirname)), floor_dirs)

def get_images():
    query = text("select id,url_to_hires_img from phil where url_to_hires_img != '';")
    results = db.execute(query).fetchall()
    for id_url_tuple in results:
        id = id_url_tuple[0]
        url = id_url_tuple[1]
        dl_image(id, url, HIRES_IMG_DIR)
        path = './' + HIRES_IMG_DIR + id
        urllib.urlretrieve(url, asdf)

def store_raw_html(id, html):
    idstr = str(id).zfill(5)
    floor = id - (id%100)
    ceiling = str(floor + 100).zfill(5)
    floor = str(floor).zfill(5)
    mkdir(RAW_HTML_DIR + '/' + floor + '-' + ceiling)
    fp = open(RAW_HTML_DIR + '/' + floor + '-' + ceiling + '/' + idstr + '.html', 'w')
    fp.write(html)
    fp.close()


def store_datum(dict):
    table.execute(dict)

#def dl_all_hires_imgs():
#    #TODO: write this function (the next line is pseudocode)    
#    # FIXME: ok, this /pretty much/ works, but I think I want two loops, 
#    # for different folders and a lot of error handling for big files
#    for img_path in session.query(Phil).filter("id<224").order_by("id").all():
#        dl_hires_img(imgMetadata['path_to_img'], imgMetadata['id'])



def cdc_phil_scrape_range(start, end):
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
    #let them know that we're starting our work on a new item
        print "STARTING: " + str(current)
        try:
            #1: get the html from their server
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
                #2: store their html on our server
                store_raw_html(current, html)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't store raw html for id " + str(current)
                failed_indices.append(current)
                current+=1
                continue
            try:
                #3: parse the metadata out of their html
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
                #4: store the metadata in our database
                store_datum(metadata)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print "ERROR: couldn't store metadata for id " + str(current)
                failed_indices.append(current)
                traceback.print_exc()
                current+=1
                continue
            #these lines will only run if everthing went according to plan
            print "SUCCESS: everything went according to plan for id " + str(current)
            current+=1
        # if we got a session error page
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
                #we were successful
                print "SESSION success. got a new cookie."
                break

    print "HOLY CRAP WE ARE DONE"
    if not len(failed_indices) == 0:
        print "Failed at " + str(len(failed_indices)) + " indices :"
        print failed_indices


def get_last():
    cookiejar = get_me_a_cookie()
    
    print stuff
    return last

#def check_start(start, end):
#    if start < end:
#        print "choosing a higher end than start, range fail"
#    else:
#        continue

def check_latest(start):
    check_start
    query = text("select id from phil order by id desc limit 1;")
    results = int(table.execute(query).fetchall())
    if results > start:
        return results
    else:
        return start


if __name__ == '__main__':
    bootstrap_filestructure()
    #cdc_phil_scrape_range(1900, 1999)

    cdc_phil_scrape_range(1, 1)
    #test_scrape()
