import re
import time
from datetime import datetime
from BeautifulSoup import BeautifulSoup
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
        'creation': '',
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
                    #make a list of tuples
                    links_tuple_list = []
                    links_rows = fieldValue.findAll('tr')
                    for link_row_html in links_rows: 
                        desc = link_row_html('td')[1].find('a').contents[0]
                        url = link_row_html('td')[1].find('a')['href']
                        links_tuple_list.append((desc,url))
                    #stringify it
                    links_tuple_list_string = str(links_tuple_list)
                elif fieldName == 'Categories:':
                    # FIXME: same as with description, except the html is more complicated.
                    # it's probably much more important that we parse this part more carefully.  at the least, we should strip out the javascript.
                    categories = str(fieldValue)
                #TODO: store copyright info in the database
                elif fieldName == 'Copyright Restrictions:':
                    copyright = fieldValue.contents[0]
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
    lores_img_url = soup("h2")[0].parent("img")[0]['src']
    # the hires img url is a simple substitution from there
    hires_img_url = re.sub('_lores.jpg', '.tif', lores_img_url)
    return {
        'id': t_id,
        'desc': desc,
        'categories': categories,
        'credit': credit,
        #'links': links,
        'provider': provider,
        'source': source,
        'copyright': copyright,
        'creation': creation,
        'access_time': access_time,
    }
    return metadict
    
def test_parse():
    f = open('./examples/10760.html')
    raw_html = f.read()
    #print parse_img(raw_html)
    parse_img(raw_html)
    f.close()

if __name__ == '__main__':
	test_parse()
