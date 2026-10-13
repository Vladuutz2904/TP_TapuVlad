# Laborator: funcții, metode și importuri pe web
# Student: Tapu Vlad
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import argparse

import webtools
# Ex45 - daca main.py ar avea propria functie get_title, definitia locala ar
# inlocui (ar umbri) numele importat din webtools, iar apelurile get_title(...)
# ar folosi functia din main.py, nu cea din modul.
from webtools import get_title, security_headers, DEFAULT_HEADERS

parser = argparse.ArgumentParser(description="Raport despre un site web")  # Ex48
parser.add_argument("url", help="adresa site-ului, ex: https://cybercor.org")
args = parser.parse_args()

# Ex44
print("Titlu:", get_title(webtools.fetch(args.url).text))
# Ex47
print("Antete implicite:", DEFAULT_HEADERS)
# Ex49
webtools.create_csv(args.url, ["/", "/robots.txt", "/sitemap.xml"])
# Ex50
webtools.site_report(args.url)
# Bonus
html = webtools.fetch(args.url).text
print("Titlu (bs4):", webtools.get_title_bs(html))
print("Legaturi (bs4):", webtools.extract_links_bs(html))
