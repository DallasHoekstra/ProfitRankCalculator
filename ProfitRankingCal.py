# A script to collect site data on the potential value of a google ranking position to a web company with some conversion-to-profit calculation
import sys
import os
from os import path
import time
import json
import csv
import webbrowser
import urllib.parse

debug = False

pathToDownloads = "/home/server/Downloads/"
exportPath = "/home/server/Desktop/ProfRankCalc/ProfitRankCalculator/"
exportFilename = {'json':'/collatedData.json', 'csv':'/collatedData.csv'}
keywordList = "/home/server/Desktop/ProfRankCalc/ProfitRankCalculator/keyword_list.json"
export_to_json = False
export_to_csv = True
base_url ="https://www.google.com/search?q="

# extract the list of comma separated keywords to collect data on.
# If I switch to a GUI input system I may need to change the parse method.
def parseKeywordList():
    if (debug):
        os.system("python3 json_creator.py")
    data = {}
    with open(keywordList) as keyword_file_json:
        data = json.load(keyword_file_json)
        for key in data:
            data[key] = base_url + urllib.parse.quote(key)
    os.remove(keywordList)
    return data

def autoSearchKeywords(keywords):
    chromePath = "/usr/bin/google-chrome"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
    for key in keywords:
        print(f'Key: {key}, Value: {keywords[key]}')
        webbrowser.open(keywords[key], 2)

def collateData(numFiles):
    keywordTraffic = {}
    sourceFiles = []
    # Await completion of file downloads
    while (len(sourceFiles) < numFiles):
        sourceFiles = [filename for filename in os.listdir(pathToDownloads) if (filename.startswith("KWP-") & filename.endswith(".json"))]
        time.sleep(2)
    # All files have been downloaded, create list of full path names
    for filename in sourceFiles:
        sourceFiles[sourceFiles.index(filename)] = pathToDownloads + filename    
        print(f'filename {filename}')
    # Extract data from files
    for filename in sourceFiles:
        print(f'opening {filename}')
        with open(filename) as json_file:
            data = json.load(json_file)
            print(f'Data: {data}')
            keywordTraffic[data['keyword']] = data['keywordVolumeByRank']    
        os.remove(filename)
    return keywordTraffic

def exportCollatedData(keywordTraffic):
    for key in exportFilename:
        exportFilename[key] = exportPath + exportFilename[key]

    if (export_to_json):
        if path.exists(exportFilename['json']):
            os.remove(exportFilename['json'])

        with open(exportFilename['json'], 'w') as outfile:
            json.dump(keywordTraffic, outfile)

    elif (export_to_csv):
        if path.exists(exportFilename['csv']):
            os.remove(exportFilename['csv'])

        with open(exportFilename['csv'], 'w', newline='', encoding='utf-8') as outfile:
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
    cdata = collateData(len(keywordsToSearch))
    exportCollatedData(cdata)


main()

#if __name__ = '__main__':
#    main()
