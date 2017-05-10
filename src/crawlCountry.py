import crawl
import json
import re
from bs4 import BeautifulSoup

'''
Crawler for each single country

Information to crawl for a country
# Name
	inside "h1" with class "masthead__title"
	text processing needed: remove the '\n' and white space the beginning and '\n' at the end

# Area belongs to (usually continent):
	inside "a" inside "div" with class "masthead__breadcrumb"

# Images
	inside data-lp-initial-images attribute of "div" with class "slideshow"
	text processing needed:
	1. each image have four values: small, medium, large, strapline, with the destination url the same, need to keep only one url for each image
	2. size of each version are different, need to remove size parameter at the end

# Map
	inside data-preload attribute of "div" with class "map-static__container"

# Introduction
	inside the page [countryUrl]/introduction
	inside "div" with itemprop = "articleBody"
	There are hyperlink inside text, therefore removal of links are needed
	# Why I love
		inside "p" with class "copy--body" following a "h2" element with class "copy--subtitle" and text "Why I love ...", and a "p" element with class "copy-body" and author inside
	# brief introdution
		inside "p" with class "copy--feature"
	# general introduction for features
		a "h2" with class "copy-subtitle" with a following "p" with class "copy-body"

# Essential Information
	inside the page [countryUrl]/essential-information
	really a lot of thing to crawl...
	# At a glance
		# language
			# phrase for "hello"
				inside "div" with class "js-hello-phrase"
				need to remove the '\n's at the beginning and at the end
			# language name
				inside "div" with class "hello__language"
				need to remove the '\n's at the beginning and at the end	
		# electricity
			# plugImgUrl
				inside the src attribute of "img" with class "plug-image"
			# elecType
				inside the "div" following a sibling "div" with text value "Electricity"
				need to remove the '\n's at the beginning and the end
			# more on electricity
				TO BE EXPLORED
		# Best time to go
			# best months to go
				inside "div" with class "flip-chart"
				need to remove the '\n's at the beginning and the end
			# best seasons to go 
				inside the "div" following a sibling "div" with text "Best time to go"
				need to remove the '\n' at the beginning and the end
				when more than one best seasons, '\n\n' will be inserted between seasons 
		# Current Weather
			TO BE EXPLORED
	# Visas
		# brief information
			inside "p" inside "div" following a sibling "h3" with id "visas"
			inside the second "p", the first "p" is observed to be empty (according china and usa)
		# LP's visa advice
			TO BE EXPLORED
		# More on entry and exit formalities
			TO BE EXPLORED
	# When to go and weather
		TO BE EXPLORED
	# Getting to China
		TO BE EXPLORED
	# Getting around China
		TO BE EXPLORED
	# Health and safety
		TO BE EXPLORED
	# Advice for travellers
		TO BE EXPLORED
	# COMMUNICATION
		TO BE EXPLORED
	# TOURIST INFORMATION
		TO BE EXPLORED
	# GOOD TO KNOW
		TO BE EXPLORED
	# BEFORE YOU GO
		TO BE EXPLORED
		
# Articles
	inside the page [countryUrl]/travel-tips-and-articles
	# article
		each article inside a "div" with class "card__mask"
		all elements refered below are children of the "div" fore-mentioned
		# article url
			inside the href attribute of the "a" element
			need to add "https://www.lonelyplanet.com" in front of the link
		# article imaegUrl
			inside the src attribute of the "img" element
			processing needed: remove the the leading query path, leave only the link with the format like "http://www.lonelyplanet.com/travel-blog/tip-article/wordpress_uploads/2017/05/xian-chinaGettyImages-187351791-2b87a256574c.jpg"
		# article title
			inside the "h1" with class "card__content__title"
			need to remove '\n'
		# article in brief
			inside the "div" with class "card__content__desc"
			need to remove '\n'

# Places
	inside the page [countryUrl]/places
	# place
		each article inside a "div" with class "card__mask"
		all elements refered below are children of the "div" fore-mentioned
		# place url
			inside the href attribute of the "a" element
			need to add "https://www.lonelyplanet.com" in front of the link
		# place name
			inside the "h1" (with class "card__content__title", which is not necessary for crawling)
			need to remove '\n'
		# place imageUrl
			inside the src attribute of the "img" element
			processing needed: remove the the leading query path, leave only the link with the format like "http://www.lonelyplanet.com/blablabla.jpg"
		# place brief descriptoin
			inside the "div" with class "card__content__desc"
			need to remove '\n' at the beginning and at the end, but not in between paragraph
'''

def crawlCountry(countryUrl, article = False):
	country = {}

	bs = crawl.getBS(countryUrl)
	if(not bs):
		print("Failed to access the country page %s, country crawling ends" % countryUrl)
		return country

	### Get the name ###
	nameHeader = bs.find("h1", class_="masthead__title")
	if(not nameHeader):
		print("Failed to access the name at the country page %s, country crawling ends" % countryUrl)
		return country
	name = nameHeader.text
	name = name.replace('\n','').replace(' ','')
	country["name"] = name


	### Get the area ###
	area = ""
	areaDiv = bs.find("div", class_="masthead__breadcrumb")
	if(areaDiv):
		area = areaDiv.a.text
	else:
		print("Failed to access the area for the country %s" % name)
	country["area"] = area


	### Get the image urls ###
	imageUrls = []
	imageDiv = bs.find("div", class_="slideshow")
	if(imageDiv):
		images = imageDiv["data-lp-initial-images"]
		imageList = json.loads(images) # convert string to list of objects/dicts
		for image in imageList:
			# exception handler in case of the "small" key corresponds to an empty value
			# code here...
			imageUrl = image["small"] # get the url with size parameter for the small version
			imageUrl = imageParamRemover(imageUrl) # remove the size parameter
			imageUrls.append(imageUrl)
	else:
		print("Failed to access images for the country %s" % name)
	country["imageUrls"] = imageUrls


	### get the map url ###
	mapUrl = ""
	mapDiv = bs.find("div", class_="map-static__container")
	if(mapDiv):
		mapUrl = mapDiv["data-preload"]
		mapUrl = imageParamRemover(mapUrl)
	else:
		print("Failed to access the map for the country %s" % name)
	country["mapUrl"] = mapUrl


	### get the introduction (including "Why I Love...", a brief introduction and additional introduction) ###
	brief = ""
	love = {}
	intros = {}
	introUrl = countryUrl + "/introduction"
	introBS = crawl.getBS(introUrl)
	if(introBS):
		introDiv = introBS.find("div", attrs={"itemprop":"articleBody"})

		### get the "Why I Love..." introduction ###
		loveHeader = introDiv.find("h2", text=re.compile("Why I Love"))
		if(loveHeader):
			# error handler here in the case that the following two elements are not author, body in sequence
			# code here...
			authorP = loveHeader.find_next_sibling()
			loveP = authorP.find_next_sibling()		
			love["title"] = loveHeader.text
			love["author"] = authorP.text
			love["body"] =  loveP.text
			loveHeader.extract()
			authorP.extract()
			loveP.extract()
		else:
			# error handler here in the case that the "Why I Love..." <h2> is not found
			# code here...
			print("Failed to extract \"Why I Love...\" introduction for the country %s" % name)

		### get the brief introduction ###
		briefElem = introDiv.p
		if ('copy--feature' in briefElem["class"]):
			brief = briefElem.text
		else:
			# error handler in the case that the first element is not for brief
			# code here...
			print("Failed to extract brief introduction for the country %s" % name)

		### get other general introduction ###
		subtitle = ""
		for introElem in briefElem.next_siblings:
			# if the element is a "h2", store it as te current subtitle
			# otherwise (it's a "p"), append it to the list with the current subtitle as its key
			if('copy--subtitle' in introElem["class"]):
				subtitle = introElem.text
				intros[subtitle] = []
			elif('copy--body' in introElem["class"]):
				if(not subtitle):
					# error handler in the case that no corresponding subtitle found
					# code here...
					print("Error: Introduction body for the country %s with no subtitles encountered" % name)
				else:
					intros[subtitle].append(introElem.text)
			else:
				# error handler in the case that unrecognized element found
				# code here...
				print("Error: Introduction for the country %s with unrecognizable type encountered" % name)
	else:
		print("Failed to access the introduction page for the country %s" % name)
	country["brief"] = brief
	country["love"] = love
	country["intros"] = intros


	### get the essential information ###
	greeting = ""
	language = ""
	plugImgUrl = ""
	elecType = ""
	visaIntro = ""
	bestMonths = []
	bestSeasons = []
	essInfoUrl = countryUrl + "/essential-information"	
	infoBS = crawl.getBS(essInfoUrl)
	if(introBS):

		### get the language information: language name and "hello" in the language ###
		greetingDiv = infoBS.find("div", class_="js-hello-phrase")
		if(greetingDiv):
			greeting = greetingDiv.text
			greeting = greeting.replace('\n','')
		else:
			print("Failed to access the \"hello\" in local language for the country %s" % name)
		languageDiv = infoBS.find("div", class_="hello__language")
		if(languageDiv):
			language = languageDiv.text
			language = language.replace('\n','')
		else:
			print("Failed to access the language for the country %s" % name)

		### get the electricity information: plug image and electricity type ###
		plugImg = infoBS.find("img", class_="plug-image")
		if(plugImg):
			plugImgUrl = plugImg["src"]
			plugImgUrl = imageParamRemover(plugImgUrl)
		else:
			print("Failed to access the plug image for the country %s" % name)
		elecDiv = infoBS.find("div", text=re.compile("Electricity"))
		if(elecDiv):
			elecTypeDiv = elecDiv.find_next_sibling()
			if(elecTypeDiv):
				elecType = elecTypeDiv.text
				elecType = elecType.replace('\n','')
			else:
				print("Failed to access the electricity type for the country %s" % name)
		else:
			print("Failed to access the electricity label for the country %s" % name)

		### get the best travel time: seasons and months ###
		bestMonthDivs = infoBS.find_all("div", class_="flip-chart")
		for bestMonthDiv in bestMonthDivs:
			bestMonth = bestMonthDiv.text
			bestMonth = bestMonth.replace('\n','')
			bestMonths.append(bestMonth)
		bestTimeDiv = infoBS.find("div", text=re.compile("Best time to go"))
		if(bestTimeDiv):
			bestSeasonDiv = bestTimeDiv.find_next_sibling()
			if(bestSeasonDiv):
				seasonStr = bestSeasonDiv.text
				seasons = seasonStr.replace('\n\n','@').replace('\n','').split('@')
				for season in seasons:
					bestSeasons.append(season)
			else:
				print("Failed to access the best seasons for traveling for the country %s" % name)
		else:
			print("Failed to access the best time to go label for the country %s" % name)

		### get the visa information ###
		visaHeader = infoBS.find("h3", id="visas")
		if(visaHeader):
			visaDiv = visaHeader.find_next_sibling()
			if(visaDiv):
				if(not visaDiv.p.text.replace('\n','')):
					visaDiv.p.extract()
				visaP = visaDiv.p
				visaIntro = visaP.text
			else:
				print("Failed to access the brief visa information for the country %s" % name)
		else:
			print("Failed to access the visa headerfor the country %s" % name)
	else:
		print("Failed to access the essential information page for the country %s" % name)
	country["greeting"] = greeting
	country["language"] = language
	country["plugImgUrl"] = plugImgUrl
	country["elecType"] = elecType
	country["visaIntro"] = visaIntro
	country["bestMonths"] = bestMonths
	country["bestSeasons"] =  bestSeasons

	### get all articles ###
	if(article):
		articles = crawlAllArticles(countryUrl, name)
		country["articles"] = articles

	return country

