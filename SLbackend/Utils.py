import requests
import json
def pullWikiTable(page,section,prop):
    link = "https://en.wikipedia.org/w/api.php?action=parse&page="+page+"&format=json&prop="+prop
    if prop == "wikitext":
        webpage = requests.get(link+"&section="+section)
    else:
        webpage = requests.get(link)
    rawSource = webpage.text
    parsedSource = json.loads(rawSource)
    return parsedSource

def findVal(String,check):
        index = 0
        l1 = []
        length = len(String)
        while index < length:
            i = String.find(check, index)
            if i == -1:
                return l1
            l1.append(i)
            index = i + 1
        return l1
    
def getTable(page,section):
    parsedSource = pullWikiTable(page,section,"wikitext")
    wikitext = parsedSource["parse"]["wikitext"]["*"]
    openVal = findVal(wikitext,"{| ")
    closeVal = findVal(wikitext,"|}\n")
    currentTable = wikitext[int(openVal[0]):int(closeVal[0])]
    currentTable = currentTable[currentTable.find("|-\n"):]
    currentTable = currentTable.split("!")[1:]
    return currentTable

def getSection(driver,request):
    parsedSource = pullWikiTable(driver,0,"sections")
    sectionList = parsedSource['parse']["sections"]
    for i in sectionList:
        if i["line"] == request:
            return(i['index'])
    else:
        return False

def searchWiki(driver):
    link = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch="+driver
    webpage = requests.get(link)
    raw_source = webpage.text
    parsed_source = json.loads(raw_source)
    return parsed_source["query"]["search"][0]["title"]

def computeRedirects(series):
    link = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch="+series
    webpage = requests.get(link)
    raw_source = webpage.text
    parsed_source = json.loads(raw_source)
    return parsed_source["query"]["search"][0]["title"]