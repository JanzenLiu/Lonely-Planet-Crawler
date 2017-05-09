import urllib.request
import urllib.error
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
	except (urllib.error.URLError, urllib.error.HTTPError) as e:
		print("Something Wrong Happened: ", e)
		return
	else:
		content = response.read().decode("utf-8")
		soup = BeautifulSoup(content)
		return soup