def imageParamRemover(imageUrl):
	newUrl = imageUrl.split('?')[0] # remove the size parameter
	return newUrl

### get all articles: url only and crawl all articles available ###
def crawlAllArticles(countryUrl, countryName):	
	articles = []
	articlesUrl = countryUrl + "/travel-tips-and-articles"
	articlesBS = crawl.getBS(articlesUrl)
	if(articlesBS):

		# get the number of pages of articles
		pageLinks = articlesBS.find_all("a", class_="js-page-link")
		pageCount = len(pageLinks) + 1

		### get urls from each single page ###
		for pageNum in range(pageCount):
			if(pageNum > 0):
				articlesUrl = countryUrl + "/travel-tips-and-articles?page=" + str(pageNum + 1)
				articlesBS = crawl.getBS(articlesUrl)
			if(articlesBS):
				articleDivs = articlesBS.find_all("div", class_="card__mask")

				### get url for each single article ###
				for articleDiv in articleDivs:
					articleA = articleDiv.a
					if(not articleA):
						print("Failed to access the link to page of this article under the country %s" % countryName)
						continue
					articleUrl = articleA["href"]
					articleUrl = crawl.baseUrl + articleUrl
					articles.append(articleUrl)
			else:
				print("Failed to access to the #%d articles page of the country %s" % (pageNum, countryName))
	else:
		print("Failed to get the articles page for the country %s" % countryName)

	return articles

