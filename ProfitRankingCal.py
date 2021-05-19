# A script to collect site data on the potential value of a google ranking position to a web company with some conversion-to-profit calculation
import os
from os import path
import time
import json
import csv
import webbrowser
import urllib.parse
import config

pathToDownloads = config.parameters['pathToDownloads']
exportPath = config.parameters['exportPath']
keywordList = config.parameters['keywordList']
exportFilename = config.parameters['exportFilename']
export_to_json = config.parameters['export_to_json']
export_to_csv = config.parameters['export_to_csv']
base_url = config.parameters['base_url']
debug = config.parameters['debug']
generate_json_command = config.parameters['generate_json_command']

MAX_TABS = 10

# extract the list of comma separated keywords to collect data on.
# If I switch to a GUI input system I may need to change the parse method.
def parseKeywordList():
    if (debug):
        os.system(generate_json_command)

    data = {}
    with open(keywordList) as keyword_file_json:
        data = json.load(keyword_file_json)
        for key in data:
            data[key] = base_url + urllib.parse.quote(key)
    os.remove(keywordList)
    return data

def batchSearches(keywordsToSearch, MAX_TABS):
    searchSubset = {}
    keylist = list(keywordsToSearch.keys())
    while len(searchSubset) < MAX_TABS:
        key = keylist.pop()
        searchSubset[key] = keywordsToSearch.pop(key)
    return searchSubset


def autoSearchKeywords(keywords):
    chromePath = "/usr/bin/google-chrome"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))

    for key in keywords:
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
        if (debug):
            print(f'filename {filename}')

    # Extract data from files
    for filename in sourceFiles:
        if (debug):
            print(f'opening {filename}')
        with open(filename) as json_file:
            data = json.load(json_file)
            print(f'Data: {data}')
            keywordTraffic[data['keyword']] = data['keywordVolumeByRank']
        os.remove(filename)
    return keywordTraffic

# FOR FUTURE: add a nonce to export file (and any other generated/removed files) 
# so that simultaneous requests don't remove each others files.
def delete_previous_searches():
    if path.exists(exportFilename['json']):
        os.remove(exportFilename['json'])
    if path.exists(exportFilename['csv']):
        os.remove(exportFilename['csv'])

def exportCollatedData(keywordTraffic):
    for key in exportFilename:
        exportFilename[key] = exportPath + exportFilename[key]

    if (export_to_json):
        with open(exportFilename['json'], 'a') as outfile:
            json.dump(keywordTraffic, outfile)

    elif (export_to_csv):
        with open(exportFilename['csv'], 'a', newline='', encoding='utf-8') as outfile:
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

    # Remove .json and .csv files from previous searches
    delete_previous_searches()

    cdata = {}

    # Batch keywords to avoid crashing server on massive data sets
    while len(keywordsToSearch) > 0:
        if len(keywordsToSearch) > MAX_TABS:
            keywordsToSearchSubset = batchSearches(keywordsToSearch, MAX_TABS)
        else: 
            keywordsToSearchSubset = batchSearches(keywordsToSearch, len(keywordsToSearch))

        autoSearchKeywords(keywordsToSearchSubset)


        # Collate the data into a formatted object
        cdata.update(collateData(len(keywordsToSearchSubset)))


    # Save the data to a json/csv file
    exportCollatedData(cdata)

main()

#if __name__ = '__main__':
#    main()
