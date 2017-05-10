import crawl
from saveFile import saveJson, readJson

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
	countryAs = soup.find_all("a", class_="card--list")

	# find all urls for single country, return urls with the country name
	countries = {}
	for country in countryAs:
		url = country["href"]
		name = country.h3.text.replace('\n','').replace(' ','-')
		# print("%s: %s" % (name, url))
		# urls.append(url)
		countries[name] = url
	return countries

def saveCountryUrls():
	countries = getCountryUrls()
	saveJson("../url/countryUrls.json", countries)

def readCountryUrls(type = "list"):
	if(type == "list"):
		urls = []
		countries = readJson("../url/countryUrls.json")
		for item in countries.items():
			urls.append(item[1])
	elif(type == "dict"):
		urls = readJson("../url/countryUrls.json")
	else:
		print("Parameter type invalid: \"list\" for list format and \"dict\" for dict format")
		return
	return urls
