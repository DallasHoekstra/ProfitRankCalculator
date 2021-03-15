# A script to collect site data on the potential value of a google ranking position to a web company with some conversion-to-profit calculation
import sys
import requests
from bs4 import BeautifulSoup
import time
import re





percentagePage = requests.get('https://www.advancedwebranking.com/ctrstudy')
print(percentagePage)
parsedwebpage = BeautifulSoup(percentagePage.content, 'html.parser')
print(parsedwebpage)
rankColumns = parsedwebpage.find_all('g', class_="amcharts-graph-column") #, aria-label=True

print("lalalalalal")
for column in rankColumns:
    print(column)

