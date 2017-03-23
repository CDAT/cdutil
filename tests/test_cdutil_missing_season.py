import cdms2,cdutil,sys,MV2,numpy,os,cdat_info
import unittest

class CDUTIL(unittest.TestCase):
    def testMissingSeason(self):

        f=cdms2.open(os.path.join(cdat_info.get_sampledata_path(),'clt.nc'))
        s=f("clt")
        cdutil.setTimeBoundsMonthly(s)

        print 'Getting JJA, which should be inexistant in data'

        with self.assertRaises(Exception):
         cdutil.JJA(s[:5]) 

        ## Create a year worth of data w/o JJA
        s1 = s[:5]
        s2 = s[8:12]

        s3 = MV2.concatenate((s1,s2))
        t = MV2.concatenate((s1.getTime()[:],s2.getTime()[:]))
        t = cdms2.createAxis(t,id='time')
        t.units=s.getTime().units
        t.designateTime()

        s3.setAxis(0,t)
        cdutil.setTimeBoundsMonthly(s3)
        with self.assertRaises(Exception):
          cdutil.JJA(s3)
        with self.assertRaises(Exception):
          cdutil.JJA.departures(s3)
        ## Original Test (badly impleemnted was checking for this
        ## But now returns None
        #with self.assertRaises(Exception):
        self.assertIsNone(cdutil.JJA.climatology(s3))


        # Now gets seasonal cycle, should have JJA all missing
        print 'Testing seasonal cycle on 1 year data w/o JJA should work'
        a = cdutil.SEASONALCYCLE(s3)
        self.assertEqual(a.shape, (4, 46, 72))
        self.assertTrue(numpy.allclose(a.getTime(),[  0.,   3.,   9.,  12.]))
        self.assertTrue(numpy.allclose(a.getTime().getBounds(),numpy.array([[ -1.,   2.],
           [  2.,   5.],
            [  8.,  11.],
             [ 11.,  14.]])))
        self.assertEqual(a.shape,(4,46,72), "Error returned data with wrong shape")
        self.assertTrue(numpy.equal(a.getTime()[:],[  0.,   3.,   9.,  12.]).all(),"Error time are not valid")

        self.assertTrue(numpy.equal(a.getTime().getBounds()[:],[[ -1.,   2.], [  2.,   5.], [  8.,  11.], [ 11.,  14.]]).all(), "Error bound time are not valid")
        d = cdutil.SEASONALCYCLE.departures(s3)
        c = cdutil.SEASONALCYCLE.climatology(s3)
        ## Create 2 year worth of data w/o JJA
        s1 = s[:5]
        s2 = s[8:17]
        s3 = s[20:24]

        s4 = MV2.concatenate((s1,s2))
        s5 = MV2.concatenate((s4,s3))
        t = MV2.concatenate((s1.getTime()[:],s2.getTime()[:]))
        t2 = MV2.concatenate((t,s3.getTime()[:]))
        t = cdms2.createAxis(t2,id='time')
        t.units=s.getTime().units
        t.designateTime()

        s5.setAxis(0,t)
        cdutil.setTimeBoundsMonthly(s5)
        d = cdutil.SEASONALCYCLE.departures(s5)
        c = cdutil.SEASONALCYCLE.climatology(s5)
        with self.assertRaises(Exception):
          cdutil.JJA(s5)
        # Now gets seasonal cycle, should have JJA all missing
        print 'Testing seasonal cycle on 2 years data w/o JJA should work'
        a = cdutil.SEASONALCYCLE(s5)
        self.assertEqual(a.shape,(7,46,72), "Error returned data with wrong shape")

        ## Create 2 years worth of data w/o 1st JJA
        s1 = s[:5]
        s2 = s[8:24]

        s3 = MV2.concatenate((s1,s2))
        t = MV2.concatenate((s1.getTime()[:],s2.getTime()[:]))
        t = cdms2.createAxis(t,id='time')
        t.units=s.getTime().units
        t.designateTime()

        s3.setAxis(0,t)
        cdutil.setTimeBoundsMonthly(s3)
        a = cdutil.JJA(s3)
        self.assertIsNotNone(a,"data w/o 1st season did not return None")

        # Now gets seasonal cycle, should have JJA all missing
        print 'Testing seasonal cycle on 2 years data w/o 1st JJA should work'
        a = cdutil.SEASONALCYCLE(s3)
        d = cdutil.SEASONALCYCLE.departures(s3)
        c = cdutil.SEASONALCYCLE.climatology(s3)
        self.assertEqual(a.shape,(8,46,72), "Error returned data with wrong shape")
        self.assertTrue(numpy.equal(a.getTime()[:],[  0.,   3.,   9.,  12., 15.,18.,21,24]).all(), "Error time are not valid")

        self.assertTrue(numpy.equal(a.getTime().getBounds()[:],[[ -1.,   2.], [  2.,   5.], [  8.,  11.], [ 11.,  14.], [ 14.,  17.], [ 17.,  20.], [ 20.,  23.], [ 23.,  26.]]).all(), "Error bound time are not valid")


        print " Ok we test the filling part"
        print " this should add month '6' as all missing"
        b= cdutil.times.insert_monthly_seasons(a,['JJA',])
        self.assertEqual( b.shape,(9,46,72), "Error returned data with wrong shape")
        self.assertTrue(numpy.equal(b.getTime()[:],[  0.,   3.,6,   9.,  12., 15.,18.,21,24]).all(), "Error time are not valid")

        self.assertTrue(numpy.equal(b.getTime().getBounds()[:],[[ -1.,   2.], [  2.,   5.], [5,8],[  8.,  11.], [ 11.,  14.], [ 14.,  17.], [ 17.,  20.], [ 20.,  23.], [ 23.,  26.]]).all(), "Error bound time are not valid")

        self.assertEqual(b[2].count(), 0,"Error not all times missing in added spot")





        # Now gets seasonal cycle, should have JJA all missing
        print 'Testing seasonal cycle on 2 years data w/o JJA should work'
        a = cdutil.SEASONALCYCLE(s5)
        self.assertEqual(a.shape,(7,46,72), "Error returned data with wrong shape")

        ## Creates data with big gap in years
        s1 = s[:15]
        s2 = s[68:]
        s3 = MV2.concatenate((s1,s2))
        t = MV2.concatenate((s1.getTime()[:],s2.getTime()[:]))
        t = cdms2.createAxis(t,id='time')
        t.units=s.getTime().units
        t.designateTime()

        s3.setAxis(0,t)
        cdutil.setTimeBoundsMonthly(s3)
        a = cdutil.JJA(s3)
        self.assertIsNotNone(a, "data with gap returned None")

        # Now gets seasonal cycle, should have JJA all missing
        print 'Testing seasonal cycle on data with years of gap should work'
        a = cdutil.SEASONALCYCLE(s3)
        d = cdutil.SEASONALCYCLE.departures(s3)
        c = cdutil.SEASONALCYCLE.climatology(s3)
        self.assertEqual(s3.shape, (67, 46, 72))
        self.assertEqual(a.shape, (24, 46, 72))
        self.assertTrue(numpy.equal(a.getTime(), [   0.,    3.,    6.,    9.,   12.,   15.,   69.,   72.,   75.,   78.,   81.,   84.,
             87.,   90.,   93.,   96.,   99.,  102.,  105.,  108.,  111.,  114.,  117.,  120.]).all())

        print " Ok we test the filling part"
        print " this should add month '6' as all missing"
        b= cdutil.times.insert_monthly_seasons(a,cdutil.times.SEASONALCYCLE.seasons)
        self.assertEqual(b.shape, (41,46,72))
        self.assertTrue(numpy.equal(b.getTime()[:],[   0.,    3.,    6.,    9.,   12.,   15.,   18.,   21.,   24.,   27.,   30.,   33.,
             36.,   39.,   42.,   45.,   48.,   51.,   54.,   57.,   60.,   63.,   66.,   69.,
                72.,   75.,   78.,   81.,   84.,   87.,   90.,   93.,   96.,   99.,  102.,  105.,
                  108.,  111.,  114.,  117.,  120.]).all())


        self.assertEqual(cdutil.SEASONALCYCLE.departures(s3).shape, (24, 46, 72) )
        self.assertEqual(a.shape, (24, 46, 72) )
        self.assertEqual(cdutil.SEASONALCYCLE.climatology(s3).shape, (4, 46, 72) )
