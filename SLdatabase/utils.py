from SLbackend.ResultScraping import GenerateResults
from SLbackend.Utils import getSection,searchWiki
from SLbackend.SLComputation import computeSLpoints
from datetime import date,timedelta
from .models import Driver
def generateDriverInfo(name):
    if name:
        history = GenerateResults(name)
        pointSet = computeSLpoints(history)
        driverInfo = Driver(name= name,series = history,live_points = pointSet[1],min_points = pointSet[0],last_updated = date.today())
        driverInfo.save()
        return driverInfo
    else: 
        return False

def checkValid(name):
    checked_name = searchWiki(name)
    if not checked_name:
        return False
    section = getSection(checked_name,"Racing record")
    if section:
        return checked_name
    else:
        return False

def tryUpdate(driverInfo):
    if date.today()-driverInfo.last_updated > timedelta(days=7):
        return generateDriverInfo(driverInfo.name)
    else:
        return driverInfo

def getTopTen():
    driverList = list(Driver.objects.order_by("live_points").reverse()[0:10])
    return driverList

def scanDatabaseName(name):
    for driver in Driver.objects.all():
        check_name = driver.name.lower()
        test_name = name.lower()
        if check_name == test_name:
            return driver.name
        if len(check_name.split())>1:
            if check_name.split()[1] == test_name: #way of dealing with this with multiple last names
                return driver.name
            if len(test_name.split())>1:
                if check_name.split()[1] == test_name.split()[1]:
                    return driver.name
    else:
        checked_name = checkValid(name)
        if not checked_name:
            return False
        else:
            try:
                driver = Driver.objects.get(name=checked_name)
                return driver.name
            except:
                driver_info = generateDriverInfo(checked_name)
                return driver_info.name