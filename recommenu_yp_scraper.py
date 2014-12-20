import urllib
from HTMLParser import HTMLParser
import bs4
import re
import csv
import random

nameArr, phoneArr, addressArr, websiteArr, reviewArr, numReviewArr, hoursArr, categoriesArr, priceRangeArr = ["Name"], ["Phone"], ["Address"], ["Website"], ["Average Rating"], ["Number of Reviews"], ["Hours"], ["Categories"], ["Price Range"]

for page in range(1, 112):
	htmlfile = urllib.urlopen('http://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=Austin%2C%20TX&page=' + str(page) + '&s=relevance')

	htmltext = htmlfile.read()

	soup = bs4.BeautifulSoup(htmltext)

	linkDivs = soup.findAll('div', { 'class' : 'info-section info-primary' })

	count = 0
	for linkDiv in linkDivs:
		if count < 30:
			count = count + 1
			try:
				htmlfile2 = urllib.urlopen('http://www.yellowpages.com' + linkDiv.find('a')['href'])
				htmltext2 = htmlfile2.read()

				soup2 = bs4.BeautifulSoup(htmltext2)

				name, phone, address, website, review, numReview, hours, categories, priceRange = '', '', '', '', '', '', '', '', ''

				try:
					name = soup2.find('h1').getText().encode('utf8')
				except:
					name = "Not Listed"
				try:
					review = soup2.find(attrs={"itemprop" : "aggregateRating"}).find('meta')['content'].encode('utf8')
				except:
					review = "Not Listed"
				try:
					numReviews = soup2.find(attrs={"itemprop" : "reviewCount"}).getText().replace('(', '').replace(')', '').encode('utf8')
				except:
					numReviews = "Not Listed"
				try:
					address = soup2.find('p', attrs={'class': 'street-address'}).getText() + soup2.find('p', attrs={'class': 'city-state'}).getText().encode('utf8')
				except:
					address = "Not Listed"
				try:
					phone = soup2.find('p', attrs={'class': 'phone'}).getText().encode('utf8')
				except:
					phone = "Not Listed"
				try:
					website = soup2.find('a', attrs={'class': 'custom-link'})['href'].encode('utf8')
				except:
					website = "Not Listed"
				try:
					allHours = soup2.findAll('time', attrs={'itemprop': 'openingHours'})
					for hour in allHours:
						hours += (hour['datetime'] + ', ').encode('utf8')
				except:
					hours = "Not Listed"
				try:
					allCategories = soup2.find('dd', attrs={'class': 'categories'}).findAll('a')
					for category in allCategories:
						categories += (category.getText() + ', ').encode('utf8')
				except:
					hours = "Not Listed"
				try:
					priceRange = soup2.find('span', attrs={'class': 'price-range'}).getText().encode('utf8')
				except:
					priceRange = "Not Listed"

				nameArr.append(name)
				phoneArr.append(phone)
				addressArr.append(address)
				websiteArr.append(website)
				reviewArr.append(review)
				numReviewArr.append(numReviews)
				hoursArr.append(hours)
				categoriesArr.append(categories)
				priceRangeArr.append(priceRange)

			except:
				print random.choice(['Blake eats butt', 'Blake and Jake sitting in a tree', 
					'Blake does not even lift', 'Blake is a cutie pie', 'Blake is a poop face',
					'Hey, Blake is dumb', 'Carlos is a Maricon', 'Fiddler on the roof is an excellent play',
					'Chilantro, yeah', 'CumbleUpon >>> Recommenu'])

with open('Bulk.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows([nameArr, phoneArr, addressArr, websiteArr, reviewArr, numReviewArr, hoursArr, categoriesArr, priceRangeArr])

print 'Results located in Bulk.csv'