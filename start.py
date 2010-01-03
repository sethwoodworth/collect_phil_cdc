from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
from scraper import *
from data_storer import *
from parser import *


#where we will store the hires images
#relative to the pwd, no trailing slash
HIRES_IMG_DIR = 'cdc-phil-imgs-hires'
RAW_HTML_DIR = 'cdc-phil-raw-html'

def mkdir(dirname):
	if not os.path.isdir("./" + dirname + "/"):
		os.mkdir("./" + dirname + "/")

# run this before downloading hires images
def bootstrap_filestructure():
	mkdir(HIRES_IMG_DIR)
	mkdir(RAW_HTML_DIR)	

def dl_hires_img(hires_img_url, img_id):
	#TODO: group them in folders of 100
	urllib.urlretrieve(hires_img_url, HIRES_IMG_DIR + '/' + img_id + '.tif')

def store_raw_html(id, html):
	#TODO: group them in folders of 100
	fp = open(RAW_HTML_DIR + '/' + str(id), 'w')
	fp.write(html)

#def dl_all_hires_imgs():
#	#TODO: write this function (the next line is pseudocode)	
#	for every item in the database as imgMetadata
#		dl_hires_img(imgMetadata['path_to_img'], imgMetadata['id'])


# downloads a single image page, parses it, and shoves its data in the database
def scrape_and_parse(id):
	try:
		html = cdc_phil_scrape(id)
		metadata = parse_img(html)
		# TODO: here, we shove the metadata in the database
		# print metadata
	except:
		return FALSE



def cdc_phil_scrape_range(start, end):
	current = start
	cookiejar = get_me_a_cookie()
	while current <= end:
		html = cdc_phil_scrape(current, cookiejar)
		# if we didn't get a session error page:
		if not is_session_expired_page(html):
			store_raw_html(current, html)
			#TODO: other stuff with the raw html (parse it, etc)
			current+=1
		# if we got a session error page:
		else:
			print "got a session error page.  going to grab a new cookie..."
			cookiejar = get_me_a_cookie()
			

def store_datum(dict):
    table.execute(dict)
    phil_table.commit()

def test_scrape():
    html = cdc_phil_scrape(1)
    metadata = parse_img(html)
    #print metadata[:10]
    store_datum(metadata)

    
if __name__ == '__main__':
	#cdc_phil_scrape_range(113, 123)
	test_scrape()




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
