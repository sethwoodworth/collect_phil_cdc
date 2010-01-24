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

import string
import urllib
import urllib2
import cookielib
from scraper import *
import re

def searchtype_query(searchtype, cj):
    # searchtype can be one of [ "video", "photo", "illustration" ]
	url_to_scrape = 'http://phil.cdc.gov/phil/quicksearch.asp'
	image_page_post_values = {'count':	'1',
		'keywords':	' ',
		'formaction':	'SEARCH',
		'searchtype':	searchtype,
		'imagesperpage':	'0',
		'page':	'1',
		'pages':	'1',
		'previouskeywords':	'',
		'referingpagetag':	'',
		'referingpageurl':	'',
		'returnpage':	'quicksearch.asp',
	}

	urlopen = urllib2.urlopen
	Request = urllib2.Request

	# Now we need to get our Cookie Jar
	# installed in the opener;
	# for fetching URLs
	# we get the HTTPCookieProcessor
	# and install the opener in urllib2
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)



	# fake a user agent, some websites (like google) don't like automated exploration
	txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

	# finally, we can grab the actual image's page
	req = Request(url_to_scrape, urllib.urlencode(image_page_post_values), txheaders)
	handle = urlopen(req)

	html = handle.read() #returns the page
	return re.split('\|', max(re.split(' ', html), key=len)[7:-1])
    
	# returns list containing all illustration numbers
	# splits html into a list by spaces, pulls the longest word,
    # drops the first eight and the last one charecters, and splits it into a list by pipe
	

if __name__ == '__main__':
	searchtype_query('illustration', get_me_a_cookie())
