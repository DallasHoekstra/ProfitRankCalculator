# A script to collect site data on the potential value of a google ranking position to a web company with some conversion-to-profit calculation
import sys
import os
import requests
from bs4 import BeautifulSoup
import time
import requests
import json
import webbrowser

pathToDownloads = "C:\\Users\\Dallas H\\Downloads"
exportPath = "C:\\Users\\Dallas H\\Downloads"
exportFilename = '\\collatedData.json'

def autoSearchKeywords(keywords):
    webbrowser.get("open -a C:\\Program Files(x86)\\Google\\Chrome\\Application\\chrome.exe")
    webbrowser.open
    #https://www.google.com/search?q=open+browser+tab+python&oq=open+browser+tab+python&aqs=chrome..69i57j0i22i30l3.5183j0j7&sourceid=chrome&ie=UTF-8
    for keyword in keywords:
        webbrowser.open(keyword, 2)

def collateData(sourceFiles):
    keywordTraffic = {}

    for filename in sourceFiles:
        print(filename)
        filename = pathToDownloads + "\\" + filename
        print(filename)
        with open(filename) as json_file:
            data = json.load(json_file)
            keywordTraffic[data['keyword']] = data['keywordVolumeByRank']
    return keywordTraffic

def exportCollatedData(keywordTraffic):
    exportFile = exportPath + exportFilename
    with open(exportFile, 'w') as outfile:
        json.dump(keywordTraffic, outfile)

def main():
    
    autoSearchKeywords("covid relief mortgage")

    keywordFiles = [filename for filename in os.listdir(pathToDownloads) if (filename.startswith("KWP-") & filename.endswith(".json"))]
    keywordTraffic = collateData(keywordFiles)
    exportCollatedData(keywordTraffic)


main()





# percentagePage = requests.get('https://www.advancedwebranking.com/ctrstudy')
# print(percentagePage)
# parsedwebpage = BeautifulSoup(percentagePage.content, 'html.parser')
# print(parsedwebpage)
# rankColumns = parsedwebpage.find_all('g', class_="amcharts-graph-column") #, aria-label=True

# print("lalalalalal")
# for column in rankColumns:
#     print(column)

