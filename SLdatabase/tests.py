from django.test import TestCase
from SLbackend.ResultScraping import GenerateResults
from SLdatabase.models import Driver, RacingSeries
from .utils import generateDriverInfo,checkValid, getTopTen, scanDatabaseName,tryUpdate
from SLbackend.SLComputation import computeSLpoints, findPoints, getReleventSeries
import datetime

class DriverModelTests(TestCase):
    def test_input_driver_read_and_initialized(self):
        testDriver = generateDriverInfo('Colton Herta')
        self.assertAlmostEqual(testDriver.name,'Colton Herta',1)
        #self.assertIs(testDriver.series['2014'][1][1],15) 

    def test_invalid_driver_name_close(self):
        testDriver = checkValid('fakeName')
        self.assertIs(testDriver,False)

    """def test_filter_relevent_series(self): 
        testDriver = generateDriverInfo(checkValid('Colton Herta'))
        filteredList = getReleventSeries(testDriver.series)
        self.assertAlmostEqual(testDriver.name,'Colton Herta',1)
        self.assertEqual(filteredList,[[['IndyCar Series', 7], ['IMSA SportsCar Championship - GTLM', 14]], 
            [['IndyCar Series', 3], ['IMSA SportsCar Championship - GTLM', 9]], 
            [['IndyCar Series', 5], ['IMSA SportsCar Championship - GTD', 50]], 
            [['IndyCar Series', 10], ['IMSA SportsCar Championship - LMP2', 0]]])
    """
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
        testDriver = Driver.objects.create(name= "Colton Herta",live_points = 5,min_points = 0,last_updated = datetime.date.today())
        testSeries1 = RacingSeries.objects.create(year=2022,series_name='IndyCar Series',finish=1, points=0, driver=testDriver) 
        findPoints(testSeries1)
        self.assertEqual(testSeries1.points,40)
        testSeries2 = RacingSeries.objects.create(year=2022, series_name='BRDC British Formula 3 Championship', finish=1, points=0, driver=testDriver)
        findPoints(testSeries2)
        self.assertEqual(testSeries2.points,10)
        testSeries5 = RacingSeries.objects.create(year=2022,series_name='Spanish Formula 3 Championship', finish=1, points=0, driver=testDriver)
        findPoints(testSeries5)
        self.assertEqual(testSeries5.points,10)
        testSeries3 = RacingSeries.objects.create(year=2022, series_name='IMSA SportsCar Championship - LMP2', finish=1, points=0, driver=testDriver)
        findPoints(testSeries3)
        self.assertEqual(testSeries3.points,18)
        testSeries4 = RacingSeries.objects.create(year=2022, series_name='IMSA SportsCar Championship - GTLM', finish=1, points=0, driver=testDriver)
        findPoints(testSeries4)
        self.assertEqual(testSeries4.points,10)
        testSeries6 = RacingSeries.objects.create(year=2022, series_name='F2000',finish=1, points=0, driver=testDriver)
        findPoints(testSeries6)
        self.assertEqual(testSeries6.points,0)
        testSeries7 = RacingSeries.objects.create(year=2022,series_name='Asian Le Mans Series - GT3', finish=1, points=0, driver=testDriver)
        findPoints(testSeries7)
        self.assertEqual(testSeries7.points,6)

    def test_update_cycle(self):
        testDriver = generateDriverInfo('Colton Herta')
        self.assertEqual(testDriver.last_updated,datetime.date.today())
        testDriver.last_updated = testDriver.last_updated - datetime.timedelta(days=35)
        self.assertEqual(testDriver.last_updated,datetime.date.today()-datetime.timedelta(days=35))
        testDriver = tryUpdate(testDriver)
        self.assertEqual(testDriver.last_updated,datetime.date.today())

    def test_get_top_10(self):
        Driver.objects.create(name= "name1",live_points = 5,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name2",live_points = 4,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name3",live_points = 3,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name4",live_points = 1,min_points = 0,last_updated = datetime.date.today())
        Driver.objects.create(name= "name5",live_points = 6,min_points = 0,last_updated = datetime.date.today())
        result = getTopTen()
        output = []
        for i in result:
            output.append(i.name)
        self.assertEqual(['name5', 'name1', 'name2', 'name3', 'name4'],output)

    def test_name_input(self):
        Driver.objects.create(name= "Colton Herta",live_points = 5,min_points = 0,last_updated = datetime.date.today())
        testName1 = "Herta"
        testName2 = "Colton H" #Not Valid
        testName3 = "Colton Herta"
        testName4 = "C Herta"
        testName5 = "herta"
        testName6 = "colton herta"
        testName8 = " colton Herta"
        self.assertEqual(scanDatabaseName(testName1),"Colton Herta")
        self.assertEqual(scanDatabaseName(testName2),False)
        self.assertEqual(scanDatabaseName(testName3),"Colton Herta")
        self.assertEqual(scanDatabaseName(testName4),"Colton Herta")
        self.assertEqual(scanDatabaseName(testName5),"Colton Herta")
        self.assertEqual(scanDatabaseName(testName6),"Colton Herta")
        #self.assertEqual(scanDatabaseName(testName7),"Colton Herta")
        self.assertEqual(scanDatabaseName(testName8),"Colton Herta")

    def test_new_driver_gen(self):
        testName = "Alex Palou"
        self.assertEqual(scanDatabaseName(testName),"Álex Palou")

class RacingSeriesTests(TestCase):
    def test_generation(self):
        test_driver = Driver(name= "Colton Herta",live_points = 5,min_points = 0,last_updated = datetime.date.today())
        test_driver.save()
        a = RacingSeries(year=2015,series_name="test series",points=5,finish=1,driver=test_driver)
        a.save()
        self.assertEqual(a.year,2015)
        self.assertEqual(list(test_driver.racingseries_set.all())[0].year,2015)

    def test_get_releventpoints(self):
        test_driver = Driver(name= "Colton Herta",live_points = 5,min_points = 0,last_updated = datetime.date.today())
        test_driver.save()
        RacingSeries.objects.create(year=2015,series_name="test series",points=10,finish = 1,driver=test_driver)
        RacingSeries.objects.create(year=2020,series_name="test series 2",points=20,finish = 1,driver=test_driver)
        self.assertEqual(list(test_driver.racingseries_set.filter(year__gt=2019))[0].points,20)
