from crawlCountryUrls import readCountryUrls
from crawl import baseUrl
from crawlCountry import crawlCountry
from saveFile import saveJson

urls = readCountryUrls()
for url in urls:
	countryUrl = baseUrl + url
	try:
		country = crawlCountry(countryUrl)
		saveJson("../data/countries.json", country)
	except:
		print("Something wrong when crawling the country %s" % countryUrl)
		continue
