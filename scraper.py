from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import os.path
import cookielib


def cdc_phil_scrape(id):
	url_to_scrape = 'http://phil.cdc.gov/phil/details.asp';
	# this post data doesn't seem to really matter, as long as it is correctly formed
	image_page_post_values = {'count':	'1',
		'displaymode':	'1',
		'formaction':	'',
		'imagelist':	id,
		'imagesperpage':	'15',
		'keywords':	'',
		'mypictures':	'',
		'page':	'1',
		'pages':	'1',
		'philid':	id,
		'previouskeywords':	'',
		'referingpagetag':	'',
		'referingpageurl':	'',
		'returnpage':	'quicksearch.asp',
		'searchtype':	'all',
	}
	quicksearch_page_post_values = {
		'formaction':	'SEARCH',
		'illustrations':	'on',
		'keywords':	'liver',
		'keywordstext':	'liver',
		'photos':	'on',
		'searchtype':	'photo|illustration|video',
		'video':	'on',
	}

	urlopen = urllib2.urlopen
	Request = urllib2.Request
	cj = cookielib.LWPCookieJar()
	# This is a subclass of FileCookieJar
	# that has useful load and save methods

	# FIXME: this probably isn't necessary. commenting out for now

	#COOKIEFILE = 'cookies.lwp'
	## the path and filename to save your cookies in
	#if os.path.isfile(COOKIEFILE):
	## if we have a cookie file already saved
	## then load the cookies into the Cookie Jar
	#	cj.load(COOKIEFILE)

	# Now we need to get our Cookie Jar
	# installed in the opener;
	# for fetching URLs
	# we get the HTTPCookieProcessor
	# and install the opener in urllib2
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)



	# fake a user agent, some websites (like google) don't like automated exploration
	txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

	# we have to step through the landing page and the search results pages in order to access an individual image's page
	# otherwise the site gives us session errors
	# so we go ahead and do that, picking up the necessary cookies along the way
	req = Request('http://phil.cdc.gov/phil/home.asp', None, txheaders)
	#cj.save(COOKIEFILE)                     # save the cookies 
	handle = urlopen(req)
	req = Request('http://phil.cdc.gov/phil/quicksearch.asp', urllib.urlencode(quicksearch_page_post_values), txheaders)
	#cj.save(COOKIEFILE)                     # save the cookies again
	handle = urlopen(req)

	# finally, we can grab the actual image's page
	req = Request(url_to_scrape, urllib.urlencode(image_page_post_values), txheaders)
	handle = urlopen(req)

	return handle.read() #returns the page



if __name__ == '__main__':
	print cdc_phil_scrape(11436)
