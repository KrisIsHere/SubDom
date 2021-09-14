class SubDom():
	__version__ = 1.0
import sys
import os
import requests
from bs4 import BeautifulSoup

def proxys():
    try:
        response = requests.get("https://sslproxies.org/")
        soup = BeautifulSoup(response.content, 'html5lib')
        proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text,
        soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
        return proxy
    except Exception as e:
        pass

def scan():
	headers = {"User-Agent": "SubDom {SubDom.__version__}"}
	proxy = proxys()
	x = requests.get(sys.argv[1], headers=headers, proxies=proxy)
	if x.status_code == 504:
		print("Connection timed out.")
	elif x.status_code == 200:
		with open(sys.argv[2], "r") as f:
			for directory in f:
				find = requests.post(sys.argv[1]+"/"+directory, headers=headers, proxies=proxy)
				if find.status_code == 200:
					print(f"Directory Found : {directory}")
				elif find.status_code == 403:
					print(f"Directory Forbidden : {directory}")
				elif find.status_code == 404:
					print(f"Directory Not Found : {directory}")
				else:
					print("Something went wrong!")
	else:
		sys.exit()

if len(sys.argv) < 2:
    print("Usage: python3 "+sys.argv[0]+" <website> <wordlist>")
    sys.exit()
else:
	scan()
