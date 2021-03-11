# A script to collect site data on the potential value of a google ranking position to a web company with some conversion-to-profit calculation
import sys
import requests
from bs4 import BeautifulSoup
import time
import re

#Add import multiprocessing and multiprocessing code to call and process multiple websites simultaneously

invalidfilecharacters = ['\\', '\/', '\:', '\*', '\?', '\"', '\<', '\>', '\|', '\-']

print("The script has the name %s " % sys.argv[0])
# print("The website provided was %s" % sys.argv[1])
# webpage = requests.get(sys.argv[1])

percentagePage = requests.get('https://www.advancedwebranking.com/ctrstudy')
parsedwebpage = BeautifulSoup(percentagePage.content, 'html.parser')
rankColumns = parsedwebpage.find_all('g', class_="amcharts-graph-column") #, aria-label=True

for column in rankColumns:
    print(column)
















# for imagetag in imagetags:
# # imageData = ({'imageTitle': x['title'], 'imageURL': x['data-src']} for x in imagetag if          	   
# #   imagetag.has_attr('data-scr') and imagetag.has_attr('title') )
#     if imagetag.has_attr('data-src') and imagetag.has_attr('title'):
#         print(imagetag['data-src'])
#         print(imagetag['title'])
#         picturetitle = re.sub("|".join(invalidfilecharacters), "", imagetag['title'])
#         imagefile = open(picturetitle + ".jpg", "w+b")
#         imagefile.write(requests.get(imagetag['data-src']).content)
#         imagefile.close()