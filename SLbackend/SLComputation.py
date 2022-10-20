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

"""def normalizeSeries(series): #TODO
    relevent_series = getReleventSeries(series)
    #Implement later
    return relevent_series

"""
def computeSLpoints(series):
    relevent_series = getReleventSeries(series)
    pointsTable = SLpoints
    total_points = [0,0,0,0]
    final_points = []
    location = -1
    for i in relevent_series: #Implement best 2/3 (best 3/4 with 2020 or 2021)*
        location +=1
        points = 0
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
    return final_points