### get the articles with number limited, 8 at default, with url, imageUrl, title and desc ###
def crawlArticles(countryUrl, countryName, num = 8):
	articles = []
	articlesUrl = countryUrl + "/travel-tips-and-articles"
	articlesBS = crawl.getBS(articlesUrl)
	if(articlesBS):
		articleDivs = articlesBS.find_all("div", class_="card__mask", limit=num) # crawl with number of articles limited to parameter num

		### get information for each single article ###
		for articleDiv in articleDivs:
			articleA = articleDiv.a
			if(not articleA):
				print("Failed to access the link to page of this article under the country %s" % countryName)
				continue
			article = {}
			imageUrl = ""
			title = ""
			desc = ""
			url = articleA["href"]
			url = crawl.baseUrl + url

			articleImg = articleDiv.img
			if(articleImg):
				rawUrl = articleImg["src"]
				pattern = 'http:\/\/www\.lonelyplanet\.com\/.*\.jpg'
				searchObj = re.search(pattern, rawUrl)
				imageUrl = searchObj.group()
			else:
				print("Failed to access the imageUrl of the article %s" % url)

			titleHeader = articleDiv.find("h1", class_="card__content__title")
			if(titleHeader):
				title = titleHeader.text
				title = title.replace('\n','')
			else:
				print("Failed to access the title of the article %s" % url)

			descDiv = articleDiv.find("div", class_="card__content__desc")
			if(descDiv):
				desc = descDiv.text
				desc = desc.replace('\n','')
			else:
				print("Failed to access the brief description of the article %s" % url)

			article["url"] = url
			article["title"] = title
			article["desc"] = desc
			article["imageUrl"] = imageUrl
			
			articles.append(article)
	else:
		print("Failed to access the articles page of the country %s" % countryName)
	return article

def crawlAllPlaces(countryUrl, countryName):
	places = {}
	placesUrl = countryUrl + "/places"
	placesBS = crawl.getBS(placesUrl)
	if(placesBS):

		# get the number of pages of places
		pageLinks = placesBS.find_all("a", class_="js-page-link")
		pageCount = len(pageLinks) + 1

		### get places from each single page ###
		for pageNum in range(pageCount):
			if(pageNum > 0):
				placesUrl = countryUrl + "/places?page=" + str(pageNum + 1)
				placesBS = crawl.getBS(placesUrl)
			if(placesBS):
				placeDivs = placesBS.find_all("div", class_="card__mask")

				### get name and url for each single place ###
				for placeDiv in placeDivs:
					placeUrl = ""
					placeHeader = placeDiv.h1
					if(not placeHeader):
						print("Failed to access the name of this place of the country %s" % countryName)
						continue
					placeName = placeHeader.text
					placeName = placeName.replace('\n','')
					placeA = placeDiv.a
					if(not placeA):
						print("Failed to access the link to this city of the country %s" % countryName)
						continue
					placeUrl = placeA["href"]
					placeUrl = crawl.baseUrl + placeUrl
					places[placeName] = placeUrl
			else:
				print("Failed to access to the #%d places page of the country %s" % (pageNum, countryName))
	else:
		print("Failed to get the places page for the country %s" % countryName)

	return places