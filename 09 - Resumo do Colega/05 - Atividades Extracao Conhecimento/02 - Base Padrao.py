# Base padrão para scraping
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import sys

sys.stdout.reconfigure(encoding='utf-8') # Se não o terminal buga com o print

try:
    html = urlopen('https://disciplinas.politecnico.ufsm.br/~dpadp0291/videos.html')
    sopa = BeautifulSoup(html.read(), 'html.parser')
    print(sopa.h1.get_text())
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
else:
    print('Tudo certo. Seguir com o scraping')