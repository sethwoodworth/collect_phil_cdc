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
    #soup = BeautifulSoup(html)
    block = soup.find(cellpadding="5") # isolate the table of data with the unique cellpadding

    # features
    t_id = block.find('tr')('td')[1].contents[0] # grab the image id
    print t_id
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
            fieldName = rowContents('td')[0]('b')[0].contents[0]
            try:
                # grab the text (note, there may be markup here) in the second column.  this is the field value
                fieldValue = rowContents('td')[1]
                if fieldName == 'Description:':
                    #FIXME: i'm just flattening the html here
                    # it's just p and b tags, i think.
                    desc = str(fieldValue)
                elif fieldName == 'Content Providers(s):':
                    provider = fieldValue.contents[0]
                elif fieldName == 'Creation Date:':
                    #TODO: turn this into a datetime
                    creation = datetime.strptime(fieldValue.contents[0], "%Y")
                elif fieldName == 'Photo Credit:':
                    credit = fieldValue.contents[0]
                elif fieldName == 'Links:':
                    links_html = fieldValue.contents[0]
                    print links_html
                    #make a list of tuples
                    #stringify it
                elif fieldName == 'Categories:':
                    # FIXME: same as with description, except the html is more complicated.
                    # it's probably much more important that we parse this part more carefully.  at the least, we should strip out the javascript.
                    categories = str(fieldValue)
                #TODO: store copyright info in the database
                elif fieldName == 'Copyright Restrictions:':
                    copyright = fieldValue.contents[0]
            except:
                print "error parsing table row contents. we were expecting two cells: one field with a bolded name and one field with data. rowContents were: "
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
    hires_img_url = re.sub('_lores.jpg', '.tif', lores_img_url)
    return {
        'id': t_id,
        'desc': desc,
        'categories': categories,
        'credit': credit,
        'provider': provider,
        'source': source,
        #'is_color': is_color,
        'creation': creation,
        'access_time': access_time,
        'copyright': copyright,
        'lores_img_url': lores_img_url,
        'hires_img_url': hires_img_url,
    }
    
def test_parse():
    f = open('./examples/1112.html')
    raw_html = f.read()
    #print parse_img(raw_html)
    parse_img(raw_html)
    f.close()

if __name__ == '__main__':
	test_parse()
