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

def dl_hires_img(hires_img_url, img_id):
	urllib.urlretrieve(hires_img_url, HIRES_IMG_DIR + '/' + img_id + '.tif')

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


def scrape_and_parse_everything():
	id=1
	while True:
		try:
			scrape_and_parse(id)
			id+=1
		except:
			break


def scrape_everything():
	id=1
	mkdir(RAW_HTML_DIR)	
	#while True:
	while id <= 10:
		try:
			html = cdc_phil_scrape(id)
			fp = open(RAW_HTML_DIR + '/' + id, 'w')
			fp.write(html)
			id+=1
		except:
			break

def test_scrape():
	html = cdc_phil_scrape(1)
	metadata = parse_img(html)
    metadata
	#print metadata[:10]
    table.execute(metadata)
    table.commit()
    
if __name__ == '__main__':
	test_scrape()
