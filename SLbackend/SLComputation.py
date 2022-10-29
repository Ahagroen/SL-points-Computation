from SLdatabase.models import Driver, RacingSeries
from .setup import SLpoints
from .Utils import computeRedirects
from datetime import datetime

def getReleventSeries(table):
    current_year = datetime.now().year
    operating_years = []
    for i in table:
        if '-' in i:
            year = i[0:i.index('-')]
        elif '–' in i:
            year = i[0:i.index('–')]
        else:
            year = i
        if current_year-int(year) <4:
            operating_years.append(table[i])
    return operating_years

def computeSLpoints(driver:Driver): #Keep in mind its possible to have multiple races per year
    corona=False
    if datetime.now().year-2020 <4 or datetime.now().year-2021 <4:
        corona = True
    if corona:
        total_points = []
        for a in range(4):
            points = 0
            current_year = list(driver.racingseries_set.filter(year__exact=(datetime.now().year-a)))
            for i in current_year:
                points+=i.points
            total_points.append((a,points))
        total_points.sort(reverse=True)
        driver.min_points = sum(x[1] for x in total_points[0:3])
        if total_points[0]>total_points[3]:
            driver.live_points = driver.min_points
        else:
            total_points.pop(0)
            driver.live_points = sum(x[1] for x in total_points)
    else:
        total_points = []
        for a in range(3):
            points = 0
            current_year = list(driver.racingseries_set.filter(year__exact=(datetime.now().year-a)))
            for i in current_year:
                points+=i.points
            total_points.append([a,points])
        total_points.sort(reverse=True)
        driver.min_points = sum(x[1] for x in total_points[0:2])
        if total_points[0]>total_points[2]:
            driver.live_points = driver.min_points
        else:
            total_points.pop(0)
            driver.live_points = sum(x[1] for x in total_points)
    driver.save()


    """relevent_series = getReleventSeries(series)
    pointsTable = SLpoints
    total_points = [0,0,0,0]
    final_points = []
    location = -1
    for i in relevent_series: #Implement best 2/3 (best 3/4 with 2020 or 2021)*
        location +=1
        if isinstance(i[0],list):
            for j in range(0,len(i)):
                if i[j][0] in pointsTable:
                    if i[j][1] != 0 and not i[j][1] >10:
                        points +=pointsTable[i[j][0]][i[j][1]-1]
                else:
                    new_series = computeRedirects(i[j][0])
                    if new_series in pointsTable:
                        if i[j][1] != 0 and not i[j][1] >10:
                            points +=pointsTable[new_series][i[j][1]-1]
                    elif "Formula 3" in i[j][0]:
                        if i[j][1] != 0 and not i[j][1] >10:
                            points +=pointsTable["National Formula 3"][i[j][1]-1]
                    elif "GT3" in i[j][0]:
                        if i[j][1] != 0 and not i[j][1] >10:
                            points +=pointsTable["GT3"][i[j][1]-1]
        else:
            if i[0] in pointsTable:
                if i[1] != 0 and not i[1] >10:
                    points +=pointsTable[i[0]][i[1]-1]
            else:
                new_series = computeRedirects(i[0])
                if new_series in pointsTable:
                    if i[1] != 0 and not i[1] >10:
                        points += pointsTable[new_series][i[1]-1]
                elif "Formula 3" in i[j][0]:
                    if i[j][1] != 0 and not i[j][1] >10:
                        points +=pointsTable["National Formula 3"][i[j][1]-1]
                elif "GT3" in i[j][0]:
                    if i[j][1] != 0 and not i[j][1] >10:
                        points +=pointsTable["GT3"][i[j][1]-1]
        total_points[location] = points
    final_points.append(total_points[0]+total_points[1]+total_points[2])
    total_points.sort(reverse= True)
    final_points.append(total_points[0]+total_points[1]+total_points[2])
    return final_points"""

def findPoints(series:RacingSeries):
        event = series.series_name
        finish = series.finish
        if event in SLpoints:
            if finish != 0 and not finish >10:
                points =SLpoints[event][finish-1]
            else:
                points=0
        elif "Formula 3" in event:
                if finish != 0 and not finish >10:
                    points =SLpoints["National Formula 3"][finish-1]
                else:
                    points=0
        elif "GT3" in event:
            if finish != 0 and not finish >10:
                points =SLpoints["GT3"][finish-1]
            else:
                points=0
        else:
            new_series = computeRedirects(event)
            series.series_name = new_series
            if new_series in SLpoints:
                if finish != 0 and not finish >10:
                    points = SLpoints[new_series][finish-1]
                else:
                    points=0
            elif "Formula 3" in new_series:
                if finish != 0 and not finish >10:
                    points =SLpoints["National Formula 3"][finish-1]
                else:
                    points=0
            elif "GT3" in new_series:
                if finish != 0 and not finish >10:
                    points =SLpoints["GT3"][finish-1]
                else:
                    points=0
            else:
                points = 0
        series.points = points
        series.save()
        return
        
