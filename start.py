import urllib
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


def store_datum(dict):
    table.execute(dict)
    #phil_table.commit()

#def dl_all_hires_imgs():
#    #TODO: write this function (the next line is pseudocode)    
#    for every item in the database as imgMetadata
#        dl_hires_img(imgMetadata['path_to_img'], imgMetadata['id'])



def cdc_phil_scrape_range(start, end):
    current = start
    cookiejar = get_me_a_cookie()
    while current <= end:
        print str(current)
        html = cdc_phil_scrape(current, cookiejar)
	    #print html
        # if we didn't get a session error page:
        if not is_session_expired_page(html):
            store_raw_html(current, html)
            metadata = parse_img(html)
            store_datum(metadata)
            current+=1
        # if we got a session error page
        else:
            print "Session error. Need a new cookie..."
            cookiejar = get_me_a_cookie()





# downloads a single image page, parses it, and shoves its data in the database
def scrape_and_parse(id):
    try:
        html = cdc_phil_scrape(id)
        metadata = parse_img(html)
        store_datum(metadata)
        # print metadata
    except:
        return FALSE


def test_scrape():
    html = cdc_phil_scrape(1)
    metadata = parse_img(html)
    #print metadata[:10]
    store_datum(metadata)

    
if __name__ == '__main__':
    bootstrap_filestructure()
    cdc_phil_scrape_range(1, 5)
    #test_scrape()
