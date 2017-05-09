import crawl

''' 
To get url and name for each country under page: /places

Find all "a" element with class "card card--list media"
For each "a": extract the url for country in href attribute
	and the country name in the inner "h3" element
'''
def getCountryUrls():
	# get soup for the Places page
	placesUrl = crawl.baseUrl + "/places"
	soup = crawl.getBS(placesUrl)
	if(not soup):
		return

	# get "a" element for each page
	countries = soup.find_all("a", class_="card--list")

	# find all urls for single country, return a url list
	urls = []
	for country in countries:
		urls.append(country["href"])
	return urls