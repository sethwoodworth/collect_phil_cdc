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
#TODO: the same zfill stuff we did in store_raw_html
def dl_hires_img(hires_img_url, img_id):
    floor = id - (id%100)
    ceiling = str(floor + 100)
    floor = str(floor)
    mkdir(HIRES_IMG_DIR + '/' + floor + '-' + ceiling)
    urllib.urlretrieve(hires_img_url, HIRES_IMG_DIR + '/' + floor + '-' + ceiling + '/' + img_id + '.tif')

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


# i gave up on this..  it's messy because you also want to keep track of "current"
# might come back to this later.  for now, fuckit
#def try_me(func, args, error_msg):
#    try:
#        retval = func(*args)
#    except:
#        
#    pass


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
    print "Failed at " + str(len(failed_indices)) + " indices :"
    print failed_indices


# downloads a single image page, parses it, and shoves its data in the database
def scrape_and_parse(id):
    try:
        html = cdc_phil_scrape(id)
        metadata = parse_img(html)
        store_datum(metadata)
        # print metadata
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        return FALSE


def test_scrape():
    html = cdc_phil_scrape(1)
    metadata = parse_img(html)
    #print metadata[:10]
    store_datum(metadata)

    
if __name__ == '__main__':
    bootstrap_filestructure()
    try:
        cdc_phil_scrape_range(500, 530)
    except KeyboardInterrupt:
        sys.exit(0)
    #cdc_phil_scrape_range(1, 11850)
    #test_scrape()
