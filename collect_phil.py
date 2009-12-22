from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
from scraper import *
from database import *
from parser import *


#where we will store the hires images
#relative to the pwd, no trailing slash
HIRES_IMG_DIR = 'cdc-phil-imgs-hires'

def mkdir(dirname):
	if not os.path.isdir("./" + dirname + "/"):
		os.mkdir("./" + dirname + "/")

def bootstrap():
	mkdir(HIRES_IMG_DIR)
	bootstrap_db()

def dl_hires_img(hires_img_url, img_id):
	urllib.urlretrieve(hires_img_url, HIRES_IMG_DIR + '/' + img_id + '.tif')

            
#just run through this for each image on the site. boom.
def cdc_phil_scrape_and_store(id):
	bootstrap()
	soup = cdc_phil_scrape(id)
	metadata = parse_img(soup)
	print metadata
	#dl_hires_img(metadata['path_to_img'], metadata['id'])

cdc_phil_scrape_and_store(1)
