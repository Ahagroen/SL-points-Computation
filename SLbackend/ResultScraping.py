#find Wiki Page of driver
#Figure out relevent season finishes
#Find what series they are, and point value
#render
from .Utils import getTable,getSection
def GenerateResults(driver):
    section = getSection(driver,"Racing record")
    TableList = getTable(driver,section)
    #print(currentTable)
    ind = 0
    #print(TableList)
    while ind <len(TableList):
        #print(TableList[ind])
        if "Position\n" in TableList[ind]:
            TableList = TableList[ind+1:]
            #print(TableList)
            ind = 11
        else:
            ind +=1
    #print(TableList)
    finalTable = {}
    for i in TableList:
        check = i.split("\n")
        if len(check) <3:
            break
        if "|" in check[0]: 
            results = []
            working = []
            Year = i[i.find("|",0)+1:i.find("\n",0)].strip()
            #print(Year)
            first = True
            while "|-" in check:
                #print('a')
                temp = check[0:check.index("|-")]
                check = check[check.index("|-")+1:]
                if first:
                    first = False
                else:
                    temp.insert(0,Year)
                working.append(temp)
            for i in working:
                currentResults = parseTable(i)
                results.append(currentResults)
            #print(results)
        else:
            Year = check[0].strip()
            #print(check)
            #print(Year)
            #print(check)
            if "|-" in check:
                working = check[0:check.index("|-")]
            else: 
                working = check
            #print(working)
            results = parseTable(working)
            #print(results)
        finalTable[Year] = results
    output = {}
    for i in finalTable:
        if '--' not in i:
            output[i] = finalTable[i]
    return output

def parseTable(intake):
    #print(intake)
    series = intake[1].replace("|align=left| ","")
    series = intake[1].replace("|align=left| ","")
    if "[[" in series:
        series = series[series.find("|")+1:]
        series = series.replace("[[",'').replace("]]",'')
    while "|" in series:
        series = series[series.find("|")+1:]
    if intake[-1]:
        finishWorking = str(intake[-1])
    else:
        finishWorking = str(intake[-2])
    #print(finishWorking)
    finishWorking = finishWorking[finishWorking.find("|",1)+1:]
    #print(finishWorking)
    try:
        finish = int(''.join(filter(str.isdigit, finishWorking)))
    except:
        finish = 0
    seriesFinish = [series,finish]
    return seriesFinish


if __name__ == '__main__':
    driver = "Jehan Daruvala"
    print(GenerateResults(driver))