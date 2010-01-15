import re
import data_storer
import time
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from html5lib import HTMLParser, treebuilders



def parse_img(html):
    # declare default values
    #t_id = 0
    path_to_img = ''
    desc = ''
    categories = ''
    credit = ''
    provider = ''
    source = ''
    is_color = 'True'
    creation = None
    #upload
    copyright = ''
    access_time = datetime.today() #time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    # soupify the html
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    block = soup.find(cellpadding="5") # isolate the table of data with the unique cellpadding

    # features
    t_id = block.find('tr')('td')[1].string # grab the image id
    # shove all the rest of the rows of data into a list, organized by row
    # we do this so that we can be sure that each item in the list is a row in our table of data
    # otherwise, rows within tables that are nested within our data table (these /do/ exist) would be given separate indices in our list
    # i knows, this isn't pretty.  feel free to make it prettier --parker
    # note that row[0] is the second tr in the table
    rowsOfData = block.find('tr').findNextSiblings('tr')
    # delete the last item (row) in this list. it's a checkbox to "add to favorites."
    # it breaks the parser
    del rowsOfData[len(rowsOfData)-1]

    # now we loop through the rows, slurping out the info as we go
    for rowContents in rowsOfData:
	try:
		# grab the bolded text in the first column.  this is the field name
		fieldName = rowContents('td')[0]('b')[0].string
		try:
			# grab the text (note, there may be markup here) in the second column.  this is the field value
			fieldValue = rowContents('td')[1]
			if fieldName == 'Description:':
				#FIXME: i'm just flattening the html here
				# it's just p and b tags, i think.
				desc = str(fieldValue)
			elif fieldName == 'Content Providers(s):':
				provider = fieldValue.string
			elif fieldName == 'Creation Date:':
				#TODO: turn this into a datetime
				creation = datetime.strptime(fieldValue.string, "%Y")
			elif fieldName == 'Photo Credit:':
				credit = fieldValue.string
			#elif fieldName == 'Links:':
			#	links = fieldValue.string
			elif fieldName == 'Categories:':
				# FIXME: same as with description, except the html is more complicated.
				# it's probably much more important that we parse this part more carefully.  at the least, we should strip out the javascript.
				categories = str(fieldValue)
			#TODO: store copyright info in the database
			elif fieldName == 'Copyright Restrictions:':
				copyright = fieldValue.string
		except:
			print "error parsing table row. we were expecting two cells: one field with a bolded name and one field with data. rowContents were: "

			print rowContents

	except:
		print "error parsing table row. we were expecting two cells: one field with a bolded name and one field with data. rowContents were: "
		print rowContents

    # before we return the dict of data,
    # generate the hires img url
    # grabbing the lores image url:
    # note that we have to go to the original soup that we were passed in order to do this
    lores_img_url = soup("h2")[0].parent("img")[0]['src']
    # the hires img url is a simple substitution from there
    path_to_img = re.sub('_lores.jpg', '.tif', lores_img_url)
    #print t_id
    #return Phil(t_id, desc, categories, credit, provider, source, path_to_img, is_color, creation, access_time)

    return {
        'id': t_id,
        'desc': desc,
        'categories': categories,
        'credit': credit,
        'provider': provider,
        'source': source,
        'path_to_img': path_to_img,
        'is_color': is_color,
        'creation': creation,
        'access_time': access_time,
    }
    
def test_parse():
    f = open('./examples/5423.html')
    raw_html = f.read()
    print parse_img(raw_html)

if __name__ == '__main__':
	test_parse()
