import re
import time
from datetime import datetime
#from BeautifulSoup import BeautifulSoup
from html5lib import HTMLParser, treebuilders
import traceback

def init_dict():
    metadict = {
        'id': '',
        'desc': '',
        'categories': '',
        'credit': '',
        'links': '',
        'provider': '',
        'source': '',
        'url_to_hires_img':  '',
        'url_to_lores_img':  '',
        'copyright': '',
        'creation': None,
        'access_time': datetime.today()
    }
    return metadict

def parse_img(html):
    metadict = init_dict()
    # soupify the html
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    #soup = BeautifulSoup(html)
    block = soup.find(cellpadding="5") # isolate the table of data with the unique cellpadding

    # navigate the block tree, find elements, and store them in the dict
    metadict['id'] = block.find('tr')('td')[1].contents[0] # grab the unique image id
    print metadict['id']

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
                    if fieldValue.contents:
                        metadict['desc'] = str(fieldValue)
                elif fieldName == 'Content Providers(s):':
                    if fieldValue.contents:
                        metadict['provider'] = fieldValue.contents[0]
                elif fieldName == 'Creation Date:':
                    if fieldValue.contents:
                        metadict['creation'] = datetime.strptime(fieldValue.contents[0], "%Y")
                elif fieldName == 'Photo Credit:':
                    if fieldValue.contents:
                        metadict['credit'] = fieldValue.contents[0]
                elif fieldName == 'Links:':
                    if fieldValue.contents:
                        #make a list of tuples
                        links_tuple_list = []
                        links_rows = fieldValue.findAll('tr')
                        for link_row_html in links_rows: 
                            desc = link_row_html('td')[1].find('a').contents[0]
                            url = link_row_html('td')[1].find('a')['href']
                            links_tuple_list.append((desc,url))
                        #stringify it
                        links_tuple_list_string = str(links_tuple_list)
                        metadict['links'] = links_tuple_list_string
                elif fieldName == 'Categories:':
                    if fieldValue.contents:
                        # FIXME: same as with description, except the html is more complicated.
                        # it's probably much more important that we parse this part more carefully.  at the least, we should strip out the javascript.
                        metadict['categories'] = str(fieldValue)
                elif fieldName == 'Copyright Restrictions:':
                    if fieldValue.contents:
                        metadict['copyright'] = str(fieldValue)
            except:
                print "error parsing table row contents. we were expecting two cells: one field with a bolded name and one field with data. rowContents were: "
                print repr(rowContents)
                traceback.print_exc()

        except:
            print "error parsing table row. we were expecting two cells: one field with a bolded name and one field with data. rowContents were: "
            print repr(rowContents)
            traceback.print_exc()
    
    # before we return the dict of data,
    # generate the hires img url
    # grabbing the lores image url:
    # note that we have to go to the original soup that we were passed in order to do this
    metadict['url_to_lores_img'] = soup("h2")[0].parent("img")[0]['src']
    # the hires img url is a simple substitution from there
    metadict['url_to_hires_img'] = re.sub('_lores.jpg', '.tif', metadict['url_to_lores_img'])
    return metadict
    
def test_parse():
    f = open('./examples/10760.html')
    raw_html = f.read()
    print repr(parse_img(raw_html))
    f.close()

if __name__ == '__main__':
	test_parse()
