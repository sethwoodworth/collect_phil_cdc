import re
import data_storer
from BeautifulSoup import BeautifulSoup



def parse_img(soup):
    # <table width="700" bgcolor="black" border="0" cellpadding="5" cellspacing="1">
    # isolate the table of data 
    block = soup.find(cellpadding="5")
    # grab the image id
    t_id = block.find('tr')('td')[1].string
    # shove all the rest of the rows of data into a list, organized by row
    # i knows, this isn't pretty.  feel free to make it prettier --parker
    # this means that row[0] is the second tr in the table
    # TODO: better name here
    rows = block.find('tr').findNextSiblings('tr')

    # now we loop through the rows, slurping out the info as we go
    for rowContents in rows:
	try:
		fieldName = rowContents('td')[0]('b')[0].string
		try:
			fieldValue = rowContents('td')[1]
			if fieldName == 'Description:':
				#FIXME: i'm just flattening the html here
				# it's just p and b tags, i think.
				desc = str(fieldValue)
			elif fieldName == 'Content Providers(s):':
				provider = fieldValue.string
			elif fieldName == 'Creation Date:':
				#TODO: turn this into a datetime
				creation = fieldValue.string
			elif fieldName == 'Photo Credit:':
				credit = fieldValue.string
			#elif fieldName == 'Links:':
			#	links = fieldValue.string
			elif fieldName == 'Categories:':
				# FIXME: same as with description, except the html is more complicated.
				# we should probably parse this more carefully
				categories = str(fieldValue)
			#elif fieldName == 'Copyright Restrictions:':
			#	copyright = fieldValue.string
		except:
			print "error parsing the field's value"

	except:
		print "well, that one didn't work"

    # before we return the dict of data,
    # download the hires image
    # grabbing the lores image url:
    # note that we have to go to the original soup that we were passed in order to do this
    lores_img_url = soup("h2")[0].parent("img")[0]['src']
    # the hires img url is a simple substitution from there
    path_to_img = re.sub('_lores.jpg', '.tif', lores_img_url)
    #FIXME: we can do this now, or we can do it later.  either way
    #dl_hires_img(path_to_img, t_id)
    print t_id
    return Phil(t_id, desc, categories, credit, provider, source, path_to_img, is_color, creation, access_time)

    #return {
    #    'id': t_id,
    #    'path_to_img': path_to_img,
    #    'desc': desc,
    #    'categories': categories,
    #    'credit': credit,
    #    'provider': provider,
    #    #'source': source,
    #    #'is_color': is_color,
    #    'creation': creation,
    #    #'upload': upload,
    #    #'access_time': access_time,
    #}
    
def test_parse():
    f = open('./examples/5423.html')
    raw_html = f.read()
    htmlSoup = BeautifulSoup(raw_html)
    print parse_img(htmlSoup)

if __name__ == '__main__':
	test_parse()
