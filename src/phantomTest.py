from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from crawl import baseUrl
import time
import random

pause = 3 #initial time interval between reloads

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0")
# dcap["phantomjs.page.settings.loadImages"] = False
# service_args = ["--proxy=127.0.0.1:9999", "--proxy-type=socks5"]
driver = webdriver.PhantomJS(desired_capabilities=dcap)

url = baseUrl + "/china/hong-kong/attractions/a/poi-sig/355975"
driver.get(url)
driver.save_screenshot('screen_shot.png')

lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
	print("Loading Page: the last height is ", lastHeight)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(pause)
	newHeight = driver.execute_script("return document.body.scrollHeight")
	if newHeight == lastHeight:
		break
	lastHeight = newHeight
