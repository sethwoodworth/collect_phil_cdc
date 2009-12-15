from BeautifulSoup import BeautifulSoup
import re
import urllib
import urllib2
from scraper import *
from sqlalchemy import *

db = create_engine('sqlite:///phil.cdc.sql')

db.echo = True
metadata = MetaData(db)

phil = Table('phil', metadata,
    Column('id', Integer, primary_key=True),
    Column('desc', String),         # Description - Extensive and authoritative explanation of the visual image or video file
    Column('categories', String),   # Categories - used to describe the image
    Column('credit', String),       # Photo Credit - Photographer or Videographer who took the photo or shot the video
    Column('provider', String),      # Content Provider - The contributor of the asset
    Column('source', String),       # Source Library - Where the image originated
    Column('path_to_img', String),  # seth: static url to hi-res images
    Column('is_color', Boolean),    # Color Scheme - Color or Black & White
    Column('creation', DateTime),   # Creation Date - When the object was created (photo taken, video shot, etc.)
    Column('upload', DateTime),     # Upload Date - When the image entered the PHIL database
    Column('access_time', DateTime) # seth: time/day we accessed the content
)
metadata.create_all(db)


#dict = {'id': '', }

#def store_dict(dict):


#where we will store the hires images
#relative to the pwd, no trailing slash
HIRES_IMG_DIR = 'cdc-phil-imgs-hires'

def mkdir(dirname):
	if not os.path.isdir("./" + dirname + "/"):
		os.mkdir("./" + dirname + "/")

mkdir(HIRES_IMG_DIR)

def dl_hires_img(hires_img_url, img_id):
	urllib.urlretrieve(hires_img_url, HIRES_IMG_DIR + '/' + img_id + '.tif')

def parse_img(soup):
    # <table width="700" bgcolor="black" border="0" cellpadding="5" cellspacing="1">
    # isolate the table of data 
    block = soup.find(cellpadding="5")
    # grab the image id
    t_id = block.find('tr')('td')[1].string
    # shove all the rest of the rows of data into a list, organized by row
    # i knows, this isn't pretty.  feel free to make it prettier --parker
    # this means that row[0] is the second tr in the table
    rows = block.find('tr').findNextSiblings('tr')
    desc = str(rows[0]('td')[1]) #FIXME: i'm just flattening the html here
    # it's just p and b tags, i think.
    #we skip row 1 because it just has a link to the hi-res img
    provider = rows[2]('td')[1].string
    creation = rows[3]('td')[1].string #TODO: turn this into a datetime
    credit = rows[4]('td')[1].string 
    #we skip row 5, which is "links"
    categories = str(rows[6]('td')[1]) #same as with desc, except the html is much more complicated.  we should probably parse this more carefully.
    # TODO: the rest of the parsing

    # before we return the dict of data,
    # download the hires image
    # grabbing the lores image url
    lores_img_url = soup("h2")[0].parent("img")[0]['src']
    # the hires img url is a simple substitution from there
    path_to_img = re.sub('_lores.jpg', '.tif', lores_img_url)
    #FIXME: we can do this now, or we can do it later.  either way
    #dl_hires_img(path_to_img, t_id)
    print t_id
    return {
        'id': t_id,
        'path_to_img': path_to_img,
        'desc': desc,
        'categories': categories,
        'credit': credit,
        'provider': provider,
        #'source': source,
        #'is_color': is_color,
        'creation': creation,
        #'upload': upload,
        #'access_time': access_time,
    }
            
    
def test_parse():
    f = open('5423.html')
    raw_html = f.read()
    htmlSoup = BeautifulSoup(raw_html)
    parse_img(htmlSoup)

#just run through this for each image on the site. boom.
def cdc_phil_scrape_and_store(id):
	soup = cdc_phil_scrape(id)
	metadata = parse_img(soup)

cdc_phil_scrape_and_store(1)
