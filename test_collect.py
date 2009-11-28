from BeautifulSoup import BeautifulSoup
import re
import urllib
import urllib2

    
f = open('5423.html')
raw_html = f.read()
html = BeautifulSoup(raw_html, smartQuotesTo=None)


block = html.findAll(cellpadding="5")
