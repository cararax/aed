# Base padrão para scraping
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import sys

sys.stdout.reconfigure(encoding='utf-8') # Se não o terminal buga com o print

try:
    html = urlopen('https://quotes.toscrape.com/')
    sopa = BeautifulSoup(html.read(), 'html.parser')
    print(sopa.h1.get_text())
    spans = sopa.find_all("span", {"class": "tag-item"})
    for span in spans:
        link = "https://quotes.toscrape.com" + span.a["href"] # poderia ser span.a.get("href")
        print(link)
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
else:
    print('Tudo certo joia de cabo a rabo')