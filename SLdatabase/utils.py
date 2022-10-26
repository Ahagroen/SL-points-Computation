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
        if driver.name == name:
            return driver.name
        elif driver.name.split()[1] == name: #way of dealing with this with multiple last names
            return driver.name
        elif driver.name.split()[1] == name.split()[1]:
            return driver.name
        else:
            pass
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