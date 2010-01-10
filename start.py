#from BeautifulSoup import BeautifulSoup
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
def dl_hires_img(hires_img_url, img_id):
	floor = id - (id%100)
	ceiling = str(floor + 100)
	floor = str(floor)
	mkdir(HIRES_IMG_DIR + '/' + floor + '--' + ceiling)
	urllib.urlretrieve(hires_img_url, HIRES_IMG_DIR + '/' + floor + '--' + ceiling + '/' + img_id + '.tif')

def store_raw_html(id, html):
	floor = id - (id%100)
	ceiling = str(floor + 100)
	floor = str(floor)
	mkdir(RAW_HTML_DIR + '/' + floor + '--' + ceiling)
	fp = open(RAW_HTML_DIR + '/' + floor + '--' + ceiling + '/' + str(id), 'w')
	fp.write(html)


def store_datum(dict):
    table.execute(dict)
    #phil_table.commit()

#def dl_all_hires_imgs():
#	#TODO: write this function (the next line is pseudocode)	
#	for every item in the database as imgMetadata
#		dl_hires_img(imgMetadata['path_to_img'], imgMetadata['id'])




def cdc_phil_scrape_range(start, end):
	current = start
	cookiejar = get_me_a_cookie()
	print "got initial cookie"
	while current <= end:
		print str(current)
		html = cdc_phil_scrape(current, cookiejar)
		# if we didn't get a session error page:
		if not is_session_expired_page(html):
			store_raw_html(current, html)
			metadata = parse_img(html)
			#FIXME: uncomment this and debug the database errors
			store_datum(metadata)
			current+=1
		# if we got a session error page:
		else:
			print "got a session error page.  going to grab a new cookie..."
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
    cdc_phil_scrape_range(73, 79)
	#test_scrape()




#these methods are deprecated because they don't cleverly keep track of cookies
#so they make many more http requests than necessary
#def scrape_and_parse_everything():
#	id=1
#	while True:
#		try:
#			scrape_and_parse(id)
#			id+=1
#		except:
#			break
#def scrape_everything():
#	id=1
#	mkdir(RAW_HTML_DIR)	
#	#while True:
#	while id <= 10:
#		try:
#			html = cdc_phil_scrape(id)
#			#print html
#			store_raw_html(id, html)
#			id+=1
#		except:
#			print "uh-oh. trouble getting a page."
#			break
