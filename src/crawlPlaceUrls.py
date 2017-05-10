import crawl
from crawlCountryUrls import readCountryUrls
from crawlCountry import crawlAllPlaces
from saveFile import saveJson, readJson

def savePlaceUrls():
	urls = readCountryUrls(type = "dict")
	countries = {}
	for item in urls.items():
		countryName = item[0]
		countryUrl = crawl.baseUrl + item[1]
		places = {}
		# print("=========== Crawling places for the country %s ===========" % countryName)
		try:
			places = crawlAllPlaces(countryUrl, countryName)
		except:
			print("Something wrong when crawling places for the country %s" % countryName)
		else:
			print("Successfully crawled places for the country %s" % countryName)
		countries[countryName] = places
		# print(places)
		print("Countries Crawled: %d" % len(countries))
	saveJson("../url/placeUrls.json", countries)

def readPlaceUrls(type = "list"):
	if(type == "list"):
		urls = []
		countries = readJson("../url/placeUrls.json")
		for country in countries.items():
			places = country[1]
			for place in places.items():
				urls.append(place[1])
	elif(type == "dict"):
		urls = readJson("../url/placeUrls.json")
	else:
		print("Parameter type invalid: \"list\" for list format and \"dict\" for dict format")
		return
	return urls