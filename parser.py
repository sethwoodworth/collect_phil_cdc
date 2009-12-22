import re
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
        print rowContents
    desc = str(rows[0]('td')[1]) #FIXME: i'm just flattening the html here
    # it's just p and b tags, i think.
    # we skip row 1 because it just has a link to the hi-res img
    provider = rows[2]('td')[1].string
    print provider
    creation = rows[3]('td')[1].string #TODO: turn this into a datetime
    credit = rows[4]('td')[1].string 
    #we skip row 5, which is "links"
    categories = str(rows[6]('td')[1]) #same as with desc, except the html is much more complicated.  we should probably parse this more carefully.
    # TODO: the rest of the parsing

    # before we return the dict of data,
    # download the hires image
    # grabbing the lores image url
    # note that we have to go to the original soup that we were passed in order to do this
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

