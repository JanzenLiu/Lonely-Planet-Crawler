from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from json import dumps, JSONEncoder

def makeUrl(lp, country, city, content):
	return lp + "/" + country + "/" + city + "/" + content

def tryCity(country, city):
	link = "https://www.lonelyplanet.com/" + country + "/" + city
	browser.get(link)

def getCityIntro(country, city):
	link = makeUrl("https://www.lonelyplanet.com", country, city, "introduction")
	browser.get(link)
	src = browser.page_source
	bs = BeautifulSoup(src, "lxml")
	title = bs.find("a", class_="place-title--text").text
	intros = bs.find_all("p", class_="copy--feature")
	intro = ""
	for item in intros:
		intro += item.text
		intro += "\n"
	return {"title": title, "intro": intro}

def getCityPage(country, city):
	link = "https://www.lonelyplanet.com/" + country + "/" + city
	browser.get(link)
	src = browser.page_source
	bs = BeautifulSoup(src, "lxml")
	return bs

def getCity(country, city):
	# get path of the city
	if(city[0] != '/'):
		path = country + "/" + city
	else:
		path = country + city
	print("===== Getting ", path, " =====")
	browser.set_page_load_timeout(1)
	browser.set_script_timeout(1)
	link = "https://www.lonelyplanet.com/" + path
	browser.get(link)
	src = browser.page_source
	bs = BeautifulSoup(src, "lxml")
	# get name of the city
	print("getting name...")
	if(bs.title):
		names = bs.title.text.split()[0:-3]
		name = " ".join(names)
	else:
		name = ""
	# get intro of the city
	print("getting intro...")
	introSpan = bs.find("span", class_="js-love-letter")
	if(introSpan):
		intro = introSpan.text
	else:
		intro = ""
	# get attractions of the city
	print("getting attractions")
	pois = bs.find_all("h5", class_="sights__title")
	poiList = []
	if(pois):
		for poi in pois:
			poiList.append({"name": " ".join(poi.text.split())})
	#get description of the city
	print("getting description...")
	browser.set_page_load_timeout(5)
	browser.set_script_timeout(5)
	link = "https://www.lonelyplanet.com/" + country + "/" + city + "/introduction"
	browser.get(link)
	src = browser.page_source
	bs = BeautifulSoup(src, "lxml")
	subtitlesRaw = bs.find_all("h2", class_="copy--subtitle")
	subtitles = []
	if(subtitlesRaw):
		for subtitle in subtitlesRaw:
			subtitles.append(subtitle.text)
	bodiesRaw = bs.find_all("p", class_="copy--body")
	bodies = []
	if(bodiesRaw):
		for body in bodiesRaw:
			bodies.append(body.text)
	return {"path": path, "name": name, "country": country, "intro":intro, "attractions": poiList, "description":{"subtitles":subtitles, "bodies":bodies}}

def getCitiesInCountry(country, cities):
	res = []
	for city in cities:
		info = getCity(country, city)
		res.append(info)
	return res

def saveJson(fileName, object):
	JSONEncoder().encode(object)
	with open(fileName,"a") as file:
		file.write(dumps(object, file, indent=4))

def crawlCity(country, city, fileName):
	cityObj = getCity(country, city)
	fileName = fileName + ".json"
	#saveJson(fileName, cityObj)

def crawlAll():
	for country in countries:
		for city in cities[country]:	
			try:
				crawlCity(country, city, "cities")
				# cities[country].remove(city)
			except TimeoutException:
				# browser.findElement(By.tagname("body")).sendKeys("Keys.ESCAPE")
				# browser.get("https://www.google.com")
				continue
			except WebDriverException:
				continue
		# countries.remove(country)

lp = "https://www.lonelyplanet.com"
content = "introduction"

usCities = ["new-york-city", "los-angeles", "san-francisco", "chicago", "seattle", "washington-dc", "boston", "new-orleans", "las-vegas", "miami"]
nzCities = ["auckland", "wellington"]
cnCities = ["hong-kong", "shanghai", "beijing", "tibet/lhasa", "guangdong/guangzhou", "sichuan/chengdu", "zhejiang/hangzhou", "shandong/qingdao", "shandong/taian", "shaanxi-shanxi/xian"]
jpCities = ["tokyo", "kansai/kyoto", "kansai/osaka", "kyushu/fukuoka", "central-honshu/nagoya", "kyushu/nagasaki", "hokkaido/sapporo", "hiroshima", "kansai/nara", "central-honshu/kanaz"]
bzCities = ["rio-de-janeiro", "sao-paulo", "the-northeast/salvador", "the-north/manaus", "the-northeast/recife", "the-northeast/fortaleza", "the-central-west/brasilia", "the-north/belem", "the-southeast/belo-horizonte", "the-northeast/sao-luis"]
egCities = ["cairo", "red-sea-coast/hurghada", "nile-valley/luxor", "mediterranean-coast/alexandria", "nile-valley/aswan", "sinai/dahab", "western-desert/siwa-oasis", "suez-canal/port-said", "sinai/nuweiba"]
itlCities = ["rome", "venice", "florence", "milan", "sicily", "puglia/otranto", "puglia/taranto", "puglia/trani", "puglia/alberobello", "puglia/cisternino"]
spCities = ["barcelona", "madrid", "valencia-and-murcia/valencia", "granada", "seville", "aragon-basque-country-and-navarra/bilbao", "aragon-basque-country-and-navarra/san-sebastian", "andalucia/malaga", "canary-islands/tenerife/santa-cruz-de-tenerife", "andalucia/cordoba"]
frCities = ["paris", "nice", "provence/marseille", "burgundy-and-the-rhone/lyon", "provence/avignon", "southwestern-france/bordeaux", "cote-dazur/cannes", "alsace-and-lorraine/strasbourg", "provence/aix-en-provence", "toulouse"]


countries = ["usa", "new-zealand", "china", "egypt", "italy", "spain", "france", "japan", "brazil"]
countries = ["brazil"]
# europoCities = [usCities, nzCities, cnCities, jpCities, bzCities, egCities, itlCities, spCities, frCities]

cities = {
	"usa": usCities,
	"new-zealand": nzCities,
	"china": cnCities,
	"japan": jpCities,
	"brazil": bzCities,
	"egypt": egCities,
	"italy": itlCities,
	"spain": spCities,
	"france": frCities
}

browser = webdriver.Firefox()
browser.set_page_load_timeout(10)
browser.set_script_timeout(10)

crawlAll()

# for country in countries:
# 	if(country != "usa"):
# 		for city in cities[country]:
# 			try:
# 				crawlCity(country, city, "cities")
# 			except TimeoutException:
# 				pass
# 			except WebDriverException:
# 				pass