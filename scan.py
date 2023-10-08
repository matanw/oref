import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

BASE_WEBSITE = "https://www.oref.org.il"

def get_page(url):
	time.sleep(5) # we don't want to do DDos 
	res = requests.get(url)
	if res.status_code != 200:
		raise Exception(f"failed to get {url}: code is {res.status_code}")
	print(f' got {url}')
	return res.content

def get_urls(base, content):
	soup = BeautifulSoup(content, 'html.parser')
	urls = []
	for link in soup.find_all('a'):
	    target =link.get('href')
	    if not target:
	    	continue
	    if target[0] == "/":
	    	target = urljoin(base, target[1:])
	    if BASE_WEBSITE not in target:
	    	continue
	    urls.append(target)
	return urls

def scan(start):
	queue = [start]
	result = {}
	while queue:
		url = queue.pop(0)
		if url in result:
			continue
		content = get_page(url)
		result[url] = content
		nighbours = get_urls(url, content)
		for n in nighbours:
			queue.append(n)
	return res

website =  scan(BASE_WEBSITE)
w = open('output.json', 'w')
w.write(json.dumps(website))