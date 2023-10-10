import json, requests, re, os, time




def get_page(url):
	time.sleep(5) # we don't want to do DDos 
	res = requests.get(url)
	if res.status_code != 200:
		raise Exception(f"failed to get {url}: code is {res.status_code}")
	return res.content

def convert_url(url, target):
	return re.sub('([^a-z])he([^a-z]|$)', r'\1'+target+r'\2', url)

def get(target):
	he= json.load(open('all_he.json', 'r'))
	he_urls = list(he.keys())
	he_urls.sort()
	result = {}
	failed = []
	for idx, url in enumerate(he_urls):
		os.rename('mid-result.json', 'mid-result.backup.json')
		open('mid-result.json', 'w').write(json.dumps({"r":result, "failed": failed}))
		print(f' {idx} , {len(he_urls)}')
		target_url = convert_url(url, target)
		if url == target_url:
			print(f" skipping {url}")
			continue
		if target_url in result:
			continue
		try:
			content = get_page(target_url)
			result[target_url] = str(content)
			print(f"got {target_url}")
		except Exception as error:
			failed.append(url)
			print(f" fail {target_url} : {error}")
	open(target+'-result.json', 'w').write(json.dumps(result))

#get('ar')

def create_mapping():
	he= list(json.load(open('all_he.json', 'r')).keys())
	langs = ['en', 'ar','ru']
	content = {}
	for lang in langs:
		content[lang]=list(json.load(open(lang+'-result.json', 'r')).keys())
	result = {}
	for key in he:
		if convert_url(key,"blabla") ==key:
			result[key]= {lang:"irrlevent" for lang in langs}
		else:
			result[key]={}
			for lang in langs:
				converted_url = convert_url(key, lang)
				result[key][lang]=converted_url if converted_url in content[lang] else "missing"
	open('mapping.json', 'w').write(json.dumps(result))
create_mapping()