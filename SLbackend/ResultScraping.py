#find Wiki Page of driver
#Figure out relevent season finishes
#Find what series they are, and point value
#render
from SLbackend.SLComputation import findPoints
from SLdatabase.models import RacingSeries
from .Utils import getTable,getSection
def GenerateResults(driverClass):
    driver = driverClass.name
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
                a = RacingSeries(year = Year, series_name=currentResults[0],finish=currentResults[1],points=0,driver=driverClass)
                a.save()
                findPoints(a)
            #print(results)
        else:
            if "-" in check[0]:
                Year = int(check[0][0:3]+check[0][-2:])
            else:
                Year = check[0].strip()
            #print(check)
            #print(check)s
            if "|-" in check:
                working = check[0:check.index("|-")]
            else: 
                working = check
            #print(working)
            result = parseTable(working)
            a = RacingSeries(year = Year,series_name = result[0],finish=result[1],points = 0,driver=driverClass)
            a.save()
            findPoints(a)
            #print(results)

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