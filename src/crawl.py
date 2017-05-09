import urllib.request
from urllib.error import URLError, HTTPError
from socket import timeout
from bs4 import BeautifulSoup
from config import headers

'''
Start from the homepage
	crawl all urls for a single country page, store the urls in a list
crawl countries: 
	crawl information for each single country using the url stored
	crawl all urls for a single city page in the country, store the urls in a list
crawl cities:
	crawl information for each single city in a country using the url stored
	crawl all urls for a single attraction page in the country, store the url in a list
crawl attractions:
	crawl information for each single attraction in a city using the url stored

'''	

baseUrl = "https://www.lonelyplanet.com"
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"}
timeout = 20

def getBS(url):
	request = urllib.request.Request(url, None, headers)
	try:
		response = urllib.request.urlopen(request, None, timeout)
	except (URLError, HTTPError) as e:
		print("Something Wrong Happened: ", e)
		return
	except timeout:
		print("Timeout at the page: %s" % url)
		return
	else:
		print("Successfully access the page: %s" % url)
		content = response.read().decode("utf-8")
		soup = BeautifulSoup(content)
		return soup