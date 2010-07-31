################################################################################
################################################################################
#####################                                  #########################
#####################         Release Our Data         #########################
#####################                                  #########################
#####################       a HelloSilo Project        #########################
#####################       <ROD@hellosilo.com>        #########################
################################################################################
##                                                                            ##  
##     Copyright 2010                                                         ##
##                                                                            ##  
##         Parker Phinney   @gameguy43   <parker@madebyparker.com>            ##
##         Seth Woodworth   @sethish     <seth@sethish.com>                   ##
##                                                                            ##
##                                                                            ##
##     Licensed under the GPLv3 or later,                                     ##
##     see PERMISSION for copying permission                                  ##
##     and COPYING for the GPL License                                        ##
##                                                                            ##
################################################################################
################################################################################

import re
import time
from datetime import datetime
#from BeautifulSoup import BeautifulSoup
from html5lib import HTMLParser, treebuilders
import traceback
import json
import yaml

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
        'url_to_thumb_img':  '',
        'copyright': '',
        'creation': None,
        'access_time': datetime.today()
    }
    return metadict


def get_first_result_index_from_quick_search_results(html):
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    block = soup.find(border="0", bgcolor="white") # isolate the table of data on the first result
    id_str = block.find('font').contents[0] #contents of first <font>
    # this should looke like: 'ID#:11901'
    # parse out the actual id and cast as int
    id = int(id_str.partition(':')[2])
    print id
    return id


def parse_quick_search(html):
    return html

def remove_surrounding_td_tags(str):
    # get the first one
    str = str.split("<td>")[1]
    split = str.split("</td>")
    str = split[len(split)-2]
    return str

def encode_all_nice(fieldvalue):
#    return unicode(remove_surrounding_td_tags(repr(str(fieldValue))))
    #return str(fieldvalue.encode("utf-8"))
    return unicode(fieldvalue)

def parse_img(html):
    metadict = init_dict()
    # soupify the html
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
    soup = parser.parse(html)
    #soup = BeautifulSoup(html)
    block = soup.find(cellpadding="5") # isolate the table of data with the unique cellpadding

    # navigate the block tree, find elements, and store them in the dict
    metadict['id'] = block.find('tr')('td')[1].contents[0] # grab the unique image id
    metadict['url_to_lores_img'] = soup("h2")[0].parent("img")[0]['src']
    metadict['url_to_thumb_img'] = re.sub('_lores.jpg', '_thumb.jpg', metadict['url_to_lores_img'])

    # shove all the rest of the rows of data into a list, organized by row
    # we do this so that we can be sure that each item in the list is a row in our table of data
    # otherwise, rows within tables that are nested within our data table 
    # (these /do/ exist) would be given separate indices in our list
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
                        metadict['desc'] = remove_surrounding_td_tags(encode_all_nice(fieldValue))
                elif fieldName == 'Content Providers(s):':
                    if fieldValue.contents:
                        metadict['provider'] = encode_all_nice(fieldValue.contents[0])
                elif fieldName == 'Creation Date:':
                    if fieldValue.contents:
                        metadict['creation'] = encode_all_nice(fieldValue.contents[0])
                elif fieldName == 'Photo Credit:':
                    if fieldValue.contents:
                        metadict['credit'] = encode_all_nice(fieldValue.contents[0])
                elif fieldName == 'High Resolution:':   
                    if fieldValue('a'):
                        metadict['url_to_hires_img'] = re.sub('_lores.jpg', '.tif', metadict['url_to_lores_img'])
                elif fieldName == 'Links:':
                    if fieldValue.contents:
                        #make a list of tuples
                        links_tuple_list = []
                        links_rows = fieldValue.findAll('tr')
                        for link_row_html in links_rows: 
                            desc = link_row_html('td')[1].find('a').contents[0]
                            url = link_row_html('td')[1].find('a')['href']
                            links_tuple_list.append((desc,url))
                        #jsonify it
                        metadict['links'] = encode_all_nice(json.dumps(links_tuple_list))
                elif fieldName == 'Categories:':
                    if fieldValue.contents:
                        tag_str = ''
                        metatags = fieldValue.find('table').findNextSiblings('table')
                        metatags.insert(0, fieldValue.find('table'))
                        for metatag in metatags:
                            metatag_name = metatag.find('td').contents[0]
                            tag_str = tag_str + "\n" + metatag_name + ":"
                            rows = metatag.findAll('table')
                            for row in rows:
                                cells = row.findAll('td')
                                indentation = len(cells) - 1
                                tagname = cells[len(cells)-1].find('a').contents[0]
                                tag_str = tag_str + "\n" +  " "*indentation + tagname + ":"
                        yamlized = yaml.safe_load(tag_str) # gets us a dict
                        metadict['categories'] = encode_all_nice(json.dumps(yamlized))

                elif fieldName == 'Copyright Restrictions:':
                    if fieldValue.contents:
                        metadict['copyright'] = encode_all_nice(fieldValue)
            except:
                print "Error parsing table row contents." 
                print "Expecting two cells: one field with a bolded name and one field with data. rowContents were: "
                print encode_all_nice(rowContents)
                traceback.print_exc()

        except:
            print "Error parsing table row."
            print "Expecting two cells: one field with a bolded name and one field with data. rowContents were: "
            print repr(str(rowContents))
            traceback.print_exc()

    return metadict
    
def test_parse():
    f = open('./examples/94.html')
    raw_html = f.read()
    print repr(parse_img(raw_html))
    f.close()

if __name__ == '__main__':
	test_parse()
