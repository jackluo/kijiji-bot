import sys
import pickle
import webbrowser
import requests
import os.path
from bs4 import BeautifulSoup

class Listings:
	# This class has 4 instance variables containing info on the listings
	def __init__(self, titles, prices, links, size):
		self.titles = titles
		self.prices = prices
		self.links = links
		self.size = size
	
def getWebsiteData():
	# This function uses requests and beautifulsoup to return the html data containing all the listings for the old video games Ottawa kijiji page
	r = requests.get('http://m.kijiji.ca/old-video-games/ottawa/f?categoryId=623&locationId=1700185')
	soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf8')
	data = soup.body.div.div.div.div.div.find_next_sibling().find_next_sibling().find_next_sibling().div.ul.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
	return data
	
def getListingsData(data):
	# Initialize the lists to be used
	dataset = []
	titles = []
	prices = []
	links = []

	# These flags determine the listing search criteria
	flags = ['game boy','nintendo','snes','64','gba','gameboy','metroid','mario','pokemon']
	exclude = ['looking for', 'want to buy', 'broken']
	
	# We only add every second item from the data to our dataset. The odd items are blank
	i = 1
	for item in data:
		if i%2 == 0:
			dataset.append(item.contents[1])
		i = i + 1
	
	# Each listing has a title, price, and link. If the title matches the search criteria, the listing is added to our list of listings
	for item in dataset:
		title = item.div.find_next_sibling().find_next_sibling().div.find_next_sibling().text
		if any(x in title.lower() for x in flags) & ~any(y in title.lower() for y in exclude):
			titles.append(title)
			prices.append(item.div.find_next_sibling().find_next_sibling().div.text[1:][:-7])
			links.append(item['href'])
	size = len(titles)
	
	# We create an instance of the Listings class for the listings and return it
	listings = Listings(titles,prices,links,size)
	return listings

def getNewListings(listings):
	# Check if the dump is present. If so, open the old listings to compare with the new listings
	if os.path.isfile('data.dump'):
		with open('data.dump', "rb") as input:
			oldlistings = pickle.load(input) # protocol version is auto detected

		# Find the new listings
		s = set(oldlistings.titles)
		newlistings = [x for x in listings.titles if x not in s]
	else:
		# If there's no dump, the listings are the new listings
		newlistings = [x for x in listings.titles]
		
	# Output the current listings to the data dump
	with open("data.dump", "wb") as output:
		pickle.dump(listings, output, pickle.HIGHEST_PROTOCOL)
	
	return newlistings
	
def outputListingsData(listings):
	# This function opens a text file, outputs all the listings data and then opens the file in Notepad
	text_file = open("Output.txt", "w")
	text_file.write('There are '+str(listings.size)+' listings that match the search criteria.\n\n')
	for i in range(0,listings.size):
		text_file.write('----------------------------------------------------------------'+'\n')
		text_file.write(listings.titles[i]+'\n')
		text_file.write(listings.prices[i]+'\n')
		text_file.write(listings.links[i]+'\n')
	text_file.write('----------------------------------------------------------------')
	text_file.close()

def main():
	data = getWebsiteData()
	listings = getListingsData(data)
	newlistings = getNewListings(listings)
	outputListingsData(listings)
	if len(newlistings) != 1:
		print('There are '+str(len(newlistings))+' new listings.')
	else:
		print('There is '+str(len(newlistings))+' new listing.')
	if len(newlistings) > 0: # If there are new listings, we output the titles
		for listing in newlistings:
			print(listing)
		webbrowser.open("Output.txt")
		
main()