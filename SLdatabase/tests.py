from django.test import TestCase
from SLbackend.ResultScraping import GenerateResults
from SLdatabase.models import Driver
from .utils import generateDriverInfo,checkValid, getTopTen, scanDatabaseName,tryUpdate
from SLbackend.SLComputation import computeSLpoints, getReleventSeries
import datetime

class DriverModelTests(TestCase):
    def test_input_driver_read_and_initialized(self):
        testDriver = generateDriverInfo('Colton Herta')
        self.assertAlmostEqual(testDriver.name,'Colton Herta',1)
        self.assertIs(testDriver.series['2014'][1][1],15) 

    def test_wrong_format_driver_name(self):
        testDriver = generateDriverInfo(checkValid('colton herta'))
        self.assertIs(testDriver.series['2014'][1][1],15)

    def test_invalid_driver_name_close(self):
        testDriver = checkValid('fakeName')
        self.assertIs(testDriver,False)

    def test_filter_relevent_series(self): 
        testDriver = generateDriverInfo(checkValid('Colton Herta'))
        filteredList = getReleventSeries(testDriver.series)
        self.assertAlmostEqual(testDriver.name,'Colton Herta',1)
        self.assertEqual(filteredList,[[['IndyCar Series', 7], ['IMSA SportsCar Championship - GTLM', 14]], 
            [['IndyCar Series', 3], ['IMSA SportsCar Championship - GTLM', 9]], 
            [['IndyCar Series', 5], ['IMSA SportsCar Championship - GTD', 50]], 
            [['IndyCar Series', 10], ['IMSA SportsCar Championship - LMP2', 0]]])
    
    def test_single_series_season(self):
         testDriver = generateDriverInfo(checkValid('palou'))
         self.assertIs(testDriver.min_points,65)

    def test_point_computation_correct(self): #Depreciated?
        testDriver = generateDriverInfo('Colton Herta')
        self.assertAlmostEqual(testDriver.name,'Colton Herta',1)
        self.assertIs(testDriver.live_points,32)

    def test_current_season_return(self):
        testDriver = generateDriverInfo('Colton Herta')
        self.assertEqual(testDriver.live_points,32)
        self.assertEqual(testDriver.min_points,32)  

    def test_adj_series_name_multiclass(self): #TODO #Need to strip out multiclass formats, 
        #then correctly assess what point system to use. Still have GT3 to do
        testSeries1 = {'2022': [['IndyCar Series', 1]]}
        demo1 = computeSLpoints(testSeries1)
        self.assertEqual(demo1[0],40)
        testSeries2 = {'2022': [['BRDC British Formula 3 Championship', 1]]}
        demo2 = computeSLpoints(testSeries2)
        self.assertEqual(demo2[0],10)
        testSeries5 = {'2022': [['Spanish Formula 3 Championship', 1]]}
        demo5 = computeSLpoints(testSeries5)
        self.assertEqual(demo5[0],10)
        testSeries3 = {'2022': [['IMSA SportsCar Championship - LMP2', 1]]}
        demo3 = computeSLpoints(testSeries3)
        self.assertEqual(demo3[0],18)
        testSeries4 = {'2022': [['IMSA SportsCar Championship - GTLM', 1]]}
        demo4 = computeSLpoints(testSeries4)
        self.assertEqual(demo4[0],10)
        testSeries6 = {'2022': [['F2000', 1]]}
        demo6 = computeSLpoints(testSeries6)
        self.assertEqual(demo6[0],0)
        testSeries7 = {'2022': [['Asian Le Mans Series - GT3', 1]]}
        demo7 = computeSLpoints(testSeries7)
        self.assertEqual(demo7[0],6)

    def test_update_cycle(self):
        testDriver = generateDriverInfo('Colton Herta')
        self.assertEqual(testDriver.last_updated,datetime.date.today())
        testDriver.last_updated = testDriver.last_updated - datetime.timedelta(days=35)
        self.assertEqual(testDriver.last_updated,datetime.date.today()-datetime.timedelta(days=35))
        testDriver = tryUpdate(testDriver)
        self.assertEqual(testDriver.last_updated,datetime.date.today())

    def test_get_top_10(self):
        Driver.objects.create(name= "name1",series = "history" ,live_points = 5,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name2",series = "history",live_points = 4,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name3",series = "history",live_points = 3,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name4",series = "history",live_points = 1,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name5",series = "history",live_points = 6,min_points = 0,last_updated = datetime.date.today())
        result = getTopTen()
        output = []
        for i in result:
            output.append(i.name)
        self.assertEqual(['name5', 'name1', 'name2', 'name3', 'name4'],output)

    def test_name_input(self):
        Driver.objects.create(name= "Colton Herta", series = "Indycar",live_points = 5,min_points = 0,last_updated = datetime.date.today())
        testName1 = "Herta"
        testName2 = "Colton H" #Not Valid
        testName3 = "Colton Herta"
        testName4 = "C Herta"
        self.assertEqual(scanDatabaseName(testName1),"Colton Herta")
        self.assertEqual(scanDatabaseName(testName2),False)
        self.assertEqual(scanDatabaseName(testName3),"Colton Herta")
        self.assertEqual(scanDatabaseName(testName4),"Colton Herta")



