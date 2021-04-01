# A script to collect site data on the potential value of a google ranking position to a web company with some conversion-to-profit calculation
import sys
import os
from os import path
# import requests
# from bs4 import BeautifulSoup
import time
# import requests
import json
import csv
import webbrowser
import urllib.parse
import threading

pathToDownloads = "C:\\Users\\Dallas H\\Downloads"
exportPath = "C:\\Users\\Dallas H\\Downloads"
exportFilename = '\\collatedData.json'
keywordList = "C:\\Users\\Dallas H\\Downloads\\keywordList.txt"

export_to_json = False
export_to_csv = True

# extract the list of comma separated keywords to collect data on.
# If I switch to a GUI input system I may need to change the parse method.
def parseKeywordList():
    with open(keywordList) as keywordFile:
        keywordString = ''.join(keywordFile.readlines())
        keywords = keywordString.split('.')[1]
        splitKeywords = keywords.split(',')
        return splitKeywords

def autoSearchKeywords(keywords):
    chromePath = "C:\\Program Files(x86)\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
    base_url = "https://www.google.com/search?q="
    if type(keywords) is list:
        for keyword in keywords:
            query = urllib.parse.quote(keyword)
            webbrowser.open(base_url + query, 2)
    elif type(keywords) is str:
        query = urllib.parse.quote(keywords)
        webbrowser.open(base_url + query, 2)

def collateData(numFiles):
    keywordTraffic = {}
    sourceFiles = []
    while (len(sourceFiles) < numFiles):
        sourceFiles = [filename for filename in os.listdir(pathToDownloads) if (filename.startswith("KWP-") & filename.endswith(".json"))]
        time.sleep(2)
    for filename in sourceFiles:
        sourceFiles[sourceFiles.index(filename)] = pathToDownloads + "\\" + filename    
        print(f'filename {filename}')
    for filename in sourceFiles:
        print(f'opening {filename}')
        with open(filename) as json_file:
            data = json.load(json_file)
            keywordTraffic[data['keyword']] = data['keywordVolumeByRank']    
        os.remove(filename)
        #             print(sourceFiles)
        # print(len(sourceFiles))
    exportCollatedData(keywordTraffic)

def exportCollatedData(keywordTraffic):
    exportFile = exportPath + exportFilename

    
    if (export_to_json):
        if path.exists(exportFile):
            os.remove(exportFile)

        with open(exportFile, 'w') as outfile:
            json.dump(keywordTraffic, outfile)
    elif (export_to_csv):
        exportFile = exportFile.split('.')[0]
        exportFile = exportFile + ".csv"

        if path.exists(exportFile):
            os.remove(exportFile)

        with open(exportFile, 'w', newline='', encoding='utf-8') as outfile:
            csv_writer = csv.writer(outfile)
            headersWritten = False

            for keyword in keywordTraffic:
                if not (headersWritten):
                    header = ["Keyword", "Result 1", "Result 2", "Result3", "Result 4", "Result5", 
                                "Result 6", "Result 7", "Result 8", "Result 9", "Result 10"]
                    csv_writer.writerow(header)
                    headersWritten = True
                row = [keyword]
                for rank in keywordTraffic[keyword]:                    
                    row.append(rank)                
                csv_writer.writerow(row)



def main():
    # Collect data on the desired keywords
    keywordsToSearch = parseKeywordList()
    autoSearchKeywords(keywordsToSearch)

    # Collate the data into a single json file    
    collateData(len(keywordsToSearch))
    


main()
