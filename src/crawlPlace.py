import crawl
import json
import re
from bs4 import BeautifulSoup
from crawlCountry import imageParamRemover

def crawlPlace(placeUrl, article = False):
	place = {}

	bs = crawl.getBS(placeUrl)
	if(not bs):
		print("Failed to access the place page %s, place crawling ends" % placeUrl)
		return place

	### Get the name ###
	nameHeader = bs.find("h1", class_="masthead__title")
	if(not nameHeader):
		print("Failed to access the name at the place page %s, place crawling ends" % placeUrl)
		return place
	name = nameHeader.text
	name = name.replace('\n','')
	name = " ".join(name.split())
	country["name"] = name

	### Get the area and the country###
	area = ""
	country = ""
	posDiv = bs.find("div", class_="masthead__breadcrumb")
	if(posDiv):
		posA = posDiv.find_all("a")
		if(len(posA) != 2):
			print("Failed to access the area and the country the place %s belonging to: cannot recognize the information given" % name)
		else:
			area = posA[0].text
			country = posA[1].text
	else:
		print("Failed to access the area and the country the place %s belonging to" % name)
	country["area"] = area
	country["country"] = country

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
		print("Failed to access images for the place %s" % name)
	place["imageUrls"] = imageUrls

	### Get the map url ###
	mapUrl = ""
	mapDiv = bs.find("div", class_="map-static__container")
	if(mapDiv):
		mapUrl = mapDiv["data-preload"]
		mapUrl = imageParamRemover(mapUrl)
		# for further use, url preprocessing is needed, as the image the url refers to is static and does not show the full view of the city
		# code here...
	else:
		print("Failed to access the map for the place %s" % name)
	place["mapUrl"] = mapUrl

	### Get the essential information ###

	### Get all articles ###
	if(article):
		articles = crawlAllArticles(placeUrl, name)
		place["articles"] = articles

	### Get all attractions/sights ###
	sights = {}
	sightsA = bs.find("a", class_="sights__more")
	if(not sightsA):
		print("Failed to access the more sights link for the place %s" % name)
	else:
		sightsUrl = sightsA["href"]
		sights = crawlAllSights(sightsUrl, name)
	place["sights"] = sights


	### Get all restaurants ###

	return place

def crawlAllSights(sightsUrl, placeName):
	sights = {}
	sightsBS = crawl.getBS(sightsUrl)
	if(sightsBS):
		# wait until loading to the bottom of the page
		# code here...
		sights = {} # to be deleted
	else:
		print("Failed to get the sights page for the place %s"  % name)
	return sights

def crawlAllArticles(placeUrl, placeName):	
	articles = []
	articlesUrl = placeUrl + "/travel-tips-and-articles"
	articlesBS = crawl.getBS(articlesUrl)
	if(articlesBS):

		# get the number of pages of articles
		pageLinks = articlesBS.find_all("a", class_="js-page-link")
		pageCount = len(pageLinks) + 1

		### get urls from each single page ###
		for pageNum in range(pageCount):
			if(pageNum > 0):
				articlesUrl = placeUrl + "/travel-tips-and-articles?page=" + str(pageNum + 1)
				articlesBS = crawl.getBS(articlesUrl)
			if(articlesBS):
				articleDivs = articlesBS.find_all("div", class_="card__mask")

				### get url for each single article ###
				for articleDiv in articleDivs:
					articleA = articleDiv.a
					if(not articleA):
						print("Failed to access the link to page of this article under the place %s" % placeName)
						continue
					articleUrl = articleA["href"]
					articleUrl = crawl.baseUrl + articleUrl
					articles.append(articleUrl)
			else:
				print("Failed to access to the #%d articles page of the place %s" % (pageNum, placeName))
	else:
		print("Failed to get the articles page for the place %s" % placeName)

	return articles