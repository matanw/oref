import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
import re
import os

BASE_WEBSITE = "https://www.oref.org.il"

def get_page(url):
	time.sleep(5) # we don't want to do DDos 
	res = requests.get(url)
	if res.status_code != 200:
		raise Exception(f"failed to get {url}: code is {res.status_code}")
	return res.content

def get_urls(content, lang_out):
	soup = BeautifulSoup(content, 'html.parser')
	urls = []
	for link in soup.find_all('a'):
	    target =link.get('href')
	    if not target:
	    	continue
	    if target[0] == "/":
	    	target = urljoin(BASE_WEBSITE, target[1:])
	    if BASE_WEBSITE not in target:
	    	continue
	    if re.search("[^a-z]("+lang_out+ ")($|[^a-z])", target):
	    	print(f" filter out {target}")
	    	continue
	    urls.append(target)
	return urls

def scan(start, lang_out):
	result, queue = {}, [start]
	fresh = True
	if not fresh:
		info = json.load(open('mid-result.json', 'r'))
		result, queue = info["r"], info["q"]
	failed_url = []
	i=0
	while queue:
		os.rename('mid-result.json', 'mid-result.backup.json')
		open('mid-result.json', 'w').write(json.dumps({"q":queue, "r":result, "failed": failed_url}))
		url = queue.pop(0)
		if url in result or url in failed_url:
			continue
		i = i+1
		try:
			content = get_page(url)
			print(f" {i} - {url}")
			result[url] = str(content)
			nighbours = get_urls(content, lang_out)
			for n in nighbours:
				queue.append(n)
		except:
			failed_url.append(url)
			print (f" ***** failed {url}")
	return result


website =  scan(BASE_WEBSITE+"/en", "ar|he|ru")
w = open('output.json', 'w')
w.write(json.dumps(website))