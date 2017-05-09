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

# Survival Guides

# Articles

# Cities
'''

def crawlCountry(countryUrl):
	country = {}

	bs = crawl.getBS(countryUrl)
	if(not bs):
		print("Failed to access the country page %s" % countryUrl)
		return country

	name = bs.find("h1", class_="masthead__title").text
	name = name.replace('\n','').replace(' ','')
	country["name"] = name

	area = bs.find("div", class_="masthead__breadcrumb").a.text
	country["area"] = area

	images = bs.find("div", class_="slideshow")["data-lp-initial-images"]
	imageList = json.loads(images) # convert string to list of objects/dicts
	imageUrls = []
	for image in imageList:
		# exception handler in case of the "small" key corresponds to an empty value
		# code here...
		imageUrl = image["small"] # get the url with size parameter for the small version
		imageUrl = imageUrl.split('?')[0] # remove the size parameter
		imageUrls.append(imageUrl)
	country["imageUrls"] = imageUrls

	brief = ""
	love = {}
	intros = {}
	introUrl = countryUrl + "/introduction"
	introBS = crawl.getBS(introUrl)
	if(introBS):
		introDiv = introBS.find("div", attrs={"itemprop":"articleBody"})
		loveHeader = introDiv.find("h2", text=re.compile("Why I Love"))
		if(loveHeader):
			# error handler here in the case that the following two elements are not author, body in sequence
			# code here...
			authorP = loveHeader.find_next_sibling()
			loveP = authorP.find_next_sibling()		
			love["title"] = loveHeader.text,
			love["author"] = authorP.text,
			love["body"] =  loveP.text
			loveHeader.extract()
			authorP.extract()
			loveP.extract()
		else:
			# error handler here in the case that the "Why I Love..." <h2> is not found
			# code here...
			print("Failed to extract \"Why I Love...\" introduction for the country %s" % name)

		briefElem = introDiv.p
		if ('copy--feature' in briefElem["class"]):
			brief = briefElem.text
		else:
			# error handler in the case that the first element is not for brief
			# code here...
			print("Failed to extract brief introduction for the country %s" % name)

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
					print("Error: Introduction body for the country %s with no subtitles encountered", name)
				else:
					intros[subtitle].append(introElem.text)
			else:
				# error handler in the case that unrecognized element found
				# code here...
				print("Error: Introduction for the country %s with unrecognizable type encountered", name)
	else:
		print("Failed to access the introduction page for the country %s" % name)
	country["brief"] = brief
	country["love"] = love
	country["intros"] = intros

	return